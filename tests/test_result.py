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

from wom import Err
from wom import Ok
from wom import Result
from wom import UnwrapError


@pytest.fixture()
def mock_ok() -> Ok[str, int]:
    return Ok("OK!")


@pytest.fixture()
def mock_err() -> Err[int, str]:
    return Err("ERR!")


def test_abstract_result_fails_to_instantiate() -> None:
    with pytest.raises(TypeError) as e:
        _ = Result()  # type: ignore

    assert "Can't instantiate abstract class Result" in e.exconly()


def test_repr(mock_ok: Ok[str, int]) -> None:
    assert repr(mock_ok) == "Ok(OK!)"


def test_ok_is_ok(mock_ok: Ok[str, int]) -> None:
    assert mock_ok.is_ok == True
    assert mock_ok.unwrap() == "OK!"


def test_ok_is_err(mock_ok: Ok[str, int]) -> None:
    assert mock_ok.is_err == False
    assert mock_ok.unwrap() == "OK!"


def test_unwrap_err_fails_for_ok(mock_ok: Ok[str, int]) -> None:
    with pytest.raises(UnwrapError) as e:
        mock_ok.unwrap_err()

    assert "Called unwrap error on a non error value of type 'str'" in e.exconly()


def test_ok_to_dict(mock_ok: Ok[str, int]) -> None:
    data = mock_ok.to_dict()
    assert data == {"value": "OK!", "error": None}


def test_err_is_err(mock_err: Err[int, str]) -> None:
    assert mock_err.is_err == True
    assert mock_err.unwrap_err() == "ERR!"


def test_err_is_ok(mock_err: Err[int, str]) -> None:
    assert mock_err.is_ok == False
    assert mock_err.unwrap_err() == "ERR!"


def test_unwrap_fails_for_err(mock_err: Err[int, str]) -> None:
    with pytest.raises(UnwrapError) as e:
        mock_err.unwrap()

    assert "Called unwrap on an error value - ERR!" in e.exconly()


def test_err_to_dict(mock_err: Err[str, int]) -> None:
    data = mock_err.to_dict()
    assert data == {"value": None, "error": "ERR!"}
