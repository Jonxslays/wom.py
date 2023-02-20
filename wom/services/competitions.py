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

__all__ = ("CompetitionService",)

ValueT = t.TypeVar("ValueT")
ResultT = result.Result[ValueT, models.HttpErrorResponse]


class CompetitionService(BaseService):
    __slots__ = ()

    async def search_competitions(
        self,
        *,
        title: str | None = None,
        type: models.CompetitionType | None = None,
        status: models.CompetitionStatus | None = None,
        metric: enums.Metric | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.CompetitionModel]]:
        params = self._generate_map(
            title=title,
            limit=limit,
            offset=offset,
            type=type.value if type else None,
            status=status.value if status else None,
            metric=metric.value if metric else None,
        )

        route = routes.SEARCH_COMPETITIONS.compile().with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_competition(c) for c in data])

    async def get_competition_details(
        self, id: int, *, metric: enums.Metric | None = None
    ) -> ResultT[models.CompetitionDetailModel]:
        params = self._generate_map(metric=metric.value if metric else None)
        route = routes.COMPETITION_DETAILS.compile(id).with_params(params)
        data = await self._http.fetch(route, self._dict)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_competition_details(data))

    async def get_top_participant_history(
        self, id: int, *, metric: enums.Metric | None = None
    ) -> ResultT[list[models.Top5ProgressResultModel]]:
        params = self._generate_map(metric=metric.value if metric else None)
        route = routes.TOP_PARTICIPANT_HISTORY.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_top5_progress_result(r) for r in data])

    async def create_competition(
        self,
        title: str,
        metric: enums.Metric,
        starts_at: datetime,
        ends_at: datetime,
        *,
        group_id: int | None = None,
        group_verification_code: str | None = None,
        teams: list[models.TeamModel] | None = None,
        participants: list[str] | None = None,
    ) -> ResultT[models.CompetitionWithParticipationsModel]:
        payload = self._generate_map(
            title=title,
            teams=teams,
            groupId=group_id,
            participants=participants,
            endsAt=ends_at.isoformat(),
            startsAt=starts_at.isoformat(),
            metric=metric.value if metric else None,
            groupVerificationCode=group_verification_code,
        )

        route = routes.CREATE_COMPETITION.compile()
        data = await self._http.fetch(route, self._dict, payload=payload)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(
            self._serializer.deserialize_competition_with_participation(data["competition"])
        )

    async def edit_competition(
        self,
        id: int,
        verification_code: str,
        *,
        title: str | None = None,
        metric: enums.Metric | None = None,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
        teams: list[models.TeamModel] | None = None,
        participants: list[str] | None = None,
    ) -> ResultT[models.CompetitionWithParticipationsModel]:
        payload = self._generate_map(
            title=title,
            teams=teams,
            participants=participants,
            startsAt=starts_at.isoformat() if starts_at else None,
            endsAt=ends_at.isoformat() if ends_at else None,
            metric=metric.value if metric else None,
            verificationCode=verification_code,
        )

        route = routes.EDIT_COMPETITION.compile(id)
        data = await self._http.fetch(route, self._dict, payload=payload)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_competition_with_participation(data))

    async def delete_competition(
        self, old_name: str, new_name: str
    ) -> ResultT[models.HttpSuccessResponse]:
        raise NotImplementedError

    async def add_participants(
        self, old_name: str, new_name: str
    ) -> ResultT[models.HttpSuccessResponse]:
        raise NotImplementedError

    async def remove_participants(
        self, old_name: str, new_name: str
    ) -> ResultT[models.HttpSuccessResponse]:
        raise NotImplementedError

    async def add_teams(self, old_name: str, new_name: str) -> ResultT[models.HttpSuccessResponse]:
        raise NotImplementedError

    async def remove_teams(
        self, old_name: str, new_name: str
    ) -> ResultT[models.HttpSuccessResponse]:
        raise NotImplementedError

    async def update_outdated_participants(
        self, old_name: str, new_name: str
    ) -> ResultT[models.HttpSuccessResponse]:
        raise NotImplementedError
