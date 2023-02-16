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

from wom import serializer
from wom import services

__all__ = ("Client",)

ServiceT = t.TypeVar("ServiceT")


class Client:
    __slots__ = (
        "_competitions",
        "_deltas",
        "_efficiency",
        "_groups",
        "_http",
        "_name_changes",
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
        return self._competitions

    @property
    def deltas(self) -> services.DeltaService:
        return self._deltas

    @property
    def efficiency(self) -> services.EfficiencyService:
        return self._efficiency

    @property
    def groups(self) -> services.GroupService:
        return self._groups

    @property
    def name_changes(self) -> services.NameChangeService:
        return self._name_changes

    @property
    def players(self) -> services.PlayerService:
        return self._players

    @property
    def records(self) -> services.RecordService:
        return self._records

    def __init_service(self, service: t.Type[ServiceT]) -> ServiceT:
        if not issubclass(service, services.BaseService):
            raise TypeError(f"{service.__name__!r} can not be initialized as a service.")

        return service(self._http, self._serializer)  # type: ignore[call-arg]

    def __init_core_services(self) -> None:
        self._deltas = self.__init_service(services.DeltaService)
        self._groups = self.__init_service(services.GroupService)
        self._players = self.__init_service(services.PlayerService)
        self._records = self.__init_service(services.RecordService)
        self._efficiency = self.__init_service(services.EfficiencyService)
        self._name_changes = self.__init_service(services.NameChangeService)

    def set_api_key(self, api_key: str) -> None:
        self._http.set_api_key(api_key)

    def set_user_agent(self, user_agent: str) -> None:
        self._http.set_user_agent(user_agent)

    def set_api_base_url(self, api_base_url: str) -> None:
        self._http.set_base_url(api_base_url)

    async def close(self) -> None:
        await self._http.close()
