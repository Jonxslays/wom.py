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

"""This module contains the [`Serializer`][wom.serializer.Serializer]
that is used to parse incoming network data into Python classes.
"""

from __future__ import annotations

import typing as t

from msgspec import Struct
from msgspec.json import Decoder

__all__ = ("Serializer",)

if t.TYPE_CHECKING:  # pragma: no cover
    T = t.TypeVar("T")
    DecodersT = t.Dict[t.Any, Decoder[Struct]]


class Serializer:
    """Deserializes raw bytes into wom.py model classes."""

    __slots__ = ("_decoders",)

    def __init__(self) -> None:
        self._decoders: DecodersT = {}

    def decode(self, data: bytes, model_type: t.Type[T]) -> T:
        """Decodes the data into the given model type.

        Args:
            data: The JSON payload as bytes.

            model_type: The type of model to decode into.

        Returns:
            The requested model.
        """
        return self.get_decoder(model_type).decode(data)

    def get_decoder(self, model_type: t.Type[T]) -> Decoder[T]:
        """Lazily initializes decoders as they are requested and caches them.

        Args:
            model_type: The model type this decoder will target.

        Returns:
            The requested decoder.
        """
        if not (decoder := self._decoders.get(model_type)):
            decoder = self._decoders[model_type] = Decoder(  # pyright: ignore[reportArgumentType]
                model_type
            )

        return decoder  # type: ignore[return-value]
