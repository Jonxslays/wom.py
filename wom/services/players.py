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
from datetime import datetime

from wom import enums
from wom import models
from wom import result
from wom import routes

from . import BaseService

__all__ = ("PlayerService",)

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]


class PlayerService(BaseService):
    """Handles endpoints related to players."""

    __slots__ = ()

    async def search_players(
        self, username: str, *, limit: t.Optional[int] = None, offset: t.Optional[int] = None
    ) -> ResultT[t.List[models.Player]]:
        """Searches for a player by partial username.

        Args:
            username: The username to search for.

        Keyword Args:
            limit: The maximum number of paginated items to receive.
                Defaults to `None`.

            offset: The page offset for requesting the next page.
                Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of matching
                players.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.search_players("Jonxslays", limit=3)
            ```
        """
        params = self._generate_map(username=username, limit=limit, offset=offset)
        route = routes.SEARCH_PLAYERS.compile().with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.Player])

    async def update_player(self, username: str) -> ResultT[models.PlayerDetail]:
        """Updates the given player.

        Args:
            username: The username to update.

        Returns:
            A [`Result`][wom.Result] containing the updated player
                details.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.update_player("Jonxslays")
            ```
        """
        route = routes.UPDATE_PLAYER.compile(username)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, models.PlayerDetail)

    async def assert_player_type(self, username: str) -> ResultT[models.AssertPlayerType]:
        """Asserts, and fixes, a players type.

        Args:
            username: The username to assert the type for.

        Returns:
            A [`Result`][wom.Result] containing the asserted player
                type.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.assert_player_type("Jonxslays")
            ```
        """
        route = routes.ASSERT_PLAYER_TYPE.compile(username)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, models.AssertPlayerType)

    async def get_details(self, username: str) -> ResultT[models.PlayerDetail]:
        """Gets the details for a given player.

        Args:
            username: The username to get the details for.

        Returns:
            A [`Result`][wom.Result] containing the player details.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_details("Jonxslays")
            ```
        """
        route = routes.PLAYER_DETAILS.compile(username)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, models.PlayerDetail)

    async def get_details_by_id(self, player_id: int) -> ResultT[models.PlayerDetail]:
        """Gets the details for a given player id.

        Args:
            player_id: The is of the player to get the details for.

        Returns:
            A [`Result`][wom.Result] containing the player details.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_details_by_id(1234)
            ```
        """
        route = routes.PLAYER_DETAILS_BY_ID.compile(player_id)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, models.PlayerDetail)

    async def get_achievements(self, username: str) -> ResultT[t.List[models.Achievement]]:
        """Gets the achievements for a given player.

        Args:
            username: The username to get the achievements for.

        Returns:
            A [`Result`][wom.Result] containing the list of player
                achievements.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_achievements("Jonxslays")
            ```
        """
        route = routes.PLAYER_ACHIEVEMENTS.compile(username)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.Achievement])

    async def get_achievement_progress(
        self, username: str
    ) -> ResultT[t.List[models.PlayerAchievementProgress]]:
        """Gets the progress towards achievements for a given player.

        Args:
            username: The username to get the achievement progress for.

        Returns:
            A [`Result`][wom.Result] containing the list of player
                achievement progress.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_achievement_progress("Jonxslays")
            ```
        """
        route = routes.PLAYER_ACHIEVEMENT_PROGRESS.compile(username)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.PlayerAchievementProgress])

    async def get_competition_participations(
        self,
        username: str,
        *,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
        status: t.Optional[models.CompetitionStatus] = None,
    ) -> ResultT[t.List[models.PlayerParticipation]]:
        """Gets the competition participations for a given player.

        Args:
            username: The username to get the participations for.

        Keyword Args:
            limit: The maximum number of paginated items to receive.
                Defaults to `None` (I think thats 20 items?).

            offset: The page offset for requesting multiple pages.
                Defaults to `None`.

            status: The optional [`CompetitionStatus`]
                [wom.CompetitionStatus] to filter on. Defaults to
                `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of competition
                participations.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_competition_participations(
                "Jonxslays", limit=3
            )
            ```
        """
        params = self._generate_map(
            status=status.value if status else None,
            offset=offset,
            limit=limit,
        )

        route = routes.PLAYER_COMPETITION_PARTICIPATION.compile(username)
        data = await self._http.fetch(route.with_params(params))
        return self._ok_or_err(data, t.List[models.PlayerParticipation])

    async def get_competition_standings(
        self,
        username: str,
        status: models.CompetitionStatus,
    ) -> ResultT[t.List[models.PlayerCompetitionStanding]]:
        """Gets the competition standings for a given player.

        Args:
            username: The username to get the standings for.

            status: The competition status to get standings for.

        Returns:
            A [`Result`][wom.Result] containing the list of competition
                standings.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_competition_standings(
                "Jonxslays", wom.CompetitionStatus.Ongoing
            )
            ```
        """
        params = self._generate_map(status=status.value)
        route = routes.PLAYER_COMPETITION_STANDINGS.compile(username)
        data = await self._http.fetch(route.with_params(params))
        return self._ok_or_err(data, t.List[models.PlayerCompetitionStanding])

    async def get_group_memberships(
        self, username: str, *, limit: t.Optional[int] = None, offset: t.Optional[int] = None
    ) -> ResultT[t.List[models.PlayerMembership]]:
        """Gets the group memberships for the given player.

        Args:
            username: The username to get the memberships for.

        Keyword Args:
            limit: The maximum number of paginated items to receive.
                Defaults to `None` (I think thats 20 items?).

            offset: The page offset for requesting multiple pages.
                Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of group
                memberships.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_group_memberships(
                "Jonxslays", limit=3
            )
            ```
        """
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.PLAYER_GROUP_MEMBERSHIPS.compile(username)
        data = await self._http.fetch(route.with_params(params))
        return self._ok_or_err(data, t.List[models.PlayerMembership])

    async def get_gains(
        self,
        username: str,
        *,
        period: t.Optional[enums.Period] = None,
        start_date: t.Optional[datetime] = None,
        end_date: t.Optional[datetime] = None,
    ) -> ResultT[models.PlayerGains]:
        """Gets the gains made by this player over the given time span.

        Args:
            username: The username to get the gains for.

        Keyword Args:
            period: The optional period of time to get gains for.
                Defaults to `None`.

            start_date: The minimum date to get the gains from. Defaults
                to `None`.

            end_date: The maximum date to get the gains from. Defaults
                to `None`.

        Returns:
            A [`Result`][wom.Result] containing the players gains.

        !!! info

            You must pass one of (`period`) or (`start_date` +
            `end_date`), but not both.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_gains(
                "Jonxslays", period=wom.Period.Day
            )
            ```
        """
        params = self._generate_map(
            period=period.value if period else None,
            startDate=start_date.isoformat() if start_date else None,
            endDate=end_date.isoformat() if end_date else None,
        )

        route = routes.PLAYER_GAINS.compile(username).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, models.PlayerGains)

    async def get_records(
        self,
        username: str,
        *,
        period: t.Optional[enums.Period] = None,
        metric: t.Optional[enums.Metric] = None,
    ) -> ResultT[t.List[models.Record]]:
        """Gets the records held by this player.

        Args:
            username: The username to get the gains for.

        Keyword Args:
            period: The optional period of time to get records for.
                Defaults to `None`.

            metric: The optional metric to filter the records on.
                Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing a list of the players
                records.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_records(
                "Jonxslays", period=wom.Period.Day, metric=wom.Metric.Attack
            )
            ```
        """
        params = self._generate_map(
            period=period.value if period else None, metric=metric.value if metric else None
        )

        route = routes.PLAYER_RECORDS.compile(username).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.Record])

    async def get_snapshots(
        self,
        username: str,
        *,
        period: t.Optional[enums.Period] = None,
        start_date: t.Optional[datetime] = None,
        end_date: t.Optional[datetime] = None,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.Snapshot]]:
        """Gets the snapshots for the player.

        Args:
            username: The username to get the snapshots for.

        Keyword Args:
            period: The optional period of time to get snapshots for.
                Defaults to `None`.

            start_date: The minimum date to get the snapshots from.
                Defaults to `None`.

            end_date: The maximum date to get the snapshots from.
                Defaults to `None`.

            limit: The maximum number of paginated items to receive.
                Defaults to `None`.

            offset: The page offset for requesting the next page.
                Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of snapshots.

        !!! info

            You can pass either (`period`) or (`start_date` +
            `end_date`), but not both.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_snapshots(
                "Jonxslays", period=wom.Period.Week, limit=3
            )
            ```
        """
        params = self._generate_map(
            period=period.value if period else None,
            startDate=start_date.isoformat() if start_date else None,
            endDate=end_date.isoformat() if end_date else None,
            limit=limit if limit else None,
            offset=offset if offset else None,
        )

        route = routes.PLAYER_SNAPSHOTS.compile(username)
        data = await self._http.fetch(route.with_params(params))
        return self._ok_or_err(data, t.List[models.Snapshot])

    async def get_name_changes(self, username: str) -> ResultT[t.List[models.NameChange]]:
        """Gets the name changes for the player.

        Args:
            username: The username to get the name changes for.

        Returns:
            A [`Result`][wom.Result] containing the list of name changes.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_name_changes("Jonxslays")
            ```
        """
        route = routes.PLAYER_NAME_CHANGES.compile(username)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.NameChange])

    async def get_snapshots_timeline(
        self,
        username: str,
        metric: enums.Metric,
        *,
        period: t.Optional[enums.Period] = None,
        start_date: t.Optional[datetime] = None,
        end_date: t.Optional[datetime] = None,
    ) -> ResultT[t.List[models.SnapshotTimelineEntry]]:
        """Gets the snapshots timeline for the given player and metric.

        Args:
            username: The username to get the timeline for.

            metric: The metric to get the timeline for.

        Keyword Args:
            period: The optional period of time to get snapshots for.
                Defaults to `None`.

            start_date: The minimum date to get the snapshots from.
                Defaults to `None`.

            end_date: The maximum date to get the snapshots from.
                Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of snapshots timeline
                entries.

        !!! info

            You can pass either (`period`) or (`start_date` +
            `end_date`), but not both.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_snapshots_timeline(
                "Jonxslays", wom.Skills.Attack, period=wom.Period.Week
            )
            ```
        """
        params = self._generate_map(
            period=period.value if period else None,
            startDate=start_date.isoformat() if start_date else None,
            endDate=end_date.isoformat() if end_date else None,
            metric=metric.value,
        )

        route = routes.PLAYER_SNAPSHOTS_TIMELINE.compile(username)
        data = await self._http.fetch(route.with_params(params))
        return self._ok_or_err(data, t.List[models.SnapshotTimelineEntry])

    async def get_archives(
        self,
        username: str,
    ) -> ResultT[t.List[models.PlayerArchive]]:
        """Gets the archives for the given player.

        Args:
            username: The username to get archives for.

        Returns:
            A [`Result`][wom.Result] containing the list of archives.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.players.get_archives("Jonxslays")
            ```
        """
        route = routes.PLAYER_ARCHIVES.compile(username)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.PlayerArchive])
