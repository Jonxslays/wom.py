# Services

Each service groups the requests for one area of the WOM API and is accessed as
a property on the [`Client`][wom.Client]. For a high-level tour see the
[services guide](../../getting-started/services.md), and for a flat list of
every method see [supported endpoints](../../getting-started/endpoints.md).

| Service | Client property | Reference |
| --- | --- | --- |
| [`PlayerService`][wom.PlayerService] | `client.players` | [Players](players.md) |
| [`GroupService`][wom.GroupService] | `client.groups` | [Groups](groups.md) |
| [`CompetitionService`][wom.CompetitionService] | `client.competitions` | [Competitions](competitions.md) |
| [`NameChangeService`][wom.NameChangeService] | `client.names` | [Name changes](names.md) |
| [`DeltaService`][wom.DeltaService] | `client.deltas` | [Deltas](deltas.md) |
| [`RecordService`][wom.RecordService] | `client.records` | [Records](records.md) |
| [`EfficiencyService`][wom.EfficiencyService] | `client.efficiency` | [Efficiency](efficiency.md) |
| [`GeneralService`][wom.GeneralService] | `client.general` | [General](general.md) |

The [`BaseService`][wom.BaseService] they inherit from and the
[`HttpService`][wom.HttpService] that performs requests are documented under
[internals](../internals/http.md).
