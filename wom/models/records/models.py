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

from wom import enums

from ..base import BaseModel
from ..players import PlayerModel

__all__ = ("RecordModel", "RecordLeaderboardEntryModel")


@dataclass(init=False)
class RecordModel(BaseModel):
    """Represents a record held by a player."""

    __slots__ = ("id", "player_id", "period", "metric", "value", "updated_at")

    id: int
    """The unique ID for this record."""
    player_id: int
    """The player ID associated with this record."""
    period: enums.Period
    """The [`Period`][wom.enums.Period] over which this record was
    achieved.
    """
    metric: enums.Metric
    """The metric measured in this record."""
    value: int
    """The records gained value."""
    updated_at: datetime
    """The records creation/modification date."""


@dataclass(init=False)
class RecordLeaderboardEntryModel(BaseModel):
    """Represents a player's record leaderboard entry."""

    __slots__ = ("player", "record")

    player: PlayerModel
    """The [`Player`][wom.models.PlayerModel] holding this leaderboard
    entry.
    """
    record: RecordModel
    """The [`Record`][wom.models.RecordModel] tied to this leaderboard
    entry.
    """
