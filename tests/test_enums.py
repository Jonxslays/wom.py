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

from unittest import mock

import wom


def test_str() -> None:
    attack = wom.Metric.Attack
    zulrah = wom.Metric.Zulrah
    lms = wom.Metric.LastManStanding
    ehp = wom.Metric.Ehp

    assert str(attack) == "attack"
    assert str(zulrah) == "zulrah"
    assert str(lms) == "last_man_standing"
    assert str(ehp) == "ehp"


def test_eq() -> None:
    assert wom.Metric.Slayer == wom.Metric.Slayer
    assert wom.Metric.BarrowsChests == "barrows_chests"
    assert wom.Metric.Ehb != 123


def test_hash() -> None:
    metric = wom.Metric.Agility
    assert hash(metric) == hash("agility")


@mock.patch("wom.enums.random.choice")
def test_at_random(choice: mock.MagicMock) -> None:
    _ = wom.Metric.at_random()
    choice.assert_called_once_with(tuple(wom.Metric))


def test_base_enum_missing() -> None:
    """A test for the BaseEnum.__missing__ method."""
    assert wom.Metric["new_fake_metric"] == wom.Metric.Unknown
    assert wom.Metric["another_fake_metric"] == wom.Metric.Unknown
    assert wom.Metric.Unknown.value == "unknown"
    assert wom.Metric.Unknown != wom.Metric.Vardorvis
    assert wom.Metric.Attack.value == "attack"
