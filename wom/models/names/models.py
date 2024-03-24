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

from ..base import BaseModel
from .enums import NameChangeReviewReason
from .enums import NameChangeStatus

__all__ = (
    "NameChange",
    "NameChangeReviewContext",
)


class NameChangeReviewContext(BaseModel):
    """The review context for a name change that was not approved."""

    reason: NameChangeReviewReason
    """The reason this name change was denied."""

    # TODO: Setting everything to None here is painful.
    # Determine with Ruben whether we want to keep this
    # public on the name change endpoints and if we do
    # determine how to handle it in a cleaner way.

    negative_gains: t.Optional[t.Dict[enums.Metric, int]] = None
    """The negative gains that were observed, if there were any. Only populated
    when the reason is `NegativeGains`.
    """

    max_hours_diff: t.Optional[int] = None
    """The max number of hours in the transition period. Only populated when
    reason is `TransitionTooLong`.
    """

    hours_diff: t.Optional[int] = None
    """The actual number of hours in the transition period. Only populated when
    reason is `TransitionTooLong` or `ExcessiveGains`.
    """

    ehp_diff: t.Optional[int] = None
    """The number difference between the old and new names ehp. Only populated
    when the reason is `ExcessiveGains`.
    """

    ehb_diff: t.Optional[int] = None
    """The number difference between the old and new names ehb. Only populated
    when the reason is `ExcessiveGains`.
    """

    min_total_level: t.Optional[int] = None
    """The minimum total level allowed for this name change. Only populated
    when the reason is `TotalLevelTooLow`.
    """

    total_level: t.Optional[int] = None
    """The number difference between the old and new names ehb. Only populated
    when the reason is `TotalLevelTooLow`.
    """


class NameChange(BaseModel):
    """Represents a player name change."""

    id: int
    """The unique ID of this name change."""

    player_id: int
    """The player ID associated with the name change."""

    old_name: str
    """The old username of the player."""

    new_name: str
    """The new username of the player."""

    status: NameChangeStatus
    """The [`status`][wom.NameChangeStatus] of the name change."""

    review_context: t.Optional[NameChangeReviewContext]
    """The [review context][wom.NameChangeReviewContext] associated with
    this name change, if it was denied or skipped.
    """

    resolved_at: t.Optional[datetime]
    """The date the name change was approved or denied."""

    updated_at: datetime
    """The date the name change was updated."""

    created_at: datetime
    """The date the name change was created."""
