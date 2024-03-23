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

"""The group models and enums."""

from __future__ import annotations

__all__ = (
    "ActivityLeader",
    "BossLeader",
    "ComputedMetricLeader",
    "CreatedGroupDetail",
    "Group",
    "GroupActivity",
    "GroupActivityType",
    "GroupDetail",
    "GroupHiscoresActivityItem",
    "GroupHiscoresBossItem",
    "GroupHiscoresComputedMetricItem",
    "GroupHiscoresEntry",
    "GroupHiscoresSkillItem",
    "GroupMemberFragment",
    "GroupMemberGains",
    "GroupMembership",
    "GroupRole",
    "GroupStatistics",
    "Membership",
    "MetricLeader",
    "MetricLeaders",
    "PlayerMembership",
    "SkillLeader",
    "SocialLinks",
)

from .enums import *
from .models import *
