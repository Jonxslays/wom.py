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

from wom import models
from wom import result
from wom import serializer

if t.TYPE_CHECKING:  # pragma: no cover
    from . import HttpService

    T = t.TypeVar("T")
    ResultT = result.Result[T, models.HttpErrorResponse]

__all__ = ("BaseService",)


class BaseService(abc.ABC):
    """The base service all API services inherit from.

    Args:
        http_service: The http service to use for requests.

        serializer: The serializer to use for handling incoming
            JSON data from the API.
    """

    __slots__ = ("_http", "_serializer")

    def __init__(self, http_service: HttpService, serializer: serializer.Serializer) -> None:
        self._http = http_service
        self._serializer = serializer

    def _generate_map(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        return {k: v for k, v in kwargs.items() if v is not None}

    def _ok(self, data: bytes, model_type: t.Type[T]) -> ResultT[T]:
        return result.Ok(self._serializer.decode(data, model_type))

    def _ok_or_err(
        self, data: t.Union[bytes, models.HttpErrorResponse], model_type: t.Type[T]
    ) -> ResultT[T]:
        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return self._ok(data, model_type)

    def _success_or_err(
        self,
        data: t.Union[bytes, models.HttpErrorResponse],
        *,
        predicate: t.Optional[t.Callable[[str], bool]] = None,
    ) -> ResultT[models.HttpSuccessResponse]:
        if isinstance(data, bytes):
            err = self._serializer.decode(data, models.HttpErrorResponse)
            return result.Err(err)

        predicate = predicate or (lambda m: m.startswith("Success"))

        if not predicate(data.message):
            return result.Err(data)

        return result.Ok(models.HttpSuccessResponse(data.message, data.status))
