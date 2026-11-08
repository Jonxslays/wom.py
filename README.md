<div align="center">
    <h1>wom.py</h1>
    <a href="https://pypi.org/project/wom.py"><img height="20" alt="Stable version" src="https://img.shields.io/pypi/v/wom.py?label=stable&logo=pypi"></a>
    <a href="https://github.com/Jonxslays/wom.py/blob/master/LICENSE"><img height="20" alt="License" src="https://img.shields.io/pypi/l/wom-py?label=license"></a>
    <a href="https://codecov.io/gh/Jonxslays/wom.py"><img src="https://codecov.io/gh/Jonxslays/wom.py/graph/badge.svg?token=I0WKWO5EC5"></a>
    <br />
    <a href="https://python.org"><img height="20" alt="Python versions" src="https://img.shields.io/pypi/pyversions/wom-py?label=python&logo=python"></a>
</div>

An asynchronous Python wrapper for the
[Wise Old Man API](https://docs.wiseoldman.net/), the open source Old School
RuneScape player progress tracker.

wom.py provides a service method for every public endpoint and a typed model
for every response, so you get autocompletion and type checking for all the
data the API returns.

## Installation

Python 3.10 or greater is required.

```sh
pip install -U wom.py
```

## Quickstart

```py
import asyncio

import wom


async def main() -> None:
    # A user agent with your contact info is strongly encouraged
    client = wom.Client(user_agent="@my_discord_username")

    # Start the client before making any requests
    await client.start()

    try:
        result = await client.players.get_details("Jonxslays")

        # Requests never raise on API errors, they return a Result
        if result.is_ok:
            player = result.unwrap()
            print(f"{player.display_name} has {player.exp:,} total exp")
        else:
            error = result.unwrap_err()
            print(f"Request failed ({error.status}): {error.message}")
    finally:
        # Always close the client when you're done with it
        await client.close()


asyncio.run(main())
```

## Documentation

- [Stable](https://jonxslays.github.io/wom.py/stable/)
- [Development](https://jonxslays.github.io/wom.py/dev/)

New to wom.py? The
[getting started guide](https://jonxslays.github.io/wom.py/stable/getting-started/installation/)
walks through the client, services, and the `Result` type, and the
[guides](https://jonxslays.github.io/wom.py/stable/guides/errors/) cover error
handling, metrics, pagination, competitions, and more.

## Problems

If you're experiencing a problem with the library, please
[open an issue](https://github.com/Jonxslays/wom.py/issues/new/choose) after
first confirming a similar issue was not already created.

## Contributing

wom.py is open to contributions. Check out the
[contributing guide](https://github.com/Jonxslays/wom.py/blob/master/CONTRIBUTING.md)
to learn how.

## What is Wise Old Man

Wise Old Man is an open source Old School RuneScape player progress tracker,
featuring experience tracking, boss killcounts, player achievements, group
competitions, global leaderboards, and a Discord bot.

- [Website](https://wiseoldman.net/)
- [API documentation](https://docs.wiseoldman.net/)
- [GitHub repository](https://wiseoldman.net/github)
- [Discord community](https://wiseoldman.net/discord)
- [Support the developers on Patreon](https://wiseoldman.net/patreon)

## License

wom.py is licensed under the
[MIT License](https://github.com/Jonxslays/wom.py/blob/master/LICENSE).
