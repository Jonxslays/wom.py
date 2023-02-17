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

from dataclasses import dataclass
from typing import Final

__all__ = (
    "CompiledRoute",
    "Route",
    "ADD_MEMBERS",
    "ASSERT_PLAYER_TYPE",
    "CHANGE_MEMBER_ROLE",
    "CREATE_GROUP",
    "EDIT_GROUP",
    "DELETE_GROUP",
    "GLOBAL_DELTA_LEADERS",
    "GLOBAL_EFFICIENCY_LEADERS",
    "GROUP_ACHIEVEMENTS",
    "GROUP_GAINS",
    "GROUP_HISCORES",
    "GROUP_NAME_CHANGES",
    "GROUP_RECORDS",
    "GLOBAL_RECORD_LEADERS",
    "GROUP_DETAILS",
    "NAME_CHANGE_DETAILS",
    "PLAYER_ACHIEVEMENT_PROGRESS",
    "PLAYER_ACHIEVEMENTS",
    "PLAYER_COMPETITION_PARTICIPATION",
    "PLAYER_DETAILS",
    "PLAYER_DETAILS_BY_ID",
    "PLAYER_NAME_CHANGES",
    "PLAYER_GAINS",
    "PLAYER_SNAPSHOTS",
    "REMOVE_MEMBERS",
    "SEARCH_GROUPS",
    "SEARCH_NAME_CHANGES",
    "SEARCH_PLAYERS",
    "SUBMIT_NAME_CHANGE",
    "UPDATE_OUTDATED_MEMBERS",
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


SEARCH_PLAYERS: Final[Route] = Route("GET", "/players/search")
UPDATE_PLAYER: Final[Route] = Route("POST", "/players/{}")
ASSERT_PLAYER_TYPE: Final[Route] = Route("POST", "/players/{}/assert-type")
PLAYER_DETAILS: Final[Route] = Route("GET", "/players/{}")
PLAYER_DETAILS_BY_ID: Final[Route] = Route("GET", "/players/id/{}")
PLAYER_ACHIEVEMENTS: Final[Route] = Route("GET", "/players/{}/achievements")
PLAYER_ACHIEVEMENT_PROGRESS: Final[Route] = Route("GET", "/players/{}/achievements/progress")
PLAYER_COMPETITION_PARTICIPATION: Final[Route] = Route("GET", "/players/{}/competitions")
PLAYER_GAINS: Final[Route] = Route("GET", "/players/{}/gained")
PLAYER_SNAPSHOTS: Final[Route] = Route("GET", "/players/{}/snapshots")
SEARCH_NAME_CHANGES: Final[Route] = Route("GET", "/names")
SUBMIT_NAME_CHANGE: Final[Route] = Route("POST", "/names")
NAME_CHANGE_DETAILS: Final[Route] = Route("GET", "/names/{}")
PLAYER_NAME_CHANGES: Final[Route] = Route("GET", "/players/{}/names")
GLOBAL_RECORD_LEADERS: Final[Route] = Route("GET", "/records/leaderboard")
GLOBAL_EFFICIENCY_LEADERS: Final[Route] = Route("GET", "/efficiency/leaderboard")
GLOBAL_DELTA_LEADERS: Final[Route] = Route("GET", "/deltas/leaderboard")
SEARCH_GROUPS: Final[Route] = Route("GET", "/groups")
GROUP_DETAILS: Final[Route] = Route("GET", "/groups/{}")
CREATE_GROUP: Final[Route] = Route("POST", "/groups")
EDIT_GROUP: Final[Route] = Route("PUT", "/groups/{}")
DELETE_GROUP: Final[Route] = Route("DELETE", "/groups/{}")
ADD_MEMBERS: Final[Route] = Route("POST", "/groups/{}/members")
REMOVE_MEMBERS: Final[Route] = Route("DELETE", "/groups/{}/members")
CHANGE_MEMBER_ROLE: Final[Route] = Route("PUT", "/groups/{}/role")
UPDATE_OUTDATED_MEMBERS: Final[Route] = Route("POST", "/groups/{}/update-all")
GROUP_GAINS: Final[Route] = Route("GET", "/groups/{}/gained")
GROUP_ACHIEVEMENTS: Final[Route] = Route("GET", "/groups/{}/achievements")
GROUP_RECORDS: Final[Route] = Route("GET", "/groups/{}/records")
GROUP_HISCORES: Final[Route] = Route("GET", "/groups/{}/hiscores")
GROUP_NAME_CHANGES: Final[Route] = Route("GET", "/groups/{}/name-changes")
