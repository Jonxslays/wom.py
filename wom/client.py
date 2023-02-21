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

"""This module houses the wom.py [`Client`][wom.Client].

Services related to different WOM endpoints are available for use.
All functionality is encompassed in these service methods.
"""

from __future__ import annotations

import typing as t

from wom import serializer
from wom import services

__all__ = ("Client",)

ServiceT = t.TypeVar("ServiceT")


class Client:
    """A client used for interacting with the Wise Old Man API.

    Args:
        api_key: The optional WOM api key to use with requests.

    Keyword Args:
        user_agent: The optional user agent to use with requests.

            If none is provided a library default will be used.

        api_base_url: The optional alternate api base url to use

            for requests. Useful for development against a local

            version of the WOM api.
    """

    __slots__ = (
        "_competitions",
        "_deltas",
        "_efficiency",
        "_groups",
        "_http",
        "_names",
        "_players",
        "_records",
        "_serializer",
    )

    def __init__(
        self,
        api_key: str | None = None,
        *,
        user_agent: str | None = None,
        api_base_url: str | None = None,
    ) -> None:
        self._serializer = serializer.Serializer()
        self._http = services.HttpService(api_key, user_agent, api_base_url)
        self.__init_core_services()

    @property
    def competitions(self) -> services.CompetitionService:
        """The [`CompetitionService`][wom.services.CompetitionService]
        used to make competition related requests.
        """
        return self._competitions

    @property
    def deltas(self) -> services.DeltaService:
        """The [`DeltaService`][wom.services.DeltaService]
        used to make delta (increment) related requests.
        """
        return self._deltas

    @property
    def efficiency(self) -> services.EfficiencyService:
        """The [`EfficiencyService`][wom.services.EfficiencyService]
        used to make efficiency related requests.
        """
        return self._efficiency

    @property
    def groups(self) -> services.GroupService:
        """Used to make group related requests."""
        return self._groups

    @property
    def names(self) -> services.NameChangeService:
        """Used to make name change related requests."""
        return self._names

    @property
    def players(self) -> services.PlayerService:
        """Used to make player related requests."""
        return self._players

    @property
    def records(self) -> services.RecordService:
        """Used to make record related requests."""
        return self._records

    def __init_service(self, service: t.Type[ServiceT]) -> ServiceT:
        if not issubclass(service, services.BaseService):
            raise TypeError(f"{service.__name__!r} can not be initialized as a service.")

        return service(self._http, self._serializer)  # type: ignore[return-value]

    def __init_core_services(self) -> None:
        self._deltas = self.__init_service(services.DeltaService)
        self._groups = self.__init_service(services.GroupService)
        self._players = self.__init_service(services.PlayerService)
        self._records = self.__init_service(services.RecordService)
        self._names = self.__init_service(services.NameChangeService)
        self._efficiency = self.__init_service(services.EfficiencyService)
        self._competitions = self.__init_service(services.CompetitionService)

    def set_api_key(self, api_key: str) -> None:
        self._http.set_api_key(api_key)

    def set_user_agent(self, user_agent: str) -> None:
        self._http.set_user_agent(user_agent)

    def set_api_base_url(self, api_base_url: str) -> None:
        self._http.set_base_url(api_base_url)

    async def close(self) -> None:
        await self._http.close()
