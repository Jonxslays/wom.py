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

import abc
import typing as t

if t.TYPE_CHECKING:
    from wom import serializer

    from . import HttpService

__all__ = ("BaseService",)


class BaseService(abc.ABC):
    """The base service all API services inherit from.

    Args:
        http_service: The http service to use for requests.

        serializer: The serializer to use for handling incoming
            JSON data from the API.
    """

    __slots__ = ("_dict", "_list", "_http", "_serializer")

    def __init__(self, http_service: HttpService, serializer: serializer.Serializer) -> None:
        self._http = http_service
        self._serializer = serializer
        self._dict = t.Dict[str, t.Any]
        self._list = t.List[t.Dict[str, t.Any]]

    def _generate_map(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        return {k: v for k, v in kwargs.items() if v is not None}
