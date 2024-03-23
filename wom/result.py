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

"""This module contains the [`Result`][wom.Result] variants returned by
all [`Client`][wom.Client] calls.

!!! success "Correct usage"

    ```py
    client = wom.Client()

    await client.start()

    result = await client.players.update_player("Jonxslays")

    if result.is_ok:
        print(result.unwrap())
    else:
        print(result.unwrap_err())
    ```

!!! failure "Incorrect usage"

    ```py
    client = wom.Client()

    await client.start()

    result = await client.players.update_player("eeeeeeeeeeeee")

    print(result.unwrap()) # <-- Exception raised
    # Raises UnwrapError because the username was too long
    ```
"""

from __future__ import annotations

import abc
import typing as t

import msgspec

from wom import errors

__all__ = ("Err", "Ok", "Result")

T = t.TypeVar("T")
E = t.TypeVar("E")


class Result(t.Generic[T, E], abc.ABC):
    """Represents a potential [`Ok`][wom.Ok] or [`Err`][wom.Err] result.

    !!! note

        This class cannot be instantiated, only its variants can be.
    """

    __slots__ = ("_error", "_value")

    def __repr__(self) -> str:
        inner = self._value if self.is_ok else self._error  # type: ignore [attr-defined]
        return f"{self.__class__.__name__}({inner})"

    @property
    @abc.abstractmethod
    def is_ok(self) -> bool:
        """`True` if this result is the [`Ok`][wom.Ok] variant."""

    @property
    @abc.abstractmethod
    def is_err(self) -> bool:
        """`True` if this result is the [`Err`][wom.Err] variant."""

    @abc.abstractmethod
    def unwrap(self) -> T:
        """Unwraps the result to produce the value.

        Returns:
            The unwrapped value.

        Raises:
            UnwrapError: If the result was an [`Err`][wom.Err] and not
                [`Ok`][wom.Ok].
        """

    @abc.abstractmethod
    def unwrap_err(self) -> E:
        """Unwraps the result to produce the error.

        Returns:
            The unwrapped error.

        Raises:
            UnwrapError: If the result was [`Ok`][wom.Ok] and not an
                [`Err`][wom.Err].
        """

    @abc.abstractmethod
    def to_dict(self) -> t.Dict[str, t.Any]:
        """Converts the result into a dictionary.

        If this result is [`Ok`][wom.Ok], the "value" property will be set.

        If this result is [`Err`][wom.Err], the "error" property will be set.

        Returns:
            The requested dictionary.
        """


@t.final
class Ok(Result[T, E]):
    """The [`Ok`][wom.Ok] variant of a [`Result`][wom.Result].

    !!! info

        You will receive instances of this class as a result of
        calling [`Client`][wom.Client] methods, and should not have to
        instantiate it yourself.
    """

    __slots__ = ()

    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def is_ok(self) -> bool:
        """Always returns `True` for the [`Ok`][wom.Ok] variant."""
        return True

    @property
    def is_err(self) -> bool:
        """Always returns `False` for the [`Ok`][wom.Ok] variant."""
        return False

    def unwrap(self) -> T:
        """Unwraps the result to produce the value.

        Returns:
            The unwrapped value.
        """
        return self._value

    def unwrap_err(self) -> E:
        """Always throws an exception for the [`Ok`][wom.Ok] variant.

        Raises:
            UnwrapError: Because the result was an [`Ok`][wom.Ok]
                variant.
        """
        actual = self._value.__class__.__name__
        raise errors.UnwrapError(f"Called unwrap error on a non error value of type {actual!r}")

    def to_dict(self) -> t.Dict[str, t.Any]:
        """Converts the result into a dictionary.

        Returns:
            The requested dictionary.
        """
        value = msgspec.to_builtins(self._value)
        return {"value": value, "error": None}


@t.final
class Err(Result[T, E]):
    """The [`Err`][wom.Err] variant of a [`Result`][wom.Result].

    !!! info

        You will receive instances of this class as a result of
        calling [`Client`][wom.Client] methods, and should not have to
        instantiate it yourself.
    """

    __slots__ = ()

    def __init__(self, error: E) -> None:
        self._error = error

    @property
    def is_ok(self) -> bool:
        """Always returns `False` for the [`Err`][wom.Err] variant."""
        return False

    @property
    def is_err(self) -> bool:
        """Always returns `True` for the [`Err`][wom.Err] variant."""
        return True

    def unwrap(self) -> T:
        """Always throws an exception for the [`Err`][wom.Err] variant.

        Raises:
            UnwrapError: Because the result was an [`Err`][wom.Err]
                variant.
        """
        raise errors.UnwrapError(f"Called unwrap on an error value - {self._error}")

    def unwrap_err(self) -> E:
        """Unwraps the result to produce the error.

        Returns:
            The unwrapped error.
        """
        return self._error

    def to_dict(self) -> t.Dict[str, t.Any]:
        """Converts the result into a dictionary.

        Returns:
            The requested dictionary.
        """
        error = msgspec.to_builtins(self._error)
        return {"value": None, "error": error}
