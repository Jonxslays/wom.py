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

from msgspec.json import Decoder

import wom


def test_init() -> None:
    s = wom.Serializer()

    assert s._decoders == {}  # type: ignore[private-usage]


@mock.patch("wom.serializer.Decoder")
def test_get_decoder(decoder: mock.MagicMock) -> None:
    s = wom.Serializer()

    d1 = s.get_decoder(int)
    d2 = s.get_decoder(int)

    decoder.assert_called_once_with(int)
    assert s._decoders[int] == d1  # type: ignore[private-usage]
    assert id(d1) == id(d2)


@mock.patch("wom.serializer.Serializer.get_decoder")
def test_decode(get_decoder: mock.MagicMock) -> None:
    s = wom.Serializer()
    data = b"[1, 2, 3]"

    get_decoder.return_value = Decoder(t.List[int])
    result = s.decode(data, t.List[int])

    get_decoder.assert_called_once_with(t.List[int])
    assert result == [1, 2, 3]
