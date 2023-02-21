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
from ..players import Snapshot
from .enums import NameChangeStatus

__all__ = ("NameChangeData", "NameChangeDetail", "NameChange")


@dataclass(slots=True, init=False)
class NameChange(BaseModel):
    id: int
    player_id: int
    old_name: str
    new_name: str
    status: NameChangeStatus
    resolved_at: datetime | None
    updated_at: datetime
    created_at: datetime


@dataclass(slots=True, init=False)
class NameChangeData(BaseModel):
    is_new_on_hiscores: bool
    is_old_on_hiscores: bool
    is_new_tracked: bool
    has_negative_gains: bool
    time_diff: int
    hours_diff: int
    ehp_diff: int
    ehb_diff: int
    old_stats: Snapshot
    new_stats: Snapshot | None


@dataclass(slots=True, init=False)
class NameChangeDetail(BaseModel):
    name_change: NameChange
    data: NameChangeData | None
