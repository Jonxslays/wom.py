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

from dataclasses import dataclass
from datetime import datetime

from ..base import BaseModel
from ..players import PlayerModel
from ..players import StatisticsSnapshotModel
from .enums import GroupRole

__all__ = (
    "GroupDetailModel",
    "GroupHiscoresActivityItemModel",
    "GroupHiscoresBossItemModel",
    "GroupHiscoresComputedMetricItemModel",
    "GroupHiscoresEntryModel",
    "GroupHiscoresSkillItemModel",
    "GroupMemberFragmentModel",
    "GroupMembershipModel",
    "GroupModel",
    "GroupStatisticsModel",
    "MembershipModel",
    "PlayerMembershipModel",
)


@dataclass(slots=True, init=False)
class GroupModel(BaseModel):
    """Represents a group of players on WOM."""

    id: int
    name: str
    clan_chat: str
    description: str | None
    homeworld: int | None
    verified: bool
    score: int
    created_at: datetime
    updated_at: datetime
    member_count: int


@dataclass(slots=True, init=False)
class GroupDetailModel(BaseModel):
    group: GroupModel
    memberships: list[GroupMembershipModel]
    verification_code: str | None


@dataclass(slots=True, init=False)
class MembershipModel(BaseModel):
    player_id: int
    group_id: int
    role: GroupRole | None
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True, init=False)
class GroupMembershipModel(BaseModel):
    player: PlayerModel
    membership: MembershipModel


@dataclass(slots=True, init=False)
class PlayerMembershipModel(BaseModel):
    group: GroupModel
    membership: MembershipModel


@dataclass(slots=True)
class GroupMemberFragmentModel(BaseModel):
    username: str
    role: GroupRole | None = None


@dataclass(slots=True, init=False)
class GroupHiscoresEntryModel(BaseModel):
    player: PlayerModel
    data: (
        GroupHiscoresActivityItemModel
        | GroupHiscoresBossItemModel
        | GroupHiscoresSkillItemModel
        | GroupHiscoresComputedMetricItemModel
    )


@dataclass(slots=True, init=False)
class GroupHiscoresSkillItemModel(BaseModel):
    rank: int
    level: int
    experience: int


@dataclass(slots=True, init=False)
class GroupHiscoresBossItemModel(BaseModel):
    rank: int
    kills: int


@dataclass(slots=True, init=False)
class GroupHiscoresActivityItemModel(BaseModel):
    rank: int
    score: int


@dataclass(slots=True, init=False)
class GroupHiscoresComputedMetricItemModel(BaseModel):
    rank: int
    value: int


@dataclass(slots=True, init=False)
class GroupStatisticsModel(BaseModel):
    maxed_combat_count: int
    maxed_total_count: int
    maxed_200ms_count: int
    average_stats: StatisticsSnapshotModel
