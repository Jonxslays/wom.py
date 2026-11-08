# Requests and rate limits

This guide covers the parts of making requests that apply to every service:
identifying yourself, staying inside the rate limits, and paginating through
large results.

## User agents

Always set a user agent that tells the WOM team how to reach you, such as your
Discord username or a GitHub link:

```py
client = wom.Client(user_agent="@my_discord_username")
```

When passed to the constructor, wom.py prefixes it with the library version, so
the API sees something like `(wom.py v3.4.0) - @my_discord_username`. A user
agent does not raise your rate limits, but the WOM team may IP ban clients they
have no way of contacting, so don't skip it.

## API keys

Rate limits are applied per IP address, or per API key if you send one.
Registering for a key gives you much higher limits. You can request one in the
`#support` channel of the [WOM Discord](https://wiseoldman.net/discord).

```py
import os

client = wom.Client(os.environ["WOM_API_KEY"], user_agent="@my_discord_username")
```

!!! warning

    Treat your API key like a password. Load it from an environment variable
    or a secrets file rather than committing it to source control.

You can also change the key on an existing client with
[`set_api_key`][wom.Client.set_api_key] and remove it with
[`unset_api_key`][wom.Client.unset_api_key].

## Rate limits

At the time of writing, the API allows the following number of requests. Check
the [WOM API docs](https://docs.wiseoldman.net/#rate-limits--api-keys) for the
current numbers.

| Window | Without API key | With API key |
| --- | --- | --- |
| Per minute | 20 | 100 |
| Per hour | 500 | No limit |
| Per day | 3,000 | 20,000 |

All windows apply at the same time. Going over any of them returns a `429`
error until the window resets, which wom.py hands back as an
[`Err`][wom.Err] like any other API error:

```py
result = await client.players.update_player("Jonxslays")

if result.is_err and result.unwrap_err().status == 429:
    ...  # Back off and try again later
```

Updating the same player too often also returns a `429`, independent of the
rate limits above.

wom.py does not retry or throttle requests for you. If you send many requests
at once, limit how many run concurrently and space them out:

```py
import asyncio

semaphore = asyncio.Semaphore(5)


async def update(username: str) -> None:
    async with semaphore:
        result = await client.players.update_player(username)

        if result.is_err:
            print(f"{username}: {result.unwrap_err().message}")

        # Spread the load, as the WOM team asks
        await asyncio.sleep(1)


await asyncio.gather(*(update(name) for name in usernames))
```

!!! tip

    To update every member of a group, or every participant in a
    competition, use
    [`update_outdated_members`][wom.GroupService.update_outdated_members] or
    [`update_outdated_participants`][wom.CompetitionService.update_outdated_participants]
    instead. They need the group or competition verification code, and queue
    the outdated players for updating on the WOM side with a single request.

## Pagination

Methods that can return a lot of results accept keyword-only `limit` and
`offset` parameters. When you leave them out the API uses its defaults:

| Param | Default | Max |
| --- | --- | --- |
| `limit` | 20 | 50 |
| `offset` | 0 | - |

A few endpoints, such as group hiscores and group gains, don't enforce the
maximum and will return every result if you ask. Check each method's docstring
in the [services reference](../reference/services/index.md) for its
parameters.

To fetch everything, keep increasing `offset` until a page comes back with
fewer items than you asked for:

```py
async def get_all_name_changes(client: wom.Client, group_id: int) -> list[wom.NameChange]:
    limit = 50
    offset = 0
    name_changes: list[wom.NameChange] = []

    while True:
        result = await client.groups.get_name_changes(group_id, limit=limit, offset=offset)

        if result.is_err:
            raise RuntimeError(result.unwrap_err().message)

        page = result.unwrap()
        name_changes.extend(page)

        if len(page) < limit:
            return name_changes

        offset += limit
```

Every page is its own request, so large exports count against your rate limit
like any other requests.

## Using a local WOM instance

If you run the WOM API locally for development, point the client at it with
`api_base_url`, or later with
[`set_api_base_url`][wom.Client.set_api_base_url]:

```py
client = wom.Client(api_base_url="http://localhost:<port>")
```
