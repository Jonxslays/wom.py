# Using the client

The [`Client`][wom.Client] class is used to interact with the WOM API. You use
the client to make requests via its difference service properties.

Services available on the client include:

- [`CompetitionService`][wom.CompetitionService] via `Client.competitions`
- [`DeltaService`][wom.DeltaService] via `Client.deltas`
- [`EfficiencyService`][wom.EfficiencyService] via `Client.efficiency`
- [`GroupService`][wom.GroupService] via `Client.groups`
- [`NameChangeService`][wom.NameChangeService] via `Client.name_changes`
- [`PlayerService`][wom.PlayerService] via `Client.players`
- [`RecordService`][wom.RecordService] via `Client.records`

## Instantiating the client

```py
import wom

client = wom.Client(
    "api_abc123",  # The wom api key to use.
    user_agent="@jonxslays",
    api_base_url="https://api.wiseoldman.net/v2",
)
```

Api base url and user agent are both optional, but user agent is highly
encouraged. The client defaults to using the production wom api url.
If you are running a local instance of the wom api you can set the base url to
your instance.

!!! info

    You only need a single instance of the `Client` to make requests to WOM.
    If you feel like you need multiple `Client` instances you should reconsider
    the architecture of your application, and how you can reuse your existing
    `Client` resource. Some niche scenarios could warrant more than one
    `Client`, but these use cases aren't common for most users.

## Handling client resources

The wom [`Client`][wom.Client] uses an `aiohttp.ClientSession` under the hood,
so it is important that you call [`Client.start`][wom.Client.start] and
[`Client.close`][wom.Client.close] appropriately.

```py
# ...continued from above

await client.start()

# Make requests here...

await client.close()
```

You will receive errors/warnings if you do not properly start the client
before using it, or close it before your program terminates.

## Example client usage

```py
import asyncio

import wom


async def main() -> None:
    # Instantiate the client
    client = wom.Client()

    # Start the client
    await client.start()

    # You can also alter some client properties after instantiation
    client.set_api_base_url("https://api.wiseoldman.net/v2")
    client.set_api_key("my-new-api-key")
    client.set_user_agent("@jonxslays")

    # Oops that api key was bogus, lets remove it
    client.unset_api_key()

    # Make requests with the client
    result = await client.groups.get_details(139)

    if result.is_ok:
        # The result is ok, so we can unwrap here
        details = result.unwrap()
        print(details.group)
        print(details.memberships)
    else:
        # Lets see what went wrong
        print(f"Error: {result.unwrap_err()}")

    # Close the client
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

```
