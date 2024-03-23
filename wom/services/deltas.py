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

from wom import enums
from wom import models
from wom import result
from wom import routes

from . import BaseService

__all__ = ("DeltaService",)

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]


class DeltaService(BaseService):
    """Handles endpoints related to deltas."""

    __slots__ = ()

    async def get_global_leaderboards(
        self,
        metric: enums.Metric,
        period: enums.Period,
        *,
        player_type: t.Optional[models.PlayerType] = None,
        player_build: t.Optional[models.PlayerBuild] = None,
        country: t.Optional[models.Country] = None,
    ) -> ResultT[t.List[models.DeltaLeaderboardEntry]]:
        """Gets the top global delta leaderboard for a specific
        metric and period.

        Args:
            metric: The metric to filter on.

            period: The period of time to filter on.

        Keyword Args:
            player_type: The optional player type to filter on. Defaults
                to `None`.

            player_build: The optional player build to filter on.
                Defaults to `None`.

            country: The optional country to filter on. Defaults to
                `None`.

        Returns:
            A [`Result`][wom.Result] containing a list of  delta
                leaderboard entries.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.deltas.get_global_leaderboards(
                wom.Metric.Attack,
                wom.Period.Day,
                country=wom.Country.Gb,
            )
            ```
        """
        params = self._generate_map(
            metric=metric.value,
            period=period.value,
            playerType=player_type.value if player_type else None,
            playerBuild=player_build.value if player_build else None,
            country=country.value if country else None,
        )

        route = routes.GLOBAL_DELTA_LEADERS.compile()
        data = await self._http.fetch(route.with_params(params))
        return self._ok_or_err(data, t.List[models.DeltaLeaderboardEntry])
