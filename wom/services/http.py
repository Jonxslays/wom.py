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

from __future__ import annotations

import typing as t

import aiohttp

from wom import constants
from wom import models
from wom import routes

__all__ = ("HttpService",)

T = t.TypeVar("T")


class HttpService:
    __slots__ = ("_base_url", "_headers", "_method_mapping", "_session")

    def __init__(
        self,
        api_key: str | None,
        user_agent: str | None,
        api_base_url: str | None,
    ) -> None:
        self._headers = {
            "x-user-agent": (
                f"{constants.USER_AGENT_BASE} {user_agent}"
                if user_agent
                else constants.DEFAULT_USER_AGENT
            )
        }

        if api_key:
            self._headers["x-api-key"] = api_key

        self._base_url = api_base_url or constants.WOM_BASE_URL
        self._session = aiohttp.ClientSession()
        self._method_mapping = {
            "GET": self._session.get,
            "POST": self._session.post,
            "PUT": self._session.put,
            "PATCH": self._session.patch,
            "DELETE": self._session.delete,
        }

    async def _try_get_json(self, response: aiohttp.ClientResponse) -> t.Any:
        try:
            return await response.json()
        except Exception:
            return models.HttpErrorResponse(
                response.status, "Unable to deserialize response, the api is likely down."
            )

    async def _request(
        self, req: t.Callable[..., t.Awaitable[t.Any]], url: str, **kwargs: t.Any
    ) -> t.Any:
        response = await req(url, **kwargs)
        data = await self._try_get_json(response)

        if isinstance(data, models.HttpErrorResponse):
            return data

        if not response.ok or "message" in data:
            return models.HttpErrorResponse(
                response.status,
                data.get("message", "An unexpected error occurred while making the request."),
            )

        return data

    def _get_request_func(self, method: str) -> t.Callable[..., t.Awaitable[t.Any]]:
        return self._method_mapping[method]  # type: ignore

    def set_api_key(self, api_key: str) -> None:
        self._headers["x-api-key"] = api_key

    def set_user_agent(self, user_agent: str) -> None:
        self._headers["x-user-agent"] = user_agent

    def set_base_url(self, base_url: str) -> None:
        self._base_url = base_url

    async def close(self) -> None:
        if not self._session.closed:
            await self._session.close()

    async def fetch(
        self,
        route: routes.CompiledRoute,
        _: t.Type[T],
        *,
        payload: dict[str, t.Any] | None = None,
    ) -> T | models.HttpErrorResponse:
        return await self._request(  # type: ignore
            self._get_request_func(route.method),
            self._base_url + route.uri,
            headers=self._headers,
            params=route.params,
            json=payload or None,
        )
