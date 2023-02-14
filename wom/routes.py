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
from dataclasses import dataclass

__all__ = (
    "CompiledRoute",
    "Route",
    "ASSERT_PLAYER_TYPE",
    "GET_PLAYER_ACHIEVEMENTS",
    "GET_PLAYER_DETAILS",
    "GET_PLAYER_DETAILS_BY_ID",
    "SEARCH_PLAYERS",
    "UPDATE_PLAYER",
)


@dataclass(slots=True)
class CompiledRoute:
    params: dict[str, str | int]
    route: Route

    def __init__(self, route: Route) -> None:
        self.route = route
        self.params = {}

    @property
    def uri(self) -> str:
        return self.route.uri

    @uri.setter
    def uri(self, uri: str) -> None:
        self.route.uri = uri

    @property
    def method(self) -> str:
        return self.route.method

    def with_params(self, params: dict[str, str | int]) -> CompiledRoute:
        if params:
            self.params.update(params)

        return self


@dataclass(slots=True)
class Route:
    method: str
    uri: str

    def compile(self, *args: str | int) -> CompiledRoute:
        compiled = CompiledRoute(self)

        for arg in args:
            compiled.uri = compiled.uri.replace(r"{}", str(arg), 1)

        return compiled


SEARCH_PLAYERS: t.Final[Route] = Route("GET", "/players/search")
UPDATE_PLAYER: t.Final[Route] = Route("POST", "/players/{}")
ASSERT_PLAYER_TYPE: t.Final[Route] = Route("POST", "/players/{}/assert-type")
GET_PLAYER_DETAILS: t.Final[Route] = Route("GET", "/players/{}")
GET_PLAYER_DETAILS_BY_ID: t.Final[Route] = Route("GET", "/players/id/{}")
GET_PLAYER_ACHIEVEMENTS: t.Final[Route] = Route("GET", "/players/{}/achievements")
