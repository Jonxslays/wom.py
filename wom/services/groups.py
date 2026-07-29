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


T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]


class GroupService(BaseService):
    """Handles endpoints related to groups."""

    __slots__ = ()

    def _prepare_member_fragments(
        self, members: t.Iterable[t.Union[str, models.GroupMemberFragment]]
    ) -> tuple[t.Dict[str, t.Any], ...]:
        return tuple(
            {k: str(v) for k, v in m.to_dict().items() if v}
            for m in self._parse_member_fragments(members)
        )

    def _parse_member_fragments(
        self, members: t.Iterable[t.Union[str, models.GroupMemberFragment]]
    ) -> t.Generator[models.GroupMemberFragment, None, None]:
        return (models.GroupMemberFragment(m, None) if isinstance(m, str) else m for m in members)

    async def search_groups(
        self,
        name: t.Optional[str] = None,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.Group]]:
        """Searches for groups that at least partially match the given
        name.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.search_groups("Some group", limit=3)
            ```

        Parameters
        ----------
        name : str, optional
            The group name to search for.
        limit : int, optional
            The pagination limit.
        offset : int, optional
            The pagination offset.

        Returns
        -------
        Result
            A result containing the list of matching
            groups.
        """
        params = self._generate_map(name=name, limit=limit, offset=offset)
        route = routes.SEARCH_GROUPS.compile().with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.Group])

    async def get_details(self, id: int) -> ResultT[models.GroupDetail]:
        """Gets the details for the given group id.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_details(1234)
            ```

        Parameters
        ----------
        id : int
            The group ID to get details for.

        Returns
        -------
        Result
            A result containing the group details.
        """
        route = routes.GROUP_DETAILS.compile(id)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, models.GroupDetail)

    async def create_group(
        self,
        name: str,
        *members: t.Union[str, models.GroupMemberFragment],
        clan_chat: t.Optional[str] = None,
        description: t.Optional[str] = None,
        homeworld: t.Optional[int] = None,
    ) -> ResultT[models.CreatedGroupDetail]:
        """Creates a new group.

        !!! note

            A mixture of strings and GroupMemberFragments can be passed for
            members. If a string is passed, no role will be added for that
            member.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.create_group(
                "My new group",
                wom.GroupMemberFragment("Jonxslays", wom.GroupRole.Owner),
                "Faabvk",
                "psikoi",
                "rro",
                description="The most epic group."
            )
            ```

        Parameters
        ----------
        name : str
            The name for the group.
        *members : str or GroupMemberFragment
            The optional members to add to the group.
        clan_chat : str, optional
            The optional clan chat for the group. Defaults to
            `None`.
        description : str, optional
            The optional group description. Defaults to
            `None`.
        homeworld : int, optional
            The optional homeworld for the group. Defaults to
            `None`.

        Returns
        -------
        Result
            A result containing the created group details.
        """
        payload = self._generate_map(
            name=name,
            clanChat=clan_chat,
            homeworld=homeworld,
            description=description,
            members=self._prepare_member_fragments(members),
        )

        route = routes.CREATE_GROUP.compile()
        data = await self._http.fetch(route, payload=payload)
        return self._ok_or_err(data, models.CreatedGroupDetail)

    async def edit_group(
        self,
        id: int,
        verification_code: str,
        *,
        name: t.Optional[str] = None,
        members: t.Optional[t.Iterable[t.Union[str, models.GroupMemberFragment]]] = None,
        clan_chat: t.Optional[str] = None,
        description: t.Optional[str] = None,
        homeworld: t.Optional[int] = None,
        social_links: t.Optional[models.SocialLinks] = None,
    ) -> ResultT[models.GroupDetail]:
        """Edits an existing group.

        !!! warning

            The members list provided will completely replace the
            existing members. If you want to add members, see
            [`add_members()`][wom.GroupService.add_members]

        !!! note

             A mixture of strings and GroupMemberFragments can be passed for
             members. If a string is passed, no role will be added for that
             member.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.edit_group(
                123,
                "111-111-111",
                name="My new group name",
                members=[
                    wom.GroupMemberFragment("Jonxslays", wom.GroupRole.Owner),
                    "Faabvk",
                ],
                description="Some new description."
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        verification_code : str
            The group verification code.
        name : str, optional
            The optional new name for the group. Defaults to
            `None`.
        members : Iterable[str or GroupMemberFragment], optional
            The optional iterable of members to replace the
            existing group members with. Defaults to `None`.
        clan_chat : str, optional
            The optional new clan chat for the group.
            Defaults to `None`.
        description : str, optional
            The optional new group description. Defaults to
            `None`.
        homeworld : int, optional
            The optional new homeworld for the group.
            Defaults to `None`.
        social_links : SocialLinks, optional
            The optional new social links for the group.
            Defaults to `None`.

        Returns
        -------
        Result
            A result containing the group details.
        """
        payload = self._generate_map(
            name=name,
            clanChat=clan_chat,
            homeworld=homeworld,
            description=description,
            verificationCode=verification_code,
            members=self._prepare_member_fragments(members) if members else None,
            socialLinks=social_links.to_dict() if social_links else None,
        )

        route = routes.EDIT_GROUP.compile(id)
        data = await self._http.fetch(route, payload=payload)
        return self._ok_or_err(data, models.GroupDetail)

    async def delete_group(
        self, id: int, verification_code: str
    ) -> ResultT[models.HttpSuccessResponse]:
        """Deletes an existing group.

        !!! warning

            This action is irreversible.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.delete_group(123, "111-111-111")
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        verification_code : str
            The group verification code.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.DELETE_GROUP.compile(id)
        payload = self._generate_map(verificationCode=verification_code)
        data = await self._http.fetch(route, payload=payload, allow_http_success=True)
        return self._success_or_err(data)

    async def add_members(
        self, id: int, verification_code: str, *members: t.Union[str, models.GroupMemberFragment]
    ) -> ResultT[models.HttpSuccessResponse]:
        """Adds members to an existing group.

        !!! note

             A mixture of strings and GroupMemberFragments can be passed for
             members. If a string is passed, no role will be added for that
             member.

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
                "Zezima",
                "Psikoi",
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        verification_code : str
            The group verification code.
        *members : str or GroupMemberFragment
            The members to add to the group.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        payload = self._generate_map(
            verificationCode=verification_code,
            members=self._prepare_member_fragments(members),
        )

        route = routes.ADD_MEMBERS.compile(id)
        data = await self._http.fetch(route, payload=payload, allow_http_success=True)
        return self._success_or_err(data)

    async def remove_members(
        self, id: int, verification_code: str, *members: str
    ) -> ResultT[models.HttpSuccessResponse]:
        """Removes members from an existing group.

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

        Parameters
        ----------
        id : int
            The ID of the group.
        verification_code : str
            The group verification code.
        *members : str
            The usernames of members to remove from the group.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.REMOVE_MEMBERS.compile(id)
        payload = self._generate_map(verificationCode=verification_code, members=members)
        data = await self._http.fetch(route, payload=payload, allow_http_success=True)
        return self._success_or_err(data)

    async def change_member_role(
        self, id: int, verification_code: str, username: str, role: models.GroupRole
    ) -> ResultT[models.GroupMembership]:
        """Changes the role for a member in an existing group.

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

        Parameters
        ----------
        id : int
            The ID of the group.
        verification_code : str
            The group verification code.
        username : str
            The username of the player to update.
        role : GroupRole
            The players new group role.

        Returns
        -------
        Result
            A result containing the players group
            membership.
        """
        payload = self._generate_map(
            verificationCode=verification_code, username=username, role=role.value
        )

        route = routes.CHANGE_MEMBER_ROLE.compile(id)
        data = await self._http.fetch(route, payload=payload)
        return self._ok_or_err(data, models.GroupMembership)

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

        Parameters
        ----------
        id : int
            The ID of the group.
        verification_code : str
            The verification code for the group.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.UPDATE_OUTDATED_MEMBERS.compile(id)
        payload = self._generate_map(verificationCode=verification_code)
        data = await self._http.fetch(route, payload=payload, allow_http_success=True)
        return self._success_or_err(data, predicate=lambda m: "players are being updated" in m)

    async def get_competitions(
        self, id: int, *, limit: t.Optional[int] = None, offset: t.Optional[int] = None
    ) -> ResultT[t.List[models.Competition]]:
        """Gets competitions for a given group.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_competitions(123, limit=10)
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        limit : int, optional
            The optional pagination limit. Defaults to `None`.
        offset : int, optional
            The optional pagination offset. Defaults to `None`.

        Returns
        -------
        Result
            A result containing the list of
            competitions.
        """
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_COMPETITIONS.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.Competition])

    async def get_gains(
        self,
        id: int,
        metric: enums.Metric,
        *,
        period: t.Optional[enums.Period] = None,
        start_date: t.Optional[datetime] = None,
        end_date: t.Optional[datetime] = None,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.GroupMemberGains]]:
        """Gets the gains for a group over a particular time frame.

        !!! info

            You must pass one of (`period`) or (`start_date` +
            `end_date`), but not both.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_gains(
                123, wom.Metric.Zulrah, period=wom.Period.Week, limit=10
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        metric : Metric
            The metric to filter on.
        period : Period, optional
            The optional period of time to get gains for.
            Defaults to `None`.
        start_date : datetime, optional
            The minimum date to get the gains from. Defaults
            to `None`.
        end_date : datetime, optional
            The maximum date to get the gains from. Defaults
            to `None`.
        limit : int, optional
            The optional pagination limit. Defaults to `None`.
        offset : int, optional
            The optional pagination offset. Defaults to `None`.

        Returns
        -------
        Result
            A result containing the list of group gains.
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
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.GroupMemberGains])

    async def get_bulk_gains(
        self,
        id: int,
        *,
        period: t.Optional[enums.Period] = None,
        start_date: t.Optional[datetime] = None,
        end_date: t.Optional[datetime] = None,
    ) -> ResultT[t.List[models.BulkGroupMemberGains]]:
        """Gets the bulk gains of all metrics for a group over a particular time frame.

        !!! info

            You must pass one of (`period`) or (`start_date` +
            `end_date`), but not both.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_bulk_gains(
                123, period=wom.Period.Week
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        period : Period, optional
            The optional period of time to get gains for.
            Defaults to `None`.
        start_date : datetime, optional
            The minimum date to get the gains from. Defaults
            to `None`.
        end_date : datetime, optional
            The maximum date to get the gains from. Defaults
            to `None`.

        Returns
        -------
        Result
            A result containing the list of bulk group gains.
        """
        params = self._generate_map(
            period=period.value if period else None,
            endDate=end_date.isoformat() if end_date else None,
            startDate=start_date.isoformat() if start_date else None,
        )

        route = routes.GROUP_BULK_GAINS.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.BulkGroupMemberGains])

    async def get_achievements(
        self,
        id: int,
        *,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.Achievement]]:
        """Gets the achievements for the group.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_achievements(123, limit=10)
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        limit : int, optional
            The optional pagination limit. Defaults to `None`.
        offset : int, optional
            The optional pagination offset. Defaults to `None`.

        Returns
        -------
        Result
            A result containing the list of achievements.
        """
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_ACHIEVEMENTS.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.Achievement])

    async def get_records(
        self,
        id: int,
        metric: enums.Metric,
        period: enums.Period,
        *,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.RecordLeaderboardEntry]]:
        """Gets the records held by players in the group.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_records(
                123, wom.Metric.Zulrah, wom.Period.Day, limit=3
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        metric : Metric
            The metric to filter on.
        period : Period
            The period of time to get records for.
        limit : int, optional
            The optional pagination limit. Defaults to `None`.
        offset : int, optional
            The optional pagination offset. Defaults to `None`.

        Returns
        -------
        Result
            A result containing the list of record
            leaderboard entries.
        """
        params = self._generate_map(
            limit=limit,
            offset=offset,
            metric=metric.value,
            period=period.value,
        )

        route = routes.GROUP_RECORDS.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.RecordLeaderboardEntry])

    async def get_hiscores(
        self,
        id: int,
        metric: enums.Metric,
        *,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.GroupHiscoresEntry]]:
        """Gets the hiscores for the group.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_hiscores(
                123, wom.Metric.Runecrafting, limit=10
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        metric : Metric
            The metric to filter on.
        limit : int, optional
            The optional pagination limit. Defaults to `None`.
        offset : int, optional
            The optional pagination offset. Defaults to `None`.

        Returns
        -------
        Result
            A result containing the list of hiscores
            entries.
        """
        params = self._generate_map(limit=limit, offset=offset, metric=metric.value)
        route = routes.GROUP_HISCORES.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.GroupHiscoresEntry])

    async def get_bulk_hiscores(self, id: int) -> ResultT[t.List[models.BulkGroupHiscoresEntry]]:
        """Gets the bulk hiscores for the group.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_bulk_hiscores(123)
            ```

        Parameters
        ----------
        id : int
            The ID of the group.

        Returns
        -------
        Result
            A result containing the list of bulk
            hiscores entries.
        """
        route = routes.GROUP_BULK_HISCORES.compile(id)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.BulkGroupHiscoresEntry])

    async def get_name_changes(
        self, id: int, *, limit: t.Optional[int] = None, offset: t.Optional[int] = None
    ) -> ResultT[t.List[models.NameChange]]:
        """Gets the past name changes for the group.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_name_changes(123, limit=10)
            ```

        Parameters
        ----------
        id : int
            The ID of the group.
        limit : int, optional
            The optional pagination limit. Defaults to `None`.
        offset : int, optional
            The optional pagination offset. Defaults to `None`.

        Returns
        -------
        Result
            A result containing the list name changes.
        """
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_NAME_CHANGES.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.NameChange])

    async def get_statistics(self, id: int) -> ResultT[models.GroupStatistics]:
        """Gets the statistics for the group.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_statistics(123)
            ```

        Parameters
        ----------
        id : int
            The ID of the group.

        Returns
        -------
        Result
            A result containing the statistics.
        """
        route = routes.GROUP_STATISTICS.compile(id)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, models.GroupStatistics)

    async def get_activity(
        self,
        id: int,
        *,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.GroupActivity]]:
        """Gets the activity for the group. This is a paginated endpoint.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            await client.groups.get_activity(69, limit=5)
            ```

        Parameters
        ----------
        id : int
            The ID of the group to fetch activity for.
        limit : int, optional
            The pagination limit.
        offset : int, optional
            The pagination offset.

        Returns
        -------
        Result
            A result containing the list of activities.
        """
        params = self._generate_map(limit=limit, offset=offset)
        route = routes.GROUP_ACTIVITY.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.GroupActivity])

    async def get_members_csv(self, id: int) -> ResultT[str]:
        """Gets members in this group in CSV format.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.groups.get_members_csv(123)
            ```

        Parameters
        ----------
        id : int
            The ID of the group.

        Returns
        -------
        Result
            A result containing the CSV string.
        """
        route = routes.GROUP_MEMBERS_CSV.compile(id)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(data.decode())
