# Wom services

Services are important to understand when using `wom.py`.

Each service is related to a particular area of the WOM API, and makes requests
to those endpoints.

## Available services

- [`CompetitionService`][wom.CompetitionService] for requests related to competitions.
- [`DeltaService`][wom.DeltaService] for requests related to deltas.
- [`EfficiencyService`][wom.EfficiencyService] for requests related to efficiency.
- [`GroupService`][wom.GroupService] for requests related to groups.
- [`NameChangeService`][wom.NameChangeService] for requests related to name changes.
- [`PlayerService`][wom.PlayerService] for requests related to players.
- [`RecordService`][wom.RecordService] for requests related to records.

## Usage

Each of these services are available to you as properties on the [`Client`][wom.Client].

You should not personally be creating instances of these services, but instead use
the client to make requests using the services.

```py
client = wom.Client()

await client.start()

# Use the name change service to submit a name change
result = await client.name_changes.submit_name_change("old name", "new name")

# ... Do something with the result here

await client.close()
```
