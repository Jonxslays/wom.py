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
    """Handles endpoints related to groups."""

    __slots__ = ()

    def _prepare_member_fragments(
        self, members: t.Iterable[models.GroupMemberFragment]
    ) -> tuple[dict[str, t.Any], ...]:
        return tuple({k: str(v) for k, v in m.to_dict().items() if v} for m in members)

    async def search_groups(
        self, name: str | None = None, limit: int | None = None, offset: int | None = None
    ) -> ResultT[list[models.Group]]:
        """Searches for groups that at least partially match the given
        name.

        Args:
            name: The group name to search for.
            limit: The pagination limit.
            offset: The pagination offset.

        Returns:
            A [`Result`][wom.Result] containing the list of matching
                groups.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.search_groups("Some group", limit=3)
            ```
        """
        params = self._generate_map(name=name, limit=limit, offset=offset)
        route = routes.SEARCH_GROUPS.compile().with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_group(p) for p in data])

    async def get_details(self, id: int) -> ResultT[models.GroupDetail]:
        """Gets the details for the given group id.

        Args:
            id: The group ID to get details for.

        Returns:
            A [`Result`][wom.Result] containing the group details.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_details(1234)
            ```
        """
        route = routes.GROUP_DETAILS.compile(id)
        data = await self._http.fetch(route, self._dict)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_group_details(data))

    async def create_group(
        self,
        name: str,
        *members: models.GroupMemberFragment,
        clan_chat: str | None = None,
        description: str | None = None,
        homeworld: int | None = None,
    ) -> ResultT[models.GroupDetail]:
        """Creates a new group.

        Args:
            name: The name for the group.

            *members: The optional members to add to the group.

        Keyword Args:
            clan_chat: The optional clan chat for the group. Defaults to
                `None`.

            description: The optional group description.Defaults to
                `None`.

            homeworld: The optional homeworld for the group. Defaults to
                `None`.

        Returns:
            A [`Result`][wom.Result] containing the group details.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.create_group(
                "My new group",
                "Jonxslays",
                "Zezima",
                description="The most epic group."
            )
            ```
        """
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
        members: t.Iterable[models.GroupMemberFragment] | None = None,
        clan_chat: str | None = None,
        description: str | None = None,
        homeworld: int | None = None,
    ) -> ResultT[models.GroupDetail]:
        """Edits an existing group.

        Args:
            id: The ID of the group.

            verification_code: The group verification code.

        Keyword Args:
            name: The optional new name for the group. Defaults to
                `None`.

            members: The optional iterable of members to replace the
                existing group members with. Defaults to `None`.

            clan_chat: The optional new clan chat for the group.
                Defaults to `None`.

            description: The optional new group description.Defaults to
                `None`.

            homeworld: The optional new homeworld for the group.
                Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the group details.

        !!! warning

            The members list provided will completely replace the
            existing members. If you want to add members, see
            [`add_members()`][wom.GroupService.add_members]

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.edit_group(
                123,
                "111-111-111",
                name="My new group name",
                members=["Jonxslays"],
                description="Some new description."
            )
            ```
        """
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
        """Deletes an existing group.

        Args:
            id: The ID of the group.

            verification_code: The group verification code.

        Returns:
            A [`Result`][wom.Result] containing the success response
                message.

        !!! warning

            This action is irreversible.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.delete_group(123, "111-111-111")
            ```
        """
        payload = self._generate_map(verificationCode=verification_code)
        route = routes.DELETE_GROUP.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if not data.message.startswith("Success"):
            return result.Err(data)

        return result.Ok(models.HttpSuccessResponse(data.status, data.message))

    async def add_members(
        self, id: int, verification_code: str, *members: models.GroupMemberFragment
    ) -> ResultT[models.HttpSuccessResponse]:
        """Adds members to an existing group.

        Args:
            id: The ID of the group.

            verification_code: The group verification code.

            *members: The members to add to the group.

        Returns:
            A [`Result`][wom.Result] containing the success response
                message.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.add_members(
                123,
                "111-111-111",
                wom.GroupMemberFragment(
                    "Jonxslays", wom.GroupRole.Administrator
                ),
                wom.GroupMemberFragment("Zezima"),
                wom.GroupMemberFragment("Psikoi"),
            )
            ```
        """
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
        """Removes members from an existing group.

        Args:
            id: The ID of the group.

            verification_code: The group verification code.

            *members: The members to remove from the group.

        Returns:
            A [`Result`][wom.Result] containing the success response
                message.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.remove_members(
                123,
                "111-111-111",
                "Jonxslays",
                "Zezima",
            )
            ```
        """
        payload = self._generate_map(verificationCode=verification_code, members=members)

        route = routes.REMOVE_MEMBERS.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if not data.message.startswith("Success"):
            return result.Err(data)

        return result.Ok(models.HttpSuccessResponse(data.status, data.message))

    async def change_member_role(
        self, id: int, verification_code: str, username: str, role: models.GroupRole
    ) -> ResultT[models.GroupMembership]:
        """Changes the role for a member in an existing group.

        Args:
            id: The ID of the group.

            verification_code: The group verification code.

            username: The username of the player to update.

            role: The players new group role.

        Returns:
            A [`Result`][wom.Result] containing the players group
                membership.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.change_member_role(
                123,
                "111-111-111",
                "Jonxslays",
                wom.GroupRole.Admiral
            )
            ```
        """
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
        """Attempts to update all outdated group members.

        !!! info

            Group members are considered outdated when they haven't been
            updated in over 24h.

        !!! warning

            This method adds every outdated member to an "update queue",
            and the WOM servers try to update players in the queue one
            by one, with a delay in between each. For each player in the
            queue, an attempt is made to update it up to 3 times, with
            30s in between each attempt.

            Please note that this is dependent on the OSRS hiscores
            functioning correctly, and therefore this method does NOT
            guarantee the players will be updated, it only guarantees
            that an attempt will be made to update them, up to 3 times.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.groups.update_outdated_members(
                123, "111-111-111"
            )
            ```

        Args:
            id: The ID of the group.

            verification_code: The verification code for the group.

        Returns:
            A [`Result`][wom.Result] containing the success response
                message.
        """
        payload = self._generate_map(verificationCode=verification_code)
        route = routes.UPDATE_OUTDATED_MEMBERS.compile(id)
        data = await self._http.fetch(route, models.HttpErrorResponse, payload=payload)

        if "players are being updated" in data.message:
            return result.Ok(models.HttpSuccessResponse(data.status, data.message))

        return result.Err(data)

    async def get_competitions(
        self, id: int, *, limit: int | None = None, offset: int | None = None
    ) -> ResultT[list[models.Competition]]:
        """Gets competitions for a given group.

        Args:
            id: The ID of the group.

        Keyword Args:
            limit: The optional pagination limit. Defaults to `None`.

            offset: The optional pagination offset. Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of
                competitions.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_competitions(123, limit=10)
            ```
        """
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_COMPETITIONS.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_competition(c) for c in data])

    async def get_gains(
        self,
        id: int,
        metric: enums.Metric,
        *,
        period: enums.Period | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.DeltaLeaderboardEntry]]:
        """Gets the gains for a group over a particular time frame.

        Args:
            id: The ID of the group.

            metric: The metric to filter on.

        Keyword Args:
            period: The optional period of time to get gains for.
                Defaults to `None`.

            start_date: The minimum date to get the gains from. Defaults
                to `None`.

            end_date: The maximum date to get the gains from. Defaults
                to `None`.

            limit: The optional pagination limit. Defaults to `None`.

            offset: The optional pagination offset. Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of delta
                leaderboard entries.

        !!! info

            You can pass either (`period`) or (`start_date` +
            `end_date`), but not both.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_gains(
                123, wom.Bosses.Zulrah, limit=10
            )
            ```
        """
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

    async def get_achievements(
        self,
        id: int,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.Achievement]]:
        """Gets the achievements for the group.

        Args:
            id: The ID of the group.

        Keyword Args:
            limit: The optional pagination limit. Defaults to `None`.

            offset: The optional pagination offset. Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of
                achievements.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_achievements(123, limit=10)
            ```
        """
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_ACHIEVEMENTS.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_achievement(a) for a in data])

    async def get_records(
        self,
        id: int,
        metric: enums.Metric,
        period: enums.Period,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.RecordLeaderboardEntry]]:
        """Gets the records held by players in the group.

        Args:
            id: The ID of the group.

            metric: The metric to filter on.

            period: The period of time to get records for.

        Keyword Args:
            limit: The optional pagination limit. Defaults to `None`.

            offset: The optional pagination offset. Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of record
                leaderboard entries.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_records(
                123, wom.Bosses.Zulrah, wom.Period.Day, limit=3
            )
            ```
        """
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

    async def get_hiscores(
        self,
        id: int,
        metric: enums.Metric,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultT[list[models.GroupHiscoresEntry]]:
        """Gets the hiscores for the group.

        Args:
            id: The ID of the group.

            metric: The metric to filter on.

        Keyword Args:
            limit: The optional pagination limit. Defaults to `None`.

            offset: The optional pagination offset. Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list of hiscores
                entries.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_hiscores(
                123, wom.Skills.Runecrafting, limit=10
            )
            ```
        """
        params = self._generate_map(limit=limit, offset=offset, metric=metric.value)
        route = routes.GROUP_HISCORES.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_group_hiscores_entry(h) for h in data])

    async def get_name_changes(
        self, id: int, *, limit: int | None = None, offset: int | None = None
    ) -> ResultT[list[models.NameChange]]:
        """Gets the past name changes for the group.

        Args:
            id: The ID of the group.

        Keyword Args:
            limit: The optional pagination limit. Defaults to `None`.

            offset: The optional pagination offset. Defaults to `None`.

        Returns:
            A [`Result`][wom.Result] containing the list name changes.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_name_changes(123, limit=10)
            ```
        """
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_NAME_CHANGES.compile(id).with_params(params)
        data = await self._http.fetch(route, self._list)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_name_change(n) for n in data])

    async def get_statistics(self, id: int) -> ResultT[models.GroupStatistics]:
        """Gets the statistics for the group.

        Args:
            id: The ID of the group.

        Returns:
            A [`Result`][wom.Result] containing the statistics.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_statistics(123)
            ```
        """
        route = routes.GROUP_STATISTICS.compile(id)
        data = await self._http.fetch(route, self._dict)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(self._serializer.deserialize_group_statistics(data))
