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


@dataclass(slots=True, init=False)
class CompetitionProgressModel(BaseModel):
    """Represents progress in a competition."""

    start: int
    """The starting value for the competition's metric."""
    end: int
    """The ending value for the competition's metric."""
    gained: int
    """The amount of progress gained in the metric."""


@dataclass(slots=True, init=False)
class CompetitionModel(BaseModel):
    id: int
    title: str
    metric: enums.Metric
    type: CompetitionType
    starts_at: datetime
    ends_at: datetime
    group_id: int | None
    score: int
    created_at: datetime
    updated_at: datetime
    participant_count: int
    group: GroupModel | None


@dataclass(slots=True, init=False)
class ParticipationModel(BaseModel):
    player_id: int
    competition_id: int
    team_name: str | None
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True, init=False)
class CompetitionParticipationModel(BaseModel):
    data: ParticipationModel
    player: PlayerModel


@dataclass(slots=True, init=False)
class PlayerParticipationModel(BaseModel):
    data: ParticipationModel
    competition: CompetitionModel


@dataclass(slots=True, init=False)
class PlayerCompetitionStandingModel(BaseModel):
    participation: PlayerParticipationModel
    progress: CompetitionProgressModel
    rank: int


@dataclass(slots=True, init=False)
class CompetitionParticipationDetailModel(BaseModel):
    participation: CompetitionParticipationModel
    progress: CompetitionProgressModel


@dataclass(slots=True, init=False)
class CompetitionDetailModel(BaseModel):
    competition: CompetitionModel
    participations: list[CompetitionParticipationDetailModel]


@dataclass(slots=True, init=False)
class CompetitionHistoryDataPointModel(BaseModel):
    date: datetime
    value: int


@dataclass(slots=True, init=False)
class Top5ProgressResultModel(BaseModel):
    player: PlayerModel
    history: list[CompetitionHistoryDataPointModel]


@dataclass(slots=True)
class TeamModel(BaseModel):
    name: str
    participants: list[str]


@dataclass(slots=True, init=False)
class CompetitionWithParticipationsModel(BaseModel):
    competition: CompetitionModel
    participations: list[CompetitionParticipationModel]
    verification_code: str | None
