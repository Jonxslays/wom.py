# Models

Typed model classes returned by the service methods. Every response the WOM API
sends is deserialized into one of these; the API's camelCase fields map to the
snake_case attributes documented on each page.

Models are grouped by the area of the API they come from:

- [Players](players.md)
- [Groups](groups.md)
- [Competitions](competitions.md)
- [Name changes](names.md)
- [Deltas](deltas.md)
- [Records](records.md)
- [Efficiency](efficiency.md)
- [General](general.md)

Every model is also exported at the top level, so you always use `wom.Player`,
`wom.GroupDetail`, and so on, never the module path.

## Shared models

The base class every model inherits from, and the responses used for errors and
bare-message endpoints.

::: wom.models.base

::: wom.models.http
