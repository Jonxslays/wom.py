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

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]


class CompetitionService(BaseService):
    """Handles endpoints related to competitions."""

    __slots__ = ()

    def _merge_metrics(
        self, metric: t.Optional[enums.Metric], metrics: t.Optional[t.Sequence[enums.Metric]]
    ) -> t.Optional[t.List[str]]:
        merged: t.List[str] = []
        combined = ([metric] if metric is not None else []) + list(metrics or ())

        for item in combined:
            if item.value not in merged:
                merged.append(item.value)

        return merged or None

    async def search_competitions(
        self,
        *,
        title: t.Optional[str] = None,
        type: t.Optional[models.CompetitionType] = None,
        status: t.Optional[models.CompetitionStatus] = None,
        metric: t.Optional[enums.Metric] = None,
        metrics: t.Optional[t.List[enums.Metric]] = None,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.Competition]]:
        """Searches for competitions with the given criteria.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.search_competitions(
                title="Sick Competition",
                type=wom.CompetitionType.Classic,
                status=wom.CompetitionStatus.Ongoing,
                metrics=[wom.Metric.Zulrah, wom.Metric.Vorkath],
                limit=3,
                offset=1
            )
            ```

        Parameters
        ----------
        title : str, optional
            The optional title of the competition. Defaults to
            `None`.
        type : CompetitionType, optional
            The optional competition type filter. Defaults to `None`
        status : CompetitionStatus, optional
            The optional competition status filter. Defaults to `None`.
        metric : Metric, optional
            The optional metric filter. Defaults to `None`.

            !!! warning "Deprecated"

                Use `metrics` instead. If both are passed, they are
                combined.
        metrics : list[Metric], optional
            The optional metrics filter. Matches competitions that track
            any of these metrics. Defaults to `None`.
        limit : int, optional
            The maximum number of paginated items to receive.
            Defaults to `None` (I think thats 20 items?).
        offset : int, optional
            The page offset for requesting multiple pages.
            Defaults to `None`.

        Returns
        -------
        Result
            A result containing the list of competitions
            or an error.
        """
        params = self._generate_map(
            title=title,
            limit=limit,
            offset=offset,
            type=type.value if type else None,
            status=status.value if status else None,
            metrics=self._merge_metrics(metric, metrics),
        )

        route = routes.SEARCH_COMPETITIONS.compile().with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.Competition])

    async def get_details(
        self,
        id: int,
        *,
        metric: t.Optional[enums.Metric] = None,
        metrics: t.Optional[t.List[enums.Metric]] = None,
    ) -> ResultT[models.CompetitionDetail]:
        """Gets details for the given competition.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.get_details(123)

            result2 = await client.competitions.get_details(
                123, metrics=[wom.Metric.Attack, wom.Metric.Strength]
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        metric : Metric, optional
            The optional metric to view the competition progress in.
            As if this competition was actually for that metric.
            Defaults to `None`.

            !!! warning "Deprecated"

                Use `metrics` instead. If both are passed, they are
                combined.
        metrics : list[Metric], optional
            The optional metrics to view the competition progress in.
            As if this competition was actually for those metrics.
            Defaults to `None`.

        Returns
        -------
        Result
            A result containing the competition details.
        """
        params = self._generate_map(metrics=self._merge_metrics(metric, metrics))
        route = routes.COMPETITION_DETAILS.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, models.CompetitionDetail)

    async def get_top_participant_history(
        self,
        id: int,
        *,
        metric: t.Optional[enums.Metric] = None,
        metrics: t.Optional[t.List[enums.Metric]] = None,
    ) -> ResultT[t.List[models.Top5ProgressResult]]:
        """Gets details for the players with the top 5 progress in the
        competition.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.get_top_participant_history(123)

            result2 = await client.competitions.get_top_participant_history(
                123, metrics=[wom.Metric.Attack]
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        metric : Metric, optional
            The optional metric to view the competition progress in.
            As if this competition was actually for that metric.
            Defaults to `None`.

            !!! warning "Deprecated"

                Use `metrics` instead. If both are passed, they are
                combined.
        metrics : list[Metric], optional
            The optional metrics to view the competition progress in.
            As if this competition was actually for those metrics.
            Defaults to `None`.

        Returns
        -------
        Result
            A result containing the list of top 5
            progress players.
        """
        params = self._generate_map(metrics=self._merge_metrics(metric, metrics))
        route = routes.TOP_PARTICIPANT_HISTORY.compile(id).with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.Top5ProgressResult])

    @t.overload
    async def create_competition(
        self,
        title: str,
        metric: enums.Metric,
        starts_at: datetime,
        ends_at: datetime,
        *,
        metrics: t.Optional[t.List[enums.Metric]] = ...,
        group_id: t.Optional[int] = ...,
        group_verification_code: t.Optional[str] = ...,
        teams: t.Optional[t.List[models.Team]] = ...,
        participants: t.Optional[t.List[str]] = ...,
    ) -> ResultT[models.CreatedCompetitionDetail]: ...

    @t.overload
    async def create_competition(
        self,
        title: str,
        *,
        metrics: t.List[enums.Metric],
        starts_at: datetime,
        ends_at: datetime,
        group_id: t.Optional[int] = ...,
        group_verification_code: t.Optional[str] = ...,
        teams: t.Optional[t.List[models.Team]] = ...,
        participants: t.Optional[t.List[str]] = ...,
    ) -> ResultT[models.CreatedCompetitionDetail]: ...

    async def create_competition(
        self,
        title: str,
        metric: t.Optional[enums.Metric] = None,
        starts_at: t.Optional[datetime] = None,
        ends_at: t.Optional[datetime] = None,
        *,
        metrics: t.Optional[t.List[enums.Metric]] = None,
        group_id: t.Optional[int] = None,
        group_verification_code: t.Optional[str] = None,
        teams: t.Optional[t.List[models.Team]] = None,
        participants: t.Optional[t.List[str]] = None,
    ) -> ResultT[models.CreatedCompetitionDetail]:
        """Creates a new competition.

        !!! info

            The `group_id`, `participants`, and `teams` parameters are
            mutually exclusive.

            - If `group_id` is provided, this method will create a
                classic competition with all members of that group as
                participants.

            - If `participants` is provided and `group_id` isn't, this
                method will create a classic competition with all those
                participants included.

            - If `teams` is provided, this endpoint will create a team
                competition with all those participants included.
                Also accepts `group_id` as a way to link this
                competition to the group.

        ??? example

            ```py
            from datetime import datetime, timedelta
            import wom

            client = wom.Client(...)

            result = await client.competitions.create_competition(
                "Slayer week",
                wom.Metric.Slayer,
                starts_at=datetime.now() + timedelta(days=7),
                ends_at=datetime.now() + timedelta(days=14),
                group_verification_code="111-111-111",
                group_id=123,
            )

            # Multi-metric competitions pass `metrics` instead. All
            # metrics must be of the same type (all skills, all
            # bosses, etc).
            result = await client.competitions.create_competition(
                "Boss week",
                metrics=[wom.Metric.Zulrah, wom.Metric.Vorkath],
                starts_at=datetime.now() + timedelta(days=7),
                ends_at=datetime.now() + timedelta(days=14),
            )
            ```

        Parameters
        ----------
        title : str
            The title of the competition.
        metric : Metric
            The metric the competition should measure. Required unless
            `metrics` is passed.

            !!! warning "Deprecated"

                Use `metrics` instead. If both are passed, they are
                combined.
        starts_at : datetime
            The start date for the competition.
        ends_at : datetime
            The end date for the competition.
        metrics : list[Metric], optional
            The metrics the competition should measure. They must all be
            of the same type, otherwise the API returns an error.
            Required unless `metric` is passed.
        group_id : int, optional
            The optional group id to tie to this competition.
            Defaults to `None`.
        group_verification_code : str, optional
            The optional group verification
            code. Required if group_id is supplied. Defaults to
            `None`.
        participants : list[str], optional
            The optional list of participants to include
            in the competition. Defaults to `None`.
        teams : list[Team], optional
            The optional teams to include in the competition.
            Defaults to `None`.

        Returns
        -------
        Result
            A result containing the newly created
            competition detail.

        Raises
        ------
        TypeError
            If `starts_at` or `ends_at` is not passed.
        """
        if starts_at is None or ends_at is None:
            raise TypeError("create_competition() requires both 'starts_at' and 'ends_at'.")

        payload = self._generate_map(
            title=title,
            teams=teams,
            groupId=group_id,
            participants=participants,
            endsAt=ends_at.isoformat(),
            startsAt=starts_at.isoformat(),
            metrics=self._merge_metrics(metric, metrics),
            groupVerificationCode=group_verification_code,
        )

        route = routes.CREATE_COMPETITION.compile()
        data = await self._http.fetch(route, payload=payload)
        return self._ok_or_err(data, models.CreatedCompetitionDetail)

    async def edit_competition(
        self,
        id: int,
        verification_code: str,
        *,
        title: t.Optional[str] = None,
        metric: t.Optional[enums.Metric] = None,
        metrics: t.Optional[t.List[enums.Metric]] = None,
        starts_at: t.Optional[datetime] = None,
        ends_at: t.Optional[datetime] = None,
        teams: t.Optional[t.List[models.Team]] = None,
        participants: t.Optional[t.List[str]] = None,
    ) -> ResultT[models.Competition]:
        """Edits an existing competition.

        !!! warning

            The teams/participants parameters will completely
            overwrite the existing participants/teams. If you're looking
            to add users, check out [`add_participants()`]
            [wom.CompetitionService.add_participants].

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.edit_competition(
                123, "111-111-111", title="New title"
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        verification_code : str
            The verification code for the
            competition.
        title : str, optional
            The optional updated title of the competition.
            Defaults to `None`.
        metric : Metric, optional
            The optional new metric the competition should measure.
            Defaults to `None`.

            !!! warning "Deprecated"

                Use `metrics` instead. If both are passed, they are
                combined.
        metrics : list[Metric], optional
            The optional new metrics the competition should measure,
            replacing the existing ones. They must all be of the same
            type, otherwise the API returns an error. Defaults to `None`.
        starts_at : datetime, optional
            The optional new start date for the competition.
            Defaults to `None`.
        ends_at : datetime, optional
            The optional new end date for the competition.
            Defaults to `None`.
        participants : list[str], optional
            The optional list of participants to replace
            the existing participants with. Defaults to `None`.
        teams : list[Team], optional
            The optional list of teams to replace the existing
            participants with. Defaults to `None`.

        Returns
        -------
        Result
            A result containing the edited competition
            with participations.
        """
        payload = self._generate_map(
            title=title,
            teams=teams,
            participants=participants,
            startsAt=starts_at.isoformat() if starts_at else None,
            endsAt=ends_at.isoformat() if ends_at else None,
            metrics=self._merge_metrics(metric, metrics),
            verificationCode=verification_code,
        )

        route = routes.EDIT_COMPETITION.compile(id)
        data = await self._http.fetch(route, payload=payload)
        return self._ok_or_err(data, models.Competition)

    async def delete_competition(
        self, id: int, verification_code: str
    ) -> ResultT[models.HttpSuccessResponse]:
        """Deletes a competition.

        !!! warning

            This action can not be reversed.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.delete_competition(
                123, "111-111-111"
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        verification_code : str
            The verification code for the
            competition.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.DELETE_COMPETITION.compile(id)
        payload = self._generate_map(verificationCode=verification_code)
        data = await self._http.fetch(route, payload=payload, message_response=True)
        return self._success_or_err(data)

    async def add_participants(
        self, id: int, verification_code: str, *participants: str
    ) -> ResultT[models.HttpSuccessResponse]:
        """Adds participants to a competition. Only adds valid
        participants, and ignores duplicates.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.add_participants(
                123, "111-111-111", "Jonxslays", "Zezima"
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        verification_code : str
            The verification code for the
            competition.
        *participants : str
            The participants you would like to add.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.ADD_PARTICIPANTS.compile(id)
        payload = self._generate_map(verificationCode=verification_code, participants=participants)
        data = await self._http.fetch(route, payload=payload, message_response=True)
        return self._success_or_err(data)

    async def remove_participants(
        self, id: int, verification_code: str, *participants: str
    ) -> ResultT[models.HttpSuccessResponse]:
        """Removes participants from a competition. Ignores usernames
        that are not competing.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.remove_participants(
                123, "111-111-111", "Jonxslays"
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        verification_code : str
            The verification code for the
            competition.
        *participants : str
            The participants you would like to remove.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.REMOVE_PARTICIPANTS.compile(id)
        payload = self._generate_map(verificationCode=verification_code, participants=participants)
        data = await self._http.fetch(route, payload=payload, message_response=True)
        return self._success_or_err(data)

    async def add_teams(
        self, id: int, verification_code: str, *teams: models.Team
    ) -> ResultT[models.HttpSuccessResponse]:
        """Adds teams to a competition. Ignores duplicates.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.add_teams(
                123,
                "111-111-111",
                wom.Team("Team 1", ["Jonxslays", "lilyuffie88"]),
                wom.Team("Team 2", ["Zezima", "the old nite"]),
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        verification_code : str
            The verification code for the
            competition.
        *teams : Team
            The teams you would like to add.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.ADD_TEAMS.compile(id)
        payload = self._generate_map(verificationCode=verification_code, teams=teams)
        data = await self._http.fetch(route, payload=payload, message_response=True)
        return self._success_or_err(data)

    async def remove_teams(
        self, id: int, verification_code: str, *teams: str
    ) -> ResultT[models.HttpSuccessResponse]:
        """Removes teams from a competition. Ignores teams that don't
        exist.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.remove_teams(
                123, "111-111-111", "Team 1", "Team 2"
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        verification_code : str
            The verification code for the
            competition.
        *teams : str
            The team names you would like to remove.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.REMOVE_TEAMS.compile(id)
        payload = self._generate_map(verificationCode=verification_code, teamNames=teams)
        data = await self._http.fetch(route, payload=payload, message_response=True)
        return self._success_or_err(data)

    async def update_outdated_participants(
        self, id: int, verification_code: str
    ) -> ResultT[models.HttpSuccessResponse]:
        """Attempts to update all outdated competition participants.

        !!! info

            Participants are outdated when either:

            - Competition is ending or started within 6h of now and
                the player hasn't been updated in over 1h.

            - Player hasn't been updated in over 24h.

        !!! warning

            This method adds every outdated participant to an
            "update queue", and the WOM servers try to update players
            in the queue one by one, with a delay in between each. For
            each player in the queue, an attempt is made to update it
            up to 3 times, with 30s in between each attempt.

            Please note that this is dependent on the OSRS hiscores
            functioning correctly, and therefore this method does NOT
            guarantee the players will be updated, it only guarantees
            that an attempt will be made to update them, up to 3 times.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.update_outdated_participants(
                123, "111-111-111"
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        verification_code : str
            The verification code for the
            competition.

        Returns
        -------
        Result
            A result containing the success response
            message.
        """
        route = routes.UPDATE_OUTDATED_PARTICIPANTS.compile(id)
        payload = self._generate_map(verificationCode=verification_code)
        data = await self._http.fetch(route, payload=payload, message_response=True)
        return self._success_or_err(data)

    async def get_details_csv(
        self,
        id: int,
        *,
        metric: t.Optional[enums.Metric] = None,
        metrics: t.Optional[t.List[enums.Metric]] = None,
        team_name: t.Optional[str] = None,
        table_type: t.Optional[models.CompetitionCSVTableType] = None,
    ) -> ResultT[str]:
        """Gets details about the competition in CSV format.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.competitions.get_details_csv(
                123, team_name="Cool team"
            )
            ```

        Parameters
        ----------
        id : int
            The ID of the competition.
        metric : Metric, optional
            The optional metric to view the competition progress in.
            As if this competition was actually for that metric.
            Defaults to `None`.

            !!! warning "Deprecated"

                Use `metrics` instead. If both are passed, they are
                combined.
        metrics : list[Metric], optional
            The optional metrics to view the competition progress in.
            As if this competition was actually for those metrics.
            Defaults to `None`.
        team_name : str, optional
            The optional team name you would like to get details
            for. Defaults to `None`.
        table_type : CompetitionCSVTableType, optional
            The optional table type formatting to apply.
            Defaults to `Participants`.

        Returns
        -------
        Result
            A result containing the CSV string.
        """
        params = self._generate_map(
            metrics=self._merge_metrics(metric, metrics),
            teamName=team_name,
            table=table_type.value if table_type else None,
        )
        route = routes.COMPETITION_DETAILS_CSV.compile(id).with_params(params)
        data = await self._http.fetch(route)

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok(data.decode())
