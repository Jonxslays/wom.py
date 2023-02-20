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

__all__ = ("GroupService",)


ValueT = t.TypeVar("ValueT")
ResultT = result.Result[ValueT, models.HttpErrorResponse]


class GroupService(BaseService):
    __slots__ = ()

    def _prepare_member_fragments(
        self, members: t.Iterable[models.GroupMemberFragmentModel]
    ) -> tuple[dict[str, t.Any], ...]:
        return tuple({k: str(v) for k, v in m.to_dict().items() if v} for m in members)

    async def search_groups(
        self, name: str | None = None, limit: int | None = None, offset: int | None = None
    ) -> ResultT[list[models.GroupModel]]:
        params = self._generate_map(name=name, limit=limit, offset=offset)
        route = routes.SEARCH_GROUPS.compile().with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_group(p) for p in data])

    async def get_group_details(self, id: int) -> ResultT[models.GroupDetailModel]:
        route = routes.GROUP_DETAILS.compile(id)
        data = await self._http.fetch(route, self._dict)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_group_details(data))

    async def create_group(
        self,
        name: str,
        *members: models.GroupMemberFragmentModel,
        clan_chat: str | None = None,
        description: str | None = None,
        homeworld: int | None = None,
    ) -> ResultT[models.GroupDetailModel]:
        payload = self._generate_map(
            name=name,
            clanChat=clan_chat,
            homeworld=homeworld,
            description=description,
            members=self._prepare_member_fragments(members),
        )

        route = routes.CREATE_GROUP.compile()
        data = await self._http.fetch(route, self._dict, payload=payload)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        # Verification code is only present on new group creations
        group = self._serializer.deserialize_group_details(data["group"])
        group.verification_code = data["verificationCode"]
        return result.Ok(group)

    async def edit_group(
        self,
        id: int,
        verification_code: str,
        *,
        name: str | None = None,
        members: t.Iterable[models.GroupMemberFragmentModel] | None = None,
        clan_chat: str | None = None,
        description: str | None = None,
        homeworld: int | None = None,
    ) -> ResultT[models.GroupDetailModel]:
        payload = self._generate_map(
            name=name,
            clanChat=clan_chat,
            homeworld=homeworld,
            description=description,
            verificationCode=verification_code,
            members=self._prepare_member_fragments(members) if members else None,
        )

        route = routes.EDIT_GROUP.compile(id)
        data = await self._http.fetch(route, self._dict, payload=payload)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_group_details(data))

    async def delete_group(
        self, id: int, verification_code: str
    ) -> ResultT[models.HttpSuccessResponse]:
        payload = self._generate_map(verificationCode=verification_code)
        route = routes.DELETE_GROUP.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if not data.message.startswith("Success"):
            return result.Err(data)

        return result.Ok(models.HttpSuccessResponse(data.status, data.message))

    async def add_members(
        self, id: int, verification_code: str, *members: models.GroupMemberFragmentModel
    ) -> result.Result[models.HttpSuccessResponse, models.HttpErrorResponse]:
        payload = self._generate_map(
            verificationCode=verification_code,
            members=self._prepare_member_fragments(members),
        )

        route = routes.ADD_MEMBERS.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if not data.message.startswith("Success"):
            return result.Err(data)

        return result.Ok(models.HttpSuccessResponse(data.status, data.message))

    async def remove_members(
        self, id: int, verification_code: str, *members: str
    ) -> ResultT[models.HttpSuccessResponse]:
        payload = self._generate_map(verificationCode=verification_code, members=members)

        route = routes.REMOVE_MEMBERS.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if not data.message.startswith("Success"):
            return result.Err(data)

        return result.Ok(models.HttpSuccessResponse(data.status, data.message))

    async def change_member_role(
        self, id: int, verification_code: str, username: str, role: models.GroupRole
    ) -> ResultT[models.GroupMembershipModel]:
        payload = self._generate_map(
            verificationCode=verification_code, username=username, role=role.value
        )

        route = routes.CHANGE_MEMBER_ROLE.compile(id)
        data = await self._http.fetch(route, self._dict, payload=payload)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_group_membership(data))

    async def update_outdated_members(
        self, id: int, verification_code: str
    ) -> ResultT[models.HttpSuccessResponse]:
        payload = self._generate_map(verificationCode=verification_code)
        route = routes.UPDATE_OUTDATED_MEMBERS.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if "players are being updated" in data.message:
            return result.Ok(models.HttpSuccessResponse(data.status, data.message))

        return result.Err(data)

    async def get_group_competitions(
        self, id: int, *, limit: int | None = None, offset: int | None = None
    ) -> ResultT[list[models.CompetitionModel]]:
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_COMPETITIONS.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_competition(c) for c in data])

    async def get_group_gains(
        self,
        id: int,
        metric: enums.Metric,
        *,
        period: enums.Period | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.DeltaLeaderboardEntryModel]]:
        params = self._generate_map(
            limit=limit,
            offset=offset,
            metric=metric.value,
            period=period.value if period else None,
            endDate=end_date.isoformat() if end_date else None,
            startDate=start_date.isoformat() if start_date else None,
        )

        route = routes.GROUP_GAINS.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_delta_leaderboard_entry(d) for d in data])

    async def get_group_achievements(
        self,
        id: int,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.AchievementModel]]:
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_ACHIEVEMENTS.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_achievement(a) for a in data])

    async def get_group_records(
        self,
        id: int,
        metric: enums.Metric,
        period: enums.Period,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.RecordLeaderboardEntryModel]]:
        params = self._generate_map(
            limit=limit,
            offset=offset,
            metric=metric.value,
            period=period.value,
        )

        route = routes.GROUP_RECORDS.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_record_leaderboard_entry(a) for a in data])

    async def get_group_hiscores(
        self,
        id: int,
        metric: enums.Metric,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.GroupHiscoresEntryModel]]:
        params = self._generate_map(limit=limit, offset=offset, metric=metric.value)
        route = routes.GROUP_HISCORES.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_group_hiscores_entry(h) for h in data])

    async def get_group_name_changes(
        self, id: int, *, limit: int | None = None, offset: int | None = None
    ) -> ResultT[list[models.NameChangeModel]]:
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_NAME_CHANGES.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_name_change(n) for n in data])

    async def get_group_statistics(self, id: int) -> ResultT[models.GroupStatisticsModel]:
        route = routes.GROUP_STATISTICS.compile(id)
        data = await self._http.fetch(route, self._dict)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_group_statistics(data))
