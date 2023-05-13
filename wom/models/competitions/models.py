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

"""Competition related models."""

from __future__ import annotations

import typing as t
from datetime import datetime

import attrs

from wom import enums

from ..base import BaseModel
from ..groups import Group
from ..players import Player
from .enums import CompetitionType

__all__ = (
    "Competition",
    "CompetitionDetail",
    "CompetitionHistoryDataPoint",
    "CompetitionParticipationDetail",
    "CompetitionParticipation",
    "CompetitionProgress",
    "CompetitionWithParticipations",
    "Participation",
    "PlayerCompetitionStanding",
    "PlayerParticipation",
    "Team",
    "Top5ProgressResult",
)


@attrs.define(init=False)
class CompetitionProgress(BaseModel):
    """Represents progress in a competition."""

    start: int
    """The starting value for the competition's metric."""

    end: int
    """The ending value for the competition's metric."""

    gained: int
    """The amount of progress gained in the metric."""


@attrs.define(init=False)
class Competition(BaseModel):
    """Represents a competition."""

    id: int
    """The unique ID of the competition."""

    title: str
    """The title of the competition."""

    metric: enums.Metric
    """The metric being measured."""

    type: CompetitionType
    """The [CompetitionType][wom.CompetitionType]."""

    starts_at: datetime
    """The date the competition started at."""

    ends_at: datetime
    """The date the competition ended at."""

    group_id: t.Optional[int]
    """The optional group id associated with the competition."""

    score: int
    """The competition's score."""

    created_at: datetime
    """The date the competition was created."""

    updated_at: datetime
    """The date the competition was updated."""

    participant_count: int
    """The number of players participating."""

    group: t.Optional[Group]
    """The [`Group`][wom.Group] associated with the competition, if
    there is one.
    """


@attrs.define(init=False)
class Participation(BaseModel):
    """Represents participation in a competition."""

    player_id: int
    """The ID of the player associated with this participation."""

    competition_id: int
    """The ID of the competition associated with this participation."""

    team_name: t.Optional[str]
    """The optional team name associated with this participation."""

    created_at: datetime
    """The date this participation was created."""

    updated_at: datetime
    """The date this participation was updated."""


@attrs.define(init=False)
class CompetitionParticipation(BaseModel):
    """Represents a competition participation."""

    data: Participation
    """The [`Participation`][wom.models.Participation] achieved in this
    competition.
    """

    player: Player
    """The [`Player`][wom.Player] that participated in this competition.
    """


@attrs.define(init=False)
class PlayerParticipation(BaseModel):
    """Represents a players participation in a competition."""

    data: Participation
    """The [`Participation`][wom.Participation] the player achieved."""

    competition: Competition
    """The [`Competition`][wom.Competition] that the player participated
    in.
    """


@attrs.define(init=False)
class PlayerCompetitionStanding(BaseModel):
    """Represents a players standing in a competition."""

    participation: PlayerParticipation
    """The [`PlayerParticipation`][wom.PlayerParticipation] achieved by
    the player.
    """

    progress: CompetitionProgress
    """The [`CompetitionProgress`][wom.CompetitionProgress] that was
    made.
    """

    rank: int
    """The rank in the competition standings."""


@attrs.define(init=False)
class CompetitionParticipationDetail(BaseModel):
    """Represents competition participation details."""

    participation: CompetitionParticipation
    """The [`CompetitionParticipation`][wom.CompetitionParticipation]
    in these details.
    """

    progress: CompetitionProgress
    """The [`CompetitionProgress`][wom.CompetitionProgress] that was
    made.
    """


@attrs.define(init=False)
class CompetitionDetail(BaseModel):
    """Represents competition details."""

    competition: Competition
    """The [`Competition`][wom.Competition] that is being detailed."""

    participations: t.List[CompetitionParticipationDetail]
    """A list of [`CompetitionParticipationDetail`]
    [wom.CompetitionParticipationDetail] participations for this
    competition.
    """


@attrs.define(init=False)
class CompetitionHistoryDataPoint(BaseModel):
    """A competition history data point."""

    date: datetime
    """The date this data point occurred."""

    value: int
    """The value of the data point."""


@attrs.define(init=False)
class Top5ProgressResult(BaseModel):
    """A top 5 progress result for a competition."""

    player: Player
    """The [`Player`][wom.Player] who made top 5 progress."""

    history: t.List[CompetitionHistoryDataPoint]
    """A list of [CompetitionHistoryDataPoints]
    [wom.CompetitionHistoryDataPoint] making up the history
    of this top 5 progress result.
    """


@attrs.define
class Team(BaseModel):
    """Represents a competition team.

    Args:
        name: The name of the team.

        participants: A list of usernames to include in the
            team.

    !!! tip

        This is a model class that you will create in order to send
        data to some endpoints.
    """

    def __init__(self, name: str, participants: t.List[str]) -> None:
        self.name = name
        self.participants = participants

    name: str
    """The name of the team."""

    participants: t.List[str]
    """A list of participant usernames on the team."""


@attrs.define(init=False)
class CompetitionWithParticipations(BaseModel):
    """Represents a competition with participations."""

    competition: Competition
    """The [`Competition`][wom.Competition] itself."""

    participations: t.List[CompetitionParticipation]
    """A list containing the [`CompetitionParticipations`]
    [wom.CompetitionParticipation].
    """

    verification_code: t.Optional[str]
    """The verification code for the competition.

    !!! note

        Only returned when a competition is created and will be
        `None` otherwise.
    """
