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

"""This module contains various exceptions used by the project."""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from wom.serializer import SerializerT

__all__ = ("FailedToDeserialize", "UnwrapError", "WomError")

T = t.TypeVar("T")


class WomError(Exception):
    """The base error all wom errors inherit from."""

    __slots__ = ()


class UnwrapError(WomError):
    """Raised when calling [`unwrap()`][wom.Result.unwrap] or
    [`unwrap_err()`][wom.Result.unwrap_err] incorrectly.

    Args:
        message: The error message.
    """

    __slots__ = ()

    def __init__(self, message: str) -> None:
        super().__init__(f"Unwrap failed: {message}")


class FailedToDeserialize(WomError, t.Generic[T]):
    """Raised when a response from the WOM api fails to deserialize.

    Args:
        method: The serializer method that was being called.
        exc: The exception that occurred.
    """

    def __init__(self, method: SerializerT[T], exc: Exception) -> None:
        super().__init__(f"Serializer call to `{method.__name__}` failed\n -> {exc}")
