# Long-running applications

Scripts can create a client, make a few requests, and close it. Long-running
applications such as Discord bots, web servers, and schedulers should instead
create **one** client when they start up, share it everywhere, and close it
when they shut down.

## Why one client

Each [`Client`][wom.Client] owns an `aiohttp.ClientSession`, which keeps a pool
of open connections to the WOM API. Reusing a single client lets every request
share that pool. Creating a client per request opens new connections every
time, is slower, and makes it easy to forget a [`close`][wom.Client.close].

The client is safe to share between concurrent tasks, so there is no need for a
client per task, per user, or per command.

## The general pattern

1. Create the client once, at startup.
2. `await client.start()` before handling any work.
3. Pass the client (or the object that holds it) to whatever needs it.
4. `await client.close()` on shutdown, even if the app is exiting because of an
   error.

An async context manager is a tidy way to guarantee the last step:

```py
import contextlib
import typing as t

import wom


@contextlib.asynccontextmanager
async def wom_client() -> t.AsyncIterator[wom.Client]:
    client = wom.Client(user_agent="@my_discord_username")
    await client.start()

    try:
        yield client
    finally:
        await client.close()


async def main() -> None:
    async with wom_client() as client:
        await run_my_app(client)
```

## Discord bots

With [discord.py](https://discordpy.readthedocs.io/), start the client in
`setup_hook` and close it in `close`, so it lives exactly as long as the bot:

```py
import os

import discord
import wom
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.default())
        self.wom = wom.Client(os.environ.get("WOM_API_KEY"), user_agent="@my_discord_username")

    async def setup_hook(self) -> None:
        await self.wom.start()

    async def close(self) -> None:
        await self.wom.close()
        await super().close()


bot = Bot()


@bot.command()
async def ehp(ctx: commands.Context[Bot], username: str) -> None:
    result = await ctx.bot.wom.players.get_details(username)

    if result.is_err:
        await ctx.send(f"Couldn't find {username}: {result.unwrap_err().message}")
        return

    player = result.unwrap()
    await ctx.send(f"{player.display_name} has {player.ehp:,.2f} EHP")


bot.run(os.environ["DISCORD_TOKEN"])
```

Other frameworks have equivalent startup and shutdown hooks. For example, in
FastAPI use a `lifespan` handler, and in aiohttp web apps use
`cleanup_ctx`.

## Concurrent requests

Because the client is shared, you can fan out requests with `asyncio.gather`
or task groups. Keep the [rate limits](requests.md#rate-limits) in mind and
bound how many requests run at once with a semaphore, as shown in
[requests and rate limits](requests.md#rate-limits).

## Changing settings at runtime

Long-running apps sometimes need to rotate an API key or switch environments
without restarting. The client's setters apply to every request made after
they're called:

- [`set_api_key`][wom.Client.set_api_key] /
  [`unset_api_key`][wom.Client.unset_api_key]
- [`set_user_agent`][wom.Client.set_user_agent]
- [`set_api_base_url`][wom.Client.set_api_base_url]
