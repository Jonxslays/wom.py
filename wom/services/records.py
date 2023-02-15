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
from wom import serializer

from . import BaseService

if t.TYPE_CHECKING:
    from . import HttpService

__all__ = ("RecordService",)


class RecordService(BaseService):
    __slots__ = ("_http", "_serializer")

    def __init__(self, http_service: HttpService, serializer: serializer.Serializer) -> None:
        self._http = http_service
        self._serializer = serializer

    async def get_global_record_leaderboards(
        self,
        metric: enums.Metric,
        period: enums.Period,
        *,
        player_type: models.PlayerType | None = None,
        player_build: models.PlayerBuild | None = None,
        country: models.Country | None = None,
    ) -> result.Result[list[models.RecordLeaderboardEntryModel], models.HttpErrorResponse]:
        params = self._generate_params(
            metric=metric.value,
            period=period.value,
            playerType=player_type.value if player_type else None,
            playerBuild=player_build.value if player_build else None,
            country=country.value if country else None,
        )

        route = routes.GLOBAL_RECORD_LEADERS.compile().with_params(params)
        data = await self._http.fetch(route, list[dict[str, t.Any]])

        if isinstance(data, models.HttpErrorResponse):
            return result.Err(data)

        return result.Ok([self._serializer.deserialize_record_leaderboard_entry(r) for r in data])
