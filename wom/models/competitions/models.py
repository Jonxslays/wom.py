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
from ..groups import GroupModel
from ..players import PlayerModel
from .enums import CompetitionType

__all__ = (
    "CompetitionModel",
    "CompetitionDetailModel",
    "CompetitionHistoryDataPointModel",
    "CompetitionParticipationDetailModel",
    "CompetitionParticipationModel",
    "CompetitionProgressModel",
    "CompetitionWithParticipationsModel",
    "ParticipationModel",
    "PlayerCompetitionStandingModel",
    "PlayerParticipationModel",
    "TeamModel",
    "Top5ProgressResultModel",
)


@dataclass(init=False)
class CompetitionProgressModel(BaseModel):
    """Represents progress in a competition."""

    __slots__ = ("start", "end", "gained")

    start: int
    """The starting value for the competition's metric."""
    end: int
    """The ending value for the competition's metric."""
    gained: int
    """The amount of progress gained in the metric."""


@dataclass(init=False)
class CompetitionModel(BaseModel):
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
    group: GroupModel | None
    """The [`Group`][wom.models.GroupModel] associated with the
    competition, if there is one.
    """


@dataclass(init=False)
class ParticipationModel(BaseModel):
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
class CompetitionParticipationModel(BaseModel):
    """Represents a competition participation."""

    __slots__ = ("data", "player")

    data: ParticipationModel
    """The [`Participation`][wom.models.ParticipationModel] achieved
    in this competition.
    """
    player: PlayerModel
    """The [`Player`][wom.models.PlayerModel] that participated in this
    competition.
    """


@dataclass(init=False)
class PlayerParticipationModel(BaseModel):
    """Represents a players participation in a competition."""

    __slots__ = ("data", "competition")

    data: ParticipationModel
    """The [`Participation`][wom.models.ParticipationModel] the player
    achieved.
    """
    competition: CompetitionModel
    """The [`Competition`][wom.models.CompetitionModel] that the player
    participated in.
    """


@dataclass(init=False)
class PlayerCompetitionStandingModel(BaseModel):
    """Represents a players standing in a competition."""

    __slots__ = ("participation", "progress", "rank")

    participation: PlayerParticipationModel
    """The [`PlayerParticipotion`][wom.models.PlayerParticipationModel]
    achieved by the player.
    """
    progress: CompetitionProgressModel
    """The [`CompetitionProgress`][wom.models.CompetitionProgressModel]
    that was made.
    """
    rank: int
    """The rank in the competition standings."""


@dataclass(init=False)
class CompetitionParticipationDetailModel(BaseModel):
    """Represents competition participation details."""

    __slots__ = ("participation", "progress")

    participation: CompetitionParticipationModel
    """The [`CompetitionParticipation`]
    [wom.models.CompetitionParticipationModel] in these details.
    """
    progress: CompetitionProgressModel
    """The [`CompetitionProgress`][wom.models.CompetitionProgressModel]
    that was made.
    """


@dataclass(init=False)
class CompetitionDetailModel(BaseModel):
    """Represents competition details."""

    __slots__ = ("competition", "participations")

    competition: CompetitionModel
    """The [`Competition`][wom.models.CompetitionModel] that is being
    detailed.
    """
    participations: list[CompetitionParticipationDetailModel]
    """A list of [`CompetitionParticipationDetail`]
    [wom.models.CompetitionParticipationDetailModel] participations
    for this competition."""


@dataclass(init=False)
class CompetitionHistoryDataPointModel(BaseModel):
    """A competition history data point."""

    __slots__ = ("date", "value")

    date: datetime
    """The date this data point occured."""
    value: int
    """The value of the data point."""


@dataclass(init=False)
class Top5ProgressResultModel(BaseModel):
    """A top 5 progress result for a competition."""

    __slots__ = ("player", "history")

    player: PlayerModel
    """The [`Player`][wom.models.PlayerModel] who made top 5
    progress.
    """
    history: list[CompetitionHistoryDataPointModel]
    """A list of [CompetitionHistoryDataPoints]
    [wom.models.CompetitionHistoryDataPointModel] making up the history
    of this top 5 progress result.
    """


@dataclass()
class TeamModel(BaseModel):
    """Represents a competition team.

    !!! tip

        This is one of the model classes that will be instantiated by
        the end user in order to send data to some endpoints.
    """

    __slots__ = ("name", "participants")

    name: str
    """The name of the team."""
    participants: list[str]
    """A list of particpant usernames on the team."""


@dataclass(init=False)
class CompetitionWithParticipationsModel(BaseModel):
    """Represents a competition with participations."""

    __slots__ = ("competition", "participations", "verification_code")

    competition: CompetitionModel
    """The [`Competition`][wom.models.CompetitionModel] itself."""
    participations: list[CompetitionParticipationModel]
    """A list containing the [`CompetitionParticipations`]
    [wom.models.CompetitionParticipationModel].
    """
    verification_code: str | None
    """The verification code for the competition.

    !!! note

        Only returned when a competition is created.
    """
