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

import pytest

from wom import enums


def test_from_str() -> None:
    skill = enums.Skills.from_str("thieving")
    assert skill is enums.Skills.Thieving
    assert skill.value == "thieving"


def test_from_str_none() -> None:
    with pytest.raises(ValueError) as e:
        _ = enums.Period.from_str(None)  # type: ignore

    assert e.exconly() == "ValueError: None is not a valid Period"


def test_from_str_invalid() -> None:
    with pytest.raises(ValueError) as e:
        _ = enums.Period.from_str("fake")  # type: ignore

    assert e.exconly() == "ValueError: 'fake' is not a valid Period"


def test_from_str_maybe() -> None:
    period = enums.Period.from_str_maybe("day")
    assert period is enums.Period.Day
    assert period.value == "day"


def test_from_str_maybe_invalid() -> None:
    period = enums.Period.from_str_maybe("lol")
    assert period is None


def test_from_str_maybe_none() -> None:
    period = enums.Period.from_str_maybe(None)  # type: ignore
    assert period is None


def test_str() -> None:
    period = enums.Period.Month
    assert str(period) == "month"


def test_metric_from_str() -> None:
    metric = enums.Metric.from_str("bounty_hunter_hunter")
    assert metric is enums.Activities.BountyHunterHunter
    assert metric.value == "bounty_hunter_hunter"


def test_metric_child_from_str() -> None:
    metric = enums.Activities.from_str("bounty_hunter_hunter")
    assert metric is enums.Activities.BountyHunterHunter
    assert metric.value == "bounty_hunter_hunter"


def test_metric_from_str_invalid() -> None:
    with pytest.raises(RuntimeError) as e:
        _ = enums.Metric.from_str("hmmm")

    assert e.exconly() == "RuntimeError: No <enum 'Metric'> variant for 'hmmm'."


def test_metric_from_str_none() -> None:
    with pytest.raises(RuntimeError) as e:
        _ = enums.Metric.from_str(None)  # type: ignore

    assert e.exconly() == "RuntimeError: No <enum 'Metric'> variant for None."


def test_metric_from_str_maybe() -> None:
    metric = enums.Metric.from_str_maybe("attack")
    assert metric is enums.Skills.Attack
    assert metric.value == "attack"


def test_metric_child_from_str_maybe() -> None:
    metric = enums.ComputedMetrics.from_str_maybe("ehp")
    assert metric is enums.ComputedMetrics.Ehp
    assert metric.value == "ehp"


def test_metric_from_str_maybe_invalid() -> None:
    metric = enums.Metric.from_str_maybe("fake")
    assert metric is None


def test_metric_from_str_maybe_none() -> None:
    metric = enums.Metric.from_str_maybe(None)  # type: ignore
    assert metric is None
