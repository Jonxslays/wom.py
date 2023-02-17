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

from wom import models
from wom import result
from wom import routes

from . import BaseService

__all__ = ("GroupService",)


class GroupService(BaseService):
    __slots__ = ()

    def _prepare_member_fragments(
        self, members: t.Iterable[models.GroupMemberFragmentModel]
    ) -> tuple[dict[str, t.Any], ...]:
        return tuple({k: str(v) for k, v in m.to_dict().items() if v} for m in members)

    async def search_groups(
        self, name: str | None = None, limit: int | None = None, offset: int | None = None
    ) -> result.Result[list[models.GroupModel], models.HttpErrorResponse]:
        params = self._generate_params(name=name, limit=limit, offset=offset)
        route = routes.SEARCH_GROUPS.compile().with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_group(p) for p in data])

    async def get_group_details(
        self, id: int
    ) -> result.Result[models.GroupDetailModel, models.HttpErrorResponse]:
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
    ) -> result.Result[models.GroupDetailModel, models.HttpErrorResponse]:
        payload = self._generate_params(
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
    ) -> result.Result[models.GroupDetailModel, models.HttpErrorResponse]:
        payload = self._generate_params(
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
    ) -> result.Result[models.HttpSuccessResponse, models.HttpErrorResponse]:
        payload = self._generate_params(verificationCode=verification_code)
        route = routes.DELETE_GROUP.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if not data.message.startswith("Success"):
            return result.Err(data)

        return result.Ok(models.HttpSuccessResponse(data.status, data.message))

    async def add_members(
        self, id: int, verification_code: str, *members: models.GroupMemberFragmentModel
    ) -> result.Result[models.HttpSuccessResponse, models.HttpErrorResponse]:
        payload = self._generate_params(
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
    ) -> result.Result[models.HttpSuccessResponse, models.HttpErrorResponse]:
        payload = self._generate_params(verificationCode=verification_code, members=members)

        route = routes.REMOVE_MEMBERS.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if not data.message.startswith("Success"):
            return result.Err(data)

        return result.Ok(models.HttpSuccessResponse(data.status, data.message))
