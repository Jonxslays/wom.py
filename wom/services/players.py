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


class PlayerService(BaseService):
    __slots__ = ()

    async def search_players(
        self, username: str, *, limit: int | None = None, offset: int | None = None
    ) -> result.Result[list[models.PlayerModel], models.HttpErrorResponse]:
        params = self._generate_params(username=username, limit=limit, offset=offset)
        route = routes.SEARCH_PLAYERS.compile().with_params(params)
        data = await self._http.fetch(route, list[dict[str, t.Any]])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_player(player) for player in data])

    async def update_player(
        self, username: str
    ) -> result.Result[models.PlayerDetailModel, models.HttpErrorResponse]:
        route = routes.UPDATE_PLAYER.compile(username)
        data = await self._http.fetch(route, dict[str, t.Any])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_player_details(data))

    async def assert_player_type(
        self, username: str
    ) -> result.Result[models.AssertPlayerTypeModel, models.HttpErrorResponse]:
        route = routes.ASSERT_PLAYER_TYPE.compile(username)
        data = await self._http.fetch(route, dict[str, t.Any])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_asserted_player_type(data))

    async def get_player_details(
        self, username: str
    ) -> result.Result[models.PlayerDetailModel, models.HttpErrorResponse]:
        route = routes.PLAYER_DETAILS.compile(username)
        data = await self._http.fetch(route, dict[str, t.Any])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_player_details(data))

    async def get_player_details_by_id(
        self, player_id: int
    ) -> result.Result[models.PlayerDetailModel, models.HttpErrorResponse]:
        route = routes.PLAYER_DETAILS_BY_ID.compile(player_id)
        data = await self._http.fetch(route, dict[str, t.Any])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_player_details(data))

    async def get_player_achievements(
        self, username: str
    ) -> result.Result[list[models.AchievementModel], models.HttpErrorResponse]:
        route = routes.PLAYER_ACHIEVEMENTS.compile(username)
        data = await self._http.fetch(route, list[dict[str, t.Any]])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_achievement(a) for a in data])

    async def get_player_achievement_progress(
        self, username: str
    ) -> result.Result[list[models.PlayerAchievementProgressModel], models.HttpErrorResponse]:
        route = routes.PLAYER_ACHIEVEMENT_PROGRESS.compile(username)
        data = await self._http.fetch(route, list[dict[str, t.Any]])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(
            [self._serializer.deserialize_player_achievement_progress(p) for p in data]
        )

    async def get_player_competition_participation(
        self,
        username: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
        status: models.CompetitionStatus | None = None,
    ) -> result.Result[None, models.HttpErrorResponse]:
        raise NotImplementedError(
            "competition related endpoints are not yet implemented."
        )  # Temporary

        params = self._generate_params(status=status.value, limit=limit, offset=offset)
        route = routes.PLAYER_COMPETITION_PARTICIPATION.compile(username).with_params(params)
        data = await self._http.fetch(route, list[dict[str, t.Any]])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(None)  # TODO: deserialize the model once its created

    async def get_player_gains(
        self,
        username: str,
        *,
        period: enums.Period | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> result.Result[models.PlayerGainsModel, models.HttpErrorResponse]:
        params = self._generate_params(
            period=period.value if period else None,
            startDate=start_date.isoformat() if start_date else None,
            endDate=end_date.isoformat() if end_date else None,
        )

        route = routes.PLAYER_GAINS.compile(username).with_params(params)
        data = await self._http.fetch(route, dict[str, t.Any])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_player_gains(data))

    async def get_player_snapshots(
        self,
        username: str,
        *,
        period: enums.Period | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> result.Result[list[models.SnapshotModel], models.HttpErrorResponse]:
        params = self._generate_params(
            period=period.value if period else None,
            startDate=start_date.isoformat() if start_date else None,
            endDate=end_date.isoformat() if end_date else None,
        )

        route = routes.PLAYER_SNAPSHOTS.compile(username).with_params(params)
        data = await self._http.fetch(route, list[dict[str, t.Any]])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_snapshot(s) for s in data])

    async def get_player_name_changes(
        self, username: str
    ) -> result.Result[list[models.NameChangeModel], models.HttpErrorResponse]:
        route = routes.PLAYER_NAME_CHANGES.compile(username)
        data = await self._http.fetch(route, list[dict[str, t.Any]])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_name_change(c) for c in data])
