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

"""Route/endpoint related items."""

from __future__ import annotations

import typing as t

import attrs

__all__ = ("CompiledRoute", "Route")


class CompiledRoute:
    """A route that has been compiled to include uri variables.

    Args:
        route: The route to compile.
    """

    __slots__ = ("_route", "_uri", "_params")

    def __init__(self, route: Route, uri: str) -> None:
        self._uri = uri
        self._route = route
        self._params: t.Dict[str, t.Union[str, int]] = {}

    @property
    def route(self) -> Route:
        """The route itself."""
        return self._route

    @property
    def uri(self) -> str:
        """The routes uri endpoint."""
        return self._uri

    @uri.setter
    def uri(self, uri: str) -> None:
        self._uri = uri

    @property
    def method(self) -> str:
        """The routes method, i.e. GET, POST..."""
        return self.route.method

    @property
    def params(self) -> t.Dict[str, t.Union[str, int]]:
        """The query params for the route."""
        return self._params

    def with_params(self, params: t.Dict[str, t.Any]) -> CompiledRoute:
        """Adds additional query params to this compiled route.

        Args:
            params: The query params to compile.

        Returns:
            The compiled route for chained calls.
        """
        if params:
            self.params.update(params)

        return self


@attrs.define(weakref_slot=False)
class Route:
    """A route that has not been compiled yet."""

    method: str
    """The request method to use."""
    uri: str
    """The request uri."""

    def compile(self, *args: t.Union[str, int]) -> CompiledRoute:
        """Turn this route into a compiled route.

        Args:
            *args: The arguments to insert into the uri.

        Returns:
            The compiled route.
        """
        compiled = CompiledRoute(self, self.uri)

        for arg in args:
            compiled.uri = compiled.uri.replace(r"{}", str(arg), 1)

        return compiled


SEARCH_PLAYERS: t.Final[Route] = Route("GET", "/players/search")
UPDATE_PLAYER: t.Final[Route] = Route("POST", "/players/{}")
ASSERT_PLAYER_TYPE: t.Final[Route] = Route("POST", "/players/{}/assert-type")
PLAYER_DETAILS: t.Final[Route] = Route("GET", "/players/{}")
PLAYER_DETAILS_BY_ID: t.Final[Route] = Route("GET", "/players/id/{}")
PLAYER_ACHIEVEMENTS: t.Final[Route] = Route("GET", "/players/{}/achievements")
PLAYER_ACHIEVEMENT_PROGRESS: t.Final[Route] = Route("GET", "/players/{}/achievements/progress")
PLAYER_COMPETITION_PARTICIPATION: t.Final[Route] = Route("GET", "/players/{}/competitions")
PLAYER_COMPETITION_STANDINGS: t.Final[Route] = Route("GET", "/players/{}/competitions/standings")
PLAYER_GROUP_MEMBERSHIPS: t.Final[Route] = Route("GET", "/players/{}/groups")
PLAYER_GAINS: t.Final[Route] = Route("GET", "/players/{}/gained")
PLAYER_RECORDS: t.Final[Route] = Route("GET", "/players/{}/records")
PLAYER_SNAPSHOTS: t.Final[Route] = Route("GET", "/players/{}/snapshots")
PLAYER_SNAPSHOTS_TIMELINE: t.Final[Route] = Route("GET", "/players/{}/snapshots/timeline")
PLAYER_ARCHIVES: t.Final[Route] = Route("GET", "/players/{}/archives")
SEARCH_NAME_CHANGES: t.Final[Route] = Route("GET", "/names")
SUBMIT_NAME_CHANGE: t.Final[Route] = Route("POST", "/names")
PLAYER_NAME_CHANGES: t.Final[Route] = Route("GET", "/players/{}/names")
GLOBAL_RECORD_LEADERS: t.Final[Route] = Route("GET", "/records/leaderboard")
GLOBAL_EFFICIENCY_LEADERS: t.Final[Route] = Route("GET", "/efficiency/leaderboard")
GLOBAL_DELTA_LEADERS: t.Final[Route] = Route("GET", "/deltas/leaderboard")
SEARCH_GROUPS: t.Final[Route] = Route("GET", "/groups")
GROUP_DETAILS: t.Final[Route] = Route("GET", "/groups/{}")
CREATE_GROUP: t.Final[Route] = Route("POST", "/groups")
EDIT_GROUP: t.Final[Route] = Route("PUT", "/groups/{}")
DELETE_GROUP: t.Final[Route] = Route("DELETE", "/groups/{}")
ADD_MEMBERS: t.Final[Route] = Route("POST", "/groups/{}/members")
REMOVE_MEMBERS: t.Final[Route] = Route("DELETE", "/groups/{}/members")
CHANGE_MEMBER_ROLE: t.Final[Route] = Route("PUT", "/groups/{}/role")
UPDATE_OUTDATED_MEMBERS: t.Final[Route] = Route("POST", "/groups/{}/update-all")
GROUP_GAINS: t.Final[Route] = Route("GET", "/groups/{}/gained")
GROUP_ACHIEVEMENTS: t.Final[Route] = Route("GET", "/groups/{}/achievements")
GROUP_RECORDS: t.Final[Route] = Route("GET", "/groups/{}/records")
GROUP_HISCORES: t.Final[Route] = Route("GET", "/groups/{}/hiscores")
GROUP_NAME_CHANGES: t.Final[Route] = Route("GET", "/groups/{}/name-changes")
GROUP_STATISTICS: t.Final[Route] = Route("GET", "/groups/{}/statistics")
GROUP_COMPETITIONS: t.Final[Route] = Route("GET", "/groups/{}/competitions")
GROUP_ACTIVITY: t.Final[Route] = Route("GET", "/groups/{}/activity")
GROUP_MEMBERS_CSV: t.Final[Route] = Route("GET", "/groups/{}/csv")
SEARCH_COMPETITIONS: t.Final[Route] = Route("GET", "/competitions")
COMPETITION_DETAILS: t.Final[Route] = Route("GET", "/competitions/{}")
TOP_PARTICIPANT_HISTORY: t.Final[Route] = Route("GET", "/competitions/{}/top-history")
CREATE_COMPETITION: t.Final[Route] = Route("POST", "/competitions")
EDIT_COMPETITION: t.Final[Route] = Route("PUT", "/competitions/{}")
DELETE_COMPETITION: t.Final[Route] = Route("DELETE", "/competitions/{}")
UPDATE_OUTDATED_PARTICIPANTS: t.Final[Route] = Route("POST", "/competitions/{}/update-all")
ADD_PARTICIPANTS: t.Final[Route] = Route("POST", "/competitions/{}/participants")
REMOVE_PARTICIPANTS: t.Final[Route] = Route("DELETE", "/competitions/{}/participants")
ADD_TEAMS: t.Final[Route] = Route("POST", "/competitions/{}/teams")
REMOVE_TEAMS: t.Final[Route] = Route("DELETE", "/competitions/{}/teams")
COMPETITION_DETAILS_CSV: t.Final[Route] = Route("GET", "/competitions/{}/csv")
