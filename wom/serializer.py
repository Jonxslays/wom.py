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

import msgspec

__all__ = ("Serializer",)

StructT = t.TypeVar("StructT", bound=msgspec.Struct)
DecodersT = t.Dict[t.Type[msgspec.Struct], msgspec.json.Decoder[msgspec.Struct]]


class Serializer:
    """Deserializes raw bytes into wom.py model classes."""

    __slots__ = ("_decoders",)

    def __init__(self) -> None:
        self._decoders: DecodersT = {}

    def decode(self, data: bytes, model_type: t.Type[StructT]) -> StructT:
        """Decodes the data into the given model type.

        Args:
            data: The JSON payload as bytes.

        Returns:
            The requested model.
        """
        if not (decoder := self._decoders.get(model_type)):
            decoder = self._decoders[model_type] = msgspec.json.Decoder(model_type)

        return decoder.decode(data)  # pyright: ignore[reportGeneralTypeIssues]
