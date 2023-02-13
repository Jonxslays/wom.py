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

from wom import constants, routes

__all__ = ("HttpService",)


class HttpService:
    __slots__ = ("_base_url", "_headers", "_session")

    def __init__(
        self,
        *,
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

    def set_api_key(self, api_key: str) -> None:
        self._headers["x-api-key"] = api_key

    def set_user_agent(self, user_agent: str) -> None:
        self._headers["x-user-agent"] = user_agent

    def set_base_url(self, base_url: str) -> None:
        self._base_url = base_url

    async def close(self) -> None:
        if not self._session.closed:
            await self._session.close()

    async def get(
        self,
        route: routes.CompiledRoute,
        *,
        params: dict[str, str | int] = {},
    ) -> dict[str, t.Any]:
        ...

    async def post(
        self,
        route: routes.CompiledRoute,
        *,
        payload: dict[str, t.Any] = {},
        params: dict[str, str | int] = {},
    ) -> dict[str, t.Any]:
        ...

    async def put(
        self,
        route: routes.CompiledRoute,
        *,
        payload: dict[str, t.Any] = {},
        params: dict[str, str | int] = {},
    ) -> dict[str, t.Any]:
        ...

    async def delete(
        self,
        route: routes.CompiledRoute,
        *,
        payload: dict[str, t.Any] = {},
        params: dict[str, str | int] = {},
    ) -> dict[str, t.Any]:
        ...

    async def patch(
        self,
        route: routes.CompiledRoute,
        *,
        payload: dict[str, t.Any] = {},
        params: dict[str, str | int] = {},
    ) -> dict[str, t.Any]:
        ...
