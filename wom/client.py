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

from wom import serializer
from wom import services

__all__ = ("Client",)


class Client:
    __slots__ = ("_http", "_players", "_serializer")

    def __init__(
        self,
        api_key: str | None = None,
        *,
        user_agent: str | None = None,
        api_base_url: str | None = None,
    ) -> None:
        self._serializer = serializer.Serializer()
        self._http = services.HttpService(api_key, user_agent, api_base_url)
        self._players = services.PlayerService(self._http, self._serializer)

    @property
    def players(self) -> services.PlayerService:
        return self._players

    def set_api_key(self, api_key: str) -> None:
        self._http.set_api_key(api_key)

    def set_user_agent(self, user_agent: str) -> None:
        self._http.set_user_agent(user_agent)

    def set_api_base_url(self, api_base_url: str) -> None:
        self._http.set_base_url(api_base_url)

    async def close(self) -> None:
        await self._http.close()
