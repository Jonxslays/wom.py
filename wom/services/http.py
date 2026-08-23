# wom.py - An asynchronous wrapper for the Wise Old Man API.
# Copyright (c) 2023-present Jonxslays
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""The http service module."""

from __future__ import annotations

import typing as t

import aiohttp
import msgspec

from wom import constants
from wom import models
from wom import routes
from wom.serializer import Serializer

__all__ = ("HttpService",)

T = t.TypeVar("T")

# A request body is either a JSON object (the common case) or a bare JSON
# array (e.g. the bulk name-change endpoint, which posts a top-level array).
Payload = t.Union[t.Dict[str, t.Any], t.List[t.Any]]


class HttpService:
    """The HTTP service used to make requests to the WOM API.

    Parameters
    ----------
    api_key : str, optional
        The optional api key to use.
    user_agent : str, optional
        The optional user agent to use.
    api_base_url : str, optional
        The optional api base url to use.
    serializer : Serializer, optional
        The optional serializer to use for encoding and decoding.
        If not provided a new one is created; the [`Client`][wom.Client]
        injects its shared serializer so decoding happens in one place.
    """

    __slots__ = ("_base_url", "_headers", "_method_mapping", "_serializer", "_session")

    def __init__(
        self,
        api_key: t.Optional[str],
        user_agent: t.Optional[str],
        api_base_url: t.Optional[str],
        serializer: t.Optional[Serializer] = None,
    ) -> None:
        user_agent = (
            f"{constants.USER_AGENT_BASE} {user_agent}"
            if user_agent
            else constants.DEFAULT_USER_AGENT
        )

        self._headers = {
            "x-user-agent": user_agent,
            "User-Agent": user_agent,
        }

        if api_key:
            self._headers["x-api-key"] = api_key

        self._base_url = api_base_url or constants.WOM_BASE_URL
        self._serializer = serializer or Serializer()

    async def _read_content(
        self, response: aiohttp.ClientResponse
    ) -> t.Union[bytes, models.HttpErrorResponse]:
        try:
            return await response.content.read()
        except Exception:
            return models.HttpErrorResponse("Failed to read response content.", response.status)

    async def _request(
        self,
        req: t.Callable[..., t.Awaitable[t.Any]],
        url: str,
        message_response: bool = False,
        **kwargs: t.Any,
    ) -> t.Union[bytes, models.HttpErrorResponse, models.HttpSuccessResponse]:
        response = await req(url, **kwargs)
        content = await self._read_content(response)

        if isinstance(content, models.HttpErrorResponse):
            return content

        if not response.ok:
            return self._parse_error(content, response.status)

        if message_response:
            # These endpoints return a bare ``{"message": ...}`` envelope
            # instead of a model. WOM signals failure via the HTTP status, so
            # any 2xx here is a success (see docs.wiseoldman.net).
            return self._parse_success(content, response.status)

        return content

    def _parse_error(self, content: bytes, status: int) -> models.HttpErrorResponse:
        default = "An unexpected error occurred while making the request."

        try:
            error = self._serializer.decode(content, t.Dict[str, t.Any])
        except msgspec.DecodeError:
            # The body wasn't the JSON object we expected (e.g. an HTML error
            # page from a gateway, or an empty body). Preserve the status so
            # the caller still gets a well-formed Err instead of an exception,
            # keeping the "service methods never raise on API errors" contract.
            return models.HttpErrorResponse(default, status)

        return models.HttpErrorResponse(error.get("message", default), status, error.get("code"))

    def _parse_success(self, content: bytes, status: int) -> models.HttpSuccessResponse:
        try:
            success = self._serializer.decode(content, models.HttpSuccessResponse)
        except msgspec.DecodeError:
            # A 2xx without the expected ``{"message": ...}`` body still counts
            # as success; synthesize an empty message rather than raising.
            success = models.HttpSuccessResponse("")

        success.status = status
        return success

    def _get_request_func(self, method: str) -> t.Callable[..., t.Awaitable[t.Any]]:
        if not hasattr(self, "_method_mapping"):
            raise RuntimeError("HttpService.start was never called, aborting...")

        return self._method_mapping[method]

    async def _init_session(self) -> None:
        self._session = aiohttp.ClientSession(
            json_serialize=lambda o: self._serializer.encode(o).decode()
        )

        self._method_mapping = {
            "GET": self._session.get,
            "POST": self._session.post,
            "PUT": self._session.put,
            "PATCH": self._session.patch,
            "DELETE": self._session.delete,
        }

    def set_api_key(self, api_key: str) -> None:
        """Sets the api key used by the http service.

        Parameters
        ----------
        api_key : str
            The new api key to use.
        """
        self._headers["x-api-key"] = api_key

    def unset_api_key(self) -> None:
        """Un-sets the current api key so it isn't sent with requests."""
        if "x-api-key" in self._headers:
            del self._headers["x-api-key"]

    def set_user_agent(self, user_agent: str) -> None:
        """Sets the user agent used by the http service.

        Parameters
        ----------
        user_agent : str
            The new user agent to use.
        """
        self._headers["x-user-agent"] = user_agent
        self._headers["User-Agent"] = user_agent

    def set_base_url(self, base_url: str) -> None:
        """Sets the api base url used by the http service.

        Parameters
        ----------
        base_url : str
            The new base url to use.
        """
        self._base_url = base_url

    async def start(self) -> None:
        """Starts the client session to be used by the http service."""
        if not hasattr(self, "_session"):
            await self._init_session()

    async def close(self) -> None:
        """Closes the existing client session, if it's still open."""
        if hasattr(self, "_session") and not self._session.closed:
            await self._session.close()

    @t.overload
    async def fetch(
        self,
        route: routes.CompiledRoute,
        *,
        payload: t.Optional[Payload] = ...,
    ) -> t.Union[bytes, models.HttpErrorResponse]: ...

    @t.overload
    async def fetch(
        self,
        route: routes.CompiledRoute,
        *,
        payload: t.Optional[Payload] = ...,
        message_response: t.Literal[True],
    ) -> t.Union[models.HttpSuccessResponse, models.HttpErrorResponse]: ...

    async def fetch(
        self,
        route: routes.CompiledRoute,
        *,
        payload: t.Optional[Payload] = None,
        message_response: bool = False,
    ) -> t.Union[bytes, models.HttpErrorResponse, models.HttpSuccessResponse]:
        """Fetches the given route.

        Parameters
        ----------
        route : routes.CompiledRoute
            The route to make the request to.
        payload : dict[str, Any] | list[Any], optional
            The optional payload to send in the request
            body. May be a JSON object or a bare JSON array.
        message_response : bool
            Whether the endpoint returns a bare message envelope
            (`HttpSuccessResponse`) rather than a model. Defaults to
            `False`.

        Returns
        -------
        bytes | HttpSuccessResponse | HttpErrorResponse
            The raw bytes (or `HttpSuccessResponse` when
            `message_response` is set) on success, or the
            `HttpErrorResponse` on failure.
        """
        return await self._request(
            self._get_request_func(route.method),
            self._base_url + route.uri,
            message_response,
            headers=self._headers,
            params=route.params,
            json=payload or None,
        )
