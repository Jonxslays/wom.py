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

from wom import models
from wom import result
from wom import routes

from . import BaseService

__all__ = ("NameChangeService",)

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]


class NameChangeService(BaseService):
    """Handles endpoints related to name changes."""

    __slots__ = ()

    async def search_name_changes(
        self,
        username: t.Optional[str] = None,
        *,
        status: t.Optional[models.NameChangeStatus] = None,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> ResultT[t.List[models.NameChange]]:
        """Searches for name changes.

        Args:
            username: The optional username to search for.

        Keyword Args:
            status: The optional name change status to filter on.
                Defaults to `None`.

            limit: The optional maximum items to return on this page
                from the API. Defaults to `None`.

            offset: The optional page offset. Defaults to
                `None`.

        Returns:
            A [`Result`][wom.Result] containing a list of name changes.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.names.search_name_changes(
                "Jonxslays", limit=1
            )
            ```
        """
        params = self._generate_map(username=username, status=status, limit=limit, offset=offset)
        route = routes.SEARCH_NAME_CHANGES.compile().with_params(params)
        data = await self._http.fetch(route)
        return self._ok_or_err(data, t.List[models.NameChange])

    async def submit_name_change(self, old_name: str, new_name: str) -> ResultT[models.NameChange]:
        """Submits a new name change.

        Args:
            old_name: The old name for the player.

            new_name: The new name for the player.

        Returns:
            A [`Result`][wom.Result] containing the name change.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.names.submit_name_change(
                "Jonxslays", "I Mahatma I"
            )
            ```
        """
        payload = self._generate_map(oldName=old_name, newName=new_name)
        route = routes.SUBMIT_NAME_CHANGE.compile()
        data = await self._http.fetch(route, payload=payload)
        return self._ok_or_err(data, models.NameChange)
