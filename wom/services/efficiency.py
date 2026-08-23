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

__all__ = ("EfficiencyService",)

T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]

# The rates endpoint returns skill configs for ehp and boss configs for ehb,
# so its result is a union over the two possible element types.
RatesResultT = ResultT[t.Union[t.List[models.SkillMetaConfig], t.List[models.BossMetaConfig]]]


class EfficiencyService(BaseService):
    """Handles endpoints related to efficiency."""

    __slots__ = ()

    async def get_global_leaderboards(
        self,
        metric: enums.Metric = enums.Metric.Ehp,
        *,
        player_type: t.Optional[models.PlayerType] = None,
        player_build: t.Optional[models.PlayerBuild] = None,
        country: t.Optional[models.Country] = None,
        both: bool = False,
    ) -> ResultT[t.List[models.Player]]:
        """Gets the top global efficiency leaderboard.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.efficiency.get_global_leaderboards(
                player_type=wom.PlayerType.Ironman,
            )
            ```

        Parameters
        ----------
        metric : Metric
            The computed metric to filter on. Defaults to `Ehp`,
            must be one of `Ehp` or `Ehb` if supplied.
        player_type : PlayerType, optional
            The optional player type to filter on. Defaults
            to `None`.
        player_build : PlayerBuild, optional
            The optional player build to filter on.
            Defaults to `None`.
        country : Country, optional
            The optional country to filter on. Defaults to
            `None`.
        both : bool
            If `True`, request both ehp and ehb computed metric
            leaderboards. This will override the `metric` if it was
            provided. Defaults to `False`.

        Returns
        -------
        Result
            A result containing a list of the top
            players.
        """
        params = self._generate_map(
            playerType=player_type.value if player_type else None,
            playerBuild=player_build.value if player_build else None,
            country=country.value if country else None,
            metric=(
                metric.value
                if not both
                else "+".join(sorted((m.value for m in enums.ComputedMetrics), reverse=True))
            ),
        )

        route = routes.GLOBAL_EFFICIENCY_LEADERS.compile()
        data = await self._http.fetch(route.with_params(params))
        return self._ok_or_err(data, t.List[models.Player])

    @t.overload
    async def get_rates(
        self,
        algorithm_type: models.EfficiencyAlgorithmType,
        metric: t.Literal[enums.Metric.Ehb],
    ) -> ResultT[t.List[models.BossMetaConfig]]: ...

    @t.overload
    async def get_rates(
        self,
        algorithm_type: models.EfficiencyAlgorithmType,
        metric: t.Literal[enums.Metric.Ehp] = ...,
    ) -> ResultT[t.List[models.SkillMetaConfig]]: ...

    @t.overload
    async def get_rates(
        self,
        algorithm_type: models.EfficiencyAlgorithmType,
        metric: enums.Metric,
    ) -> RatesResultT: ...

    async def get_rates(
        self,
        algorithm_type: models.EfficiencyAlgorithmType,
        metric: enums.Metric = enums.Metric.Ehp,
    ) -> t.Any:
        """Gets the efficiency rates for the given algorithm type and metric.

        ??? example

            ```py
            import wom

            client = wom.Client(...)

            await client.start()

            result = await client.efficiency.get_rates(
                wom.EfficiencyAlgorithmType.Main, wom.Metric.Ehp
            )
            ```

        Parameters
        ----------
        algorithm_type : EfficiencyAlgorithmType
            The efficiency algorithm variant to get rates for.
        metric : Metric
            The computed metric to get rates for. Defaults to `Ehp`,
            must be one of `Ehp` or `Ehb`.

        Returns
        -------
        Result
            A result containing a list of the rate configs. When `metric`
            is statically known, the return type is narrowed by overloads:
            `Ehb` yields a list of
            [`BossMetaConfig`][wom.BossMetaConfig] and any other metric
            (i.e. `Ehp`) yields a list of
            [`SkillMetaConfig`][wom.SkillMetaConfig]. A dynamically typed
            `metric` yields a union of the two.
        """
        params = self._generate_map(type=algorithm_type.value, metric=metric.value)
        route = routes.GLOBAL_EFFICIENCY_RATES.compile().with_params(params)
        data = await self._http.fetch(route)

        # The precise per-metric return types are declared by the overloads
        # above; the implementation is typed loosely because ``Result`` is
        # invariant and cannot unify the two element types under one alias.
        if metric is enums.Metric.Ehb:
            return self._ok_or_err(data, t.List[models.BossMetaConfig])

        return self._ok_or_err(data, t.List[models.SkillMetaConfig])
