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

from dataclasses import dataclass
from datetime import datetime

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


@dataclass(init=False)
class CompetitionProgress(BaseModel):
    """Represents progress in a competition."""

    __slots__ = ("start", "end", "gained")

    start: int
    """The starting value for the competition's metric."""
    end: int
    """The ending value for the competition's metric."""
    gained: int
    """The amount of progress gained in the metric."""


@dataclass(init=False)
class Competition(BaseModel):
    """Represents a competition."""

    __slots__ = (
        "id",
        "title",
        "metric",
        "type",
        "starts_at",
        "ends_at",
        "group_id",
        "score",
        "created_at",
        "updated_at",
        "participant_count",
        "group",
    )

    id: int
    """The unique ID of the competition."""
    title: str
    """The title of the competition."""
    metric: enums.Metric
    """The metric being measured."""
    type: CompetitionType
    """The [CompetitionType][wom.models.CompetitionType]."""
    starts_at: datetime
    """The date the competition started at."""
    ends_at: datetime
    """The date the competition ended at."""
    group_id: int | None
    """The optional group id associated with the competition."""
    score: int
    """The competition's score."""
    created_at: datetime
    """The date the competition was created."""
    updated_at: datetime
    """The date the competition was updated."""
    participant_count: int
    """The number of players participating."""
    group: Group | None
    """The [`Group`][wom.models.Group] associated with the
    competition, if there is one.
    """


@dataclass(init=False)
class Participation(BaseModel):
    """Represents participation in a competition."""

    __slots__ = ("player_id", "competition_id", "team_name", "created_at", "updated_at")

    player_id: int
    """The ID of the player associated with this participation."""
    competition_id: int
    """The ID of the competition associated with this participation."""
    team_name: str | None
    """The optional team name associated with this participation."""
    created_at: datetime
    """The date this participation was created."""
    updated_at: datetime
    """The date this participation was updated."""


@dataclass(init=False)
class CompetitionParticipation(BaseModel):
    """Represents a competition participation."""

    __slots__ = ("data", "player")

    data: Participation
    """The [`Participation`][wom.models.Participation] achieved
    in this competition.
    """
    player: Player
    """The [`Player`][wom.models.Player] that participated in this
    competition.
    """


@dataclass(init=False)
class PlayerParticipation(BaseModel):
    """Represents a players participation in a competition."""

    __slots__ = ("data", "competition")

    data: Participation
    """The [`Participation`][wom.models.Participation] the player
    achieved.
    """
    competition: Competition
    """The [`Competition`][wom.models.Competition] that the player
    participated in.
    """


@dataclass(init=False)
class PlayerCompetitionStanding(BaseModel):
    """Represents a players standing in a competition."""

    __slots__ = ("participation", "progress", "rank")

    participation: PlayerParticipation
    """The [`PlayerParticipation`][wom.models.PlayerParticipation]
    achieved by the player.
    """
    progress: CompetitionProgress
    """The [`CompetitionProgress`][wom.models.CompetitionProgress]
    that was made.
    """
    rank: int
    """The rank in the competition standings."""


@dataclass(init=False)
class CompetitionParticipationDetail(BaseModel):
    """Represents competition participation details."""

    __slots__ = ("participation", "progress")

    participation: CompetitionParticipation
    """The [`CompetitionParticipation`]
    [wom.models.CompetitionParticipation] in these details.
    """
    progress: CompetitionProgress
    """The [`CompetitionProgress`][wom.models.CompetitionProgress]
    that was made.
    """


@dataclass(init=False)
class CompetitionDetail(BaseModel):
    """Represents competition details."""

    __slots__ = ("competition", "participations")

    competition: Competition
    """The [`Competition`][wom.models.Competition] that is being
    detailed.
    """
    participations: list[CompetitionParticipationDetail]
    """A list of [`CompetitionParticipationDetail`]
    [wom.models.CompetitionParticipationDetail] participations
    for this competition."""


@dataclass(init=False)
class CompetitionHistoryDataPoint(BaseModel):
    """A competition history data point."""

    __slots__ = ("date", "value")

    date: datetime
    """The date this data point occurred."""
    value: int
    """The value of the data point."""


@dataclass(init=False)
class Top5ProgressResult(BaseModel):
    """A top 5 progress result for a competition."""

    __slots__ = ("player", "history")

    player: Player
    """The [`Player`][wom.models.Player] who made top 5
    progress.
    """
    history: list[CompetitionHistoryDataPoint]
    """A list of [CompetitionHistoryDataPoints]
    [wom.models.CompetitionHistoryDataPoint] making up the history
    of this top 5 progress result.
    """


@dataclass()
class Team(BaseModel):
    """Represents a competition team.

    Args:
        name: The name of the team.

        participants: A list of usernames to include in the team.

    !!! tip

        This is a model class that you will create in order to send
        data to some endpoints.
    """

    __slots__ = ("name", "participants")

    name: str
    """The name of the team."""
    participants: list[str]
    """A list of participant usernames on the team."""


@dataclass(init=False)
class CompetitionWithParticipations(BaseModel):
    """Represents a competition with participations."""

    __slots__ = ("competition", "participations", "verification_code")

    competition: Competition
    """The [`Competition`][wom.models.Competition] itself."""
    participations: list[CompetitionParticipation]
    """A list containing the [`CompetitionParticipations`]
    [wom.models.CompetitionParticipation].
    """
    verification_code: str | None
    """The verification code for the competition.

    !!! note

        Only returned when a competition is created and will be
        `None` otherwise.
    """
