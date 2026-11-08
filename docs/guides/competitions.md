# Competitions

Competitions track the progress of a set of players in one or more metrics over
a fixed period of time. This guide walks through creating, managing, and
reading competitions with the
[`CompetitionService`][wom.CompetitionService] (`client.competitions`).

## Creating a competition

[`create_competition`][wom.CompetitionService.create_competition] needs a
title, the metrics to track, and a start and end time:

```py
from datetime import datetime, timedelta, timezone

import wom

now = datetime.now(timezone.utc)

result = await client.competitions.create_competition(
    "Slayer week",
    metrics=[wom.Metric.Slayer],
    starts_at=now + timedelta(days=1),
    ends_at=now + timedelta(days=8),
    participants=["Jonxslays", "Zezima"],
)

if result.is_ok:
    created = result.unwrap()
    print(f"Created competition {created.competition.id}")
    print(f"Verification code: {created.verification_code}")
```

!!! warning "Save the verification code"

    The returned [`CreatedCompetitionDetail`][wom.CreatedCompetitionDetail] is
    the only time you receive the competition's `verification_code`. You need
    it to edit, delete, or update the competition later, so store it somewhere
    safe.

### Multi-metric competitions

Pass more than one metric to track several at once. The API requires them to
all be of the same category - all skills, all bosses, and so on:

```py
result = await client.competitions.create_competition(
    "Wilderness boss week",
    metrics=[wom.Metric.Callisto, wom.Metric.Venenatis, wom.Metric.Vetion],
    starts_at=now + timedelta(days=1),
    ends_at=now + timedelta(days=8),
    participants=["Jonxslays", "Zezima"],
)
```

The [`Skills`][wom.Skills], [`Bosses`][wom.Bosses],
[`Activities`][wom.Activities], and
[`ComputedMetrics`][wom.ComputedMetrics] sets help you check which category a
metric belongs to - see [metrics and enums](metrics.md#metric-categories).

### Who takes part

Choose how participants are added with one of these parameters:

- `participants` - a list of usernames, for a classic competition.
- `group_id` and `group_verification_code` - every member of the group joins
  a classic competition, and it shows up on the group's page.
- `teams` - a list of [`Team`][wom.Team]s, for a team competition. You can
  also pass `group_id` to link the competition to a group.

```py
result = await client.competitions.create_competition(
    "Team boss week",
    metrics=[wom.Metric.Zulrah],
    starts_at=now + timedelta(days=1),
    ends_at=now + timedelta(days=8),
    teams=[
        wom.Team("Team one", ["Jonxslays", "Zezima"]),
        wom.Team("Team two", ["Lynx Titan", "B0aty"]),
    ],
)
```

!!! note "Deprecated: the single `metric` argument"

    Older code may pass a single metric as the second positional argument,
    like `create_competition("Slayer week", wom.Metric.Slayer, ...)`. This
    still works but is deprecated in favor of `metrics`. If you pass both,
    they are combined.

## Managing a competition

Every method that changes a competition takes its id and verification code:

```py
competition_id = 123
code = "111-111-111"

# Change the title or end date, add metrics, or replace teams
await client.competitions.edit_competition(
    competition_id, code, title="Slayer fortnight", ends_at=now + timedelta(days=15)
)

# Add or remove participants (classic competitions)
await client.competitions.add_participants(competition_id, code, "Woox", "Lynx Titan")
await client.competitions.remove_participants(competition_id, code, "Zezima")

# Add or remove teams (team competitions)
await client.competitions.add_teams(competition_id, code, wom.Team("Team three", ["Woox"]))
await client.competitions.remove_teams(competition_id, code, "Team two")

# Queue updates for every outdated participant
await client.competitions.update_outdated_participants(competition_id, code)

# Delete it entirely
await client.competitions.delete_competition(competition_id, code)
```

Each of these returns a [`Result`][wom.Result], so check it the same way as any
other request - see [handling errors](errors.md). A wrong verification code
comes back as an [`Err`][wom.Err] with a `403` status.

## Reading results

[`get_details`][wom.CompetitionService.get_details] returns a
[`CompetitionDetail`][wom.CompetitionDetail] with every participant's
progress, ordered from the most to the least progress made:

```py
result = await client.competitions.get_details(123)
detail = result.unwrap()

print(detail.title, [str(m.metric) for m in detail.metrics])

for rank, participation in enumerate(detail.participations, start=1):
    print(f"{rank}. {participation.player.display_name}")

    for delta in participation.deltas:
        if delta.is_total:
            print(f"   Total gained: {delta.values.gained:,}")
        else:
            print(f"   {delta.as_metric()}: {delta.values.gained:,}")
```

Each participation's `deltas` holds one
[`CompetitionMetricDelta`][wom.CompetitionMetricDelta] per metric, plus a
combined entry for the competition as a whole. That combined entry's `metric`
is the string `"total"`, which isn't a [`Metric`][wom.Metric], so use
[`is_total`][wom.CompetitionMetricDelta.is_total] to find it and
[`as_metric()`][wom.CompetitionMetricDelta.as_metric] to get the
[`Metric`][wom.Metric] for every other entry.

!!! note "Deprecated: `metric`, `progress`, and `levels`"

    [`Competition.metric`][wom.Competition.metric] and the `progress` /
    `levels` fields on
    [`CompetitionParticipationDetail`][wom.CompetitionParticipationDetail] only
    reflect the competition's **first** metric. They are kept for single-metric
    code, but new code should use
    [`Competition.metrics`][wom.Competition.metrics] and
    [`deltas`][wom.CompetitionParticipationDetail.deltas] instead.

### Viewing progress in other metrics

Pass `metrics` to [`get_details`][wom.CompetitionService.get_details] to see the
participants' progress as if the competition was for those metrics instead:

```py
result = await client.competitions.get_details(
    123, metrics=[wom.Metric.Attack, wom.Metric.Strength]
)
```

[`get_top_participant_history`][wom.CompetitionService.get_top_participant_history]
returns the progress over time of the top five participants, which is useful
for drawing charts, and
[`get_details_csv`][wom.CompetitionService.get_details_csv] returns the
results as CSV text.

## Finding competitions

```py
# Search every competition on WOM
result = await client.competitions.search_competitions(
    title="Slayer", status=wom.CompetitionStatus.Ongoing, limit=10
)

# A group's competitions
result = await client.groups.get_competitions(139)

# A player's competitions, with their standing in each
result = await client.players.get_competition_standings(
    "Jonxslays", wom.CompetitionStatus.Ongoing
)
```
