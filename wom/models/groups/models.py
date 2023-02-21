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
from ..players import Player
from ..players import StatisticsSnapshot
from .enums import GroupRole

__all__ = (
    "GroupDetail",
    "GroupHiscoresActivityItem",
    "GroupHiscoresBossItem",
    "GroupHiscoresComputedMetricItem",
    "GroupHiscoresEntry",
    "GroupHiscoresSkillItem",
    "GroupMemberFragment",
    "GroupMembership",
    "Group",
    "GroupStatistics",
    "Membership",
    "PlayerMembership",
)


@dataclass(init=False)
class Group(BaseModel):
    """Represents a group of players on WOM."""

    __slots__ = (
        "id",
        "name",
        "clan_chat",
        "description",
        "homeworld",
        "verified",
        "score",
        "created_at",
        "updated_at",
        "member_count",
    )

    id: int
    """The unique ID for this group."""
    name: str
    """The groups name."""
    clan_chat: str
    """The clan chat for this group."""
    description: str | None
    """The groups optional description."""
    homeworld: int | None
    """The groups optional homeworld."""
    verified: bool
    """Whether or not this group is verified."""
    score: int
    """The groups score."""
    created_at: datetime
    """The date the group was created."""
    updated_at: datetime
    """The date the group was updated."""
    member_count: int
    """The number of members in the group."""


@dataclass(init=False)
class GroupDetail(BaseModel):
    """Represents details about a group."""

    __slots__ = ("group", "memberships", "verification_code")

    group: Group
    """The [`Group`][wom.models.Group] itself."""
    memberships: list[GroupMembership]
    """A list of [`GroupMemberships`][wom.models.GroupMembership].
    """
    verification_code: str | None
    """The optional verification code for the group.

    !!! note

        This will only be present on group creation.
    """


@dataclass(slots=True, init=False)
class Membership(BaseModel):
    player_id: int
    group_id: int
    role: GroupRole | None
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True, init=False)
class GroupMembership(BaseModel):
    """Represents a players membership in a group."""

    player: Player
    membership: Membership


@dataclass(slots=True, init=False)
class PlayerMembership(BaseModel):
    group: Group
    membership: Membership


@dataclass(slots=True)
class GroupMemberFragment(BaseModel):
    username: str
    role: GroupRole | None = None


@dataclass(slots=True, init=False)
class GroupHiscoresEntry(BaseModel):
    player: Player
    data: (
        GroupHiscoresActivityItem
        | GroupHiscoresBossItem
        | GroupHiscoresSkillItem
        | GroupHiscoresComputedMetricItem
    )


@dataclass(slots=True, init=False)
class GroupHiscoresSkillItem(BaseModel):
    rank: int
    level: int
    experience: int


@dataclass(slots=True, init=False)
class GroupHiscoresBossItem(BaseModel):
    rank: int
    kills: int


@dataclass(slots=True, init=False)
class GroupHiscoresActivityItem(BaseModel):
    rank: int
    score: int


@dataclass(slots=True, init=False)
class GroupHiscoresComputedMetricItem(BaseModel):
    rank: int
    value: int


@dataclass(slots=True, init=False)
class GroupStatistics(BaseModel):
    maxed_combat_count: int
    maxed_total_count: int
    maxed_200ms_count: int
    average_stats: StatisticsSnapshot
