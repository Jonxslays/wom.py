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
from unittest import mock

import wom
from wom import BaseService


def test_init() -> None:
    http_service = mock.Mock()
    serializer = mock.Mock()

    service = BaseService(http_service, serializer)

    assert service._http is http_service  # type: ignore
    assert service._serializer is serializer  # type: ignore


def test_generate_map() -> None:
    service = BaseService(mock.Mock(), mock.Mock())

    expected = {"test": 1, "other": 2}
    result = service._generate_map(test=1, other=2, nothing=None)  # type: ignore

    assert result == expected


@mock.patch("wom.services.base.serializer.Serializer.decode")
def test_ok(decode: mock.Mock) -> None:
    decode.return_value = None
    service = BaseService(mock.Mock(), wom.Serializer())

    result = service._ok(b"", t.Type[None])  # pyright: ignore[reportPrivateUsage]

    decode.assert_called_once_with(b"", t.Type[None])
    assert isinstance(result, wom.Ok)
    assert result.unwrap() == None


@mock.patch("wom.services.base.BaseService._ok")
def test_ok_or_err_ok(_ok: mock.Mock) -> None:
    _ok.return_value = wom.Ok(123)
    service = BaseService(mock.Mock(), mock.Mock())

    result = service._ok_or_err(b"123", int)  # pyright: ignore[reportPrivateUsage]

    _ok.assert_called_once_with(b"123", int)
    assert isinstance(result, wom.Ok)
    assert result.unwrap() == 123


@mock.patch("wom.services.base.BaseService._ok")
def test_ok_or_err_err(_ok: mock.Mock) -> None:
    service = BaseService(mock.Mock(), mock.Mock())

    result = service._ok_or_err(  # pyright: ignore[reportPrivateUsage]
        wom.HttpErrorResponse("test", 69), int
    )

    _ok.assert_not_called()
    assert isinstance(result, wom.Err)
    assert isinstance(result.unwrap_err(), wom.HttpErrorResponse)
    assert result.unwrap_err().message == "test"
    assert result.unwrap_err().status == 69


@mock.patch("wom.services.base.serializer.Serializer.decode")
def test_success_or_err_bytes_err(decode: mock.Mock) -> None:
    decode.return_value = None
    service = BaseService(mock.Mock(), wom.Serializer())

    result = service._success_or_err(b"")  # pyright: ignore[reportPrivateUsage]

    decode.assert_called_once_with(b"", wom.HttpErrorResponse)
    assert isinstance(result, wom.Err)
    assert result.unwrap_err() == None


@mock.patch("wom.services.base.serializer.Serializer.decode")
def test_success_or_err_predicate_err(decode: mock.Mock) -> None:
    service = BaseService(mock.Mock(), wom.Serializer())
    data = wom.HttpErrorResponse("FAILED", 100)

    result = service._success_or_err(data)  # pyright: ignore[reportPrivateUsage]

    decode.assert_not_called()
    assert isinstance(result, wom.Err)
    assert result.unwrap_err().message == "FAILED"
    assert result.unwrap_err().status == 100


@mock.patch("wom.services.base.serializer.Serializer.decode")
def test_success_or_err_predicate_ok(decode: mock.Mock) -> None:
    service = BaseService(mock.Mock(), wom.Serializer())
    data = wom.HttpErrorResponse("Success", 10)

    result = service._success_or_err(data)  # pyright: ignore[reportPrivateUsage]

    decode.assert_not_called()
    assert isinstance(result, wom.Ok)
    assert result.unwrap().message == "Success"
    assert result.unwrap().status == 10


@mock.patch("wom.services.base.serializer.Serializer.decode")
def test_success_or_err_custom_predicate_ok(decode: mock.Mock) -> None:
    service = BaseService(mock.Mock(), wom.Serializer())
    predicate = mock.Mock()
    predicate.return_value = True
    data = wom.HttpErrorResponse("Success", 10)

    result = service._success_or_err(  # pyright: ignore[reportPrivateUsage]
        data, predicate=predicate
    )

    decode.assert_not_called()
    predicate.assert_called_once_with("Success")
    assert isinstance(result, wom.Ok)
    assert result.unwrap().message == "Success"
    assert result.unwrap().status == 10


@mock.patch("wom.services.base.serializer.Serializer.decode")
def test_success_or_err_custom_predicate_err(decode: mock.Mock) -> None:
    service = BaseService(mock.Mock(), wom.Serializer())
    predicate = mock.Mock()
    predicate.return_value = False
    data = wom.HttpErrorResponse("lol", 99)

    result = service._success_or_err(  # pyright: ignore[reportPrivateUsage]
        data, predicate=predicate
    )

    decode.assert_not_called()
    predicate.assert_called_once_with("lol")
    assert isinstance(result, wom.Err)
    assert result.unwrap_err().message == "lol"
    assert result.unwrap_err().status == 99
