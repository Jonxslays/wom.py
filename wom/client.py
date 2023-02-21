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

Services related to different WOM endpoints are available for use on
the client. All functionality is encompassed in these service methods.

!!! example

    ```py
    from wom import Client

    client = Client(user_agent="@your_discord_handle#1234")

    result = await client.players.search_players("Jonxslays")

    if result.is_ok:
        print(result.unwrap())
    else:
        print(f"ERROR: {result.unwrap_err()}")
    ```

!!! tip

    All the available client services can be found [`here`][wom.services]
"""

from __future__ import annotations

import typing as t

from wom import serializer
from wom import services

__all__ = ("Client",)

ServiceT = t.TypeVar("ServiceT")


class Client:
    """An asynchronous client used for interacting with the
    Wise Old Man API.

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
        """The [`GroupService`][wom.services.GroupService] used to make
        group related requests.
        """
        return self._groups

    @property
    def names(self) -> services.NameChangeService:
        """The [`NameChangeService`][wom.services.NameChangeService]
        used to make name change related requests.
        """
        return self._names

    @property
    def players(self) -> services.PlayerService:
        """The [`PlayerService`][wom.services.PlayerService] used to
        make player related requests.
        """
        return self._players

    @property
    def records(self) -> services.RecordService:
        """The [`RecordService`][wom.services.RecordService] used to
        make record related requests.
        """
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
        """Sets the api key used by the http service.

        Args:
            api_key: The new api key to use.
        """
        self._http.set_api_key(api_key)

    def set_user_agent(self, user_agent: str) -> None:
        """Sets the user agent used by the http service.

        Args:
            user_agent: The new user agent to use.
        """
        self._http.set_user_agent(user_agent)

    def set_api_base_url(self, base_url: str) -> None:
        """Sets the api base url used by the http service.

        Args:
            base_url: The new base url to use.
        """
        self._http.set_base_url(base_url)

    async def close(self) -> None:
        """Closes the existing client session, if it's still open.

        !!! warning

            If this is not called before your program terminates,
            you will receive an error in your console.
        """
        await self._http.close()
