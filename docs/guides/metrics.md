# Metrics and enums

Most requests take or return enums: the metric a leaderboard is for, the period
gains are measured over, a player's account type, and so on. All of them are
exported at the top level (`wom.Metric`, `wom.Period`, `wom.PlayerType`, ...).

## The Metric enum

[`Metric`][wom.Metric] holds every skill, boss, activity, and computed metric
WOM tracks, in a single enum:

```py
wom.Metric.Attack          # A skill
wom.Metric.Zulrah          # A boss
wom.Metric.LastManStanding # An activity
wom.Metric.Ehp             # A computed metric (efficient hours played)
```

Pass members straight into service methods. wom.py sends their string value to
the API for you:

```py
result = await client.deltas.get_global_leaderboards(
    wom.Metric.Slayer, wom.Period.Week
)
```

## Metric categories

To check what kind of metric you have, use the four frozensets that group
[`Metric`][wom.Metric] members by category:

- [`Skills`][wom.Skills]
- [`Bosses`][wom.Bosses]
- [`Activities`][wom.Activities]
- [`ComputedMetrics`][wom.ComputedMetrics]

```py
metric = wom.Metric.Vorkath

if metric in wom.Bosses:
    print(f"{metric} is a boss")

# Every skill except overall
skills = [m for m in wom.Skills if m is not wom.Metric.Overall]
```

They are handy when building multi-metric competitions, whose metrics must all
be of the same category - see [competitions](competitions.md).

## Periods

[`Period`][wom.Period] is used by the gains, records, and leaderboard methods:

```py
result = await client.players.get_gains("Jonxslays", period=wom.Period.Month)
```

Methods that accept a `period` often also accept a `start_date` and `end_date`
as an alternative. Pass one or the other, not both - the method's docstring
says which combinations are allowed.

## Working with enum values

Every wom.py enum inherits from [`BaseEnum`][wom.BaseEnum], which makes them
behave like the strings the API uses:

```py
str(wom.Metric.Attack)                       # "attack"
wom.Metric.Attack == "attack"                # True
wom.Metric("attack") is wom.Metric.Attack    # True, look up by value

wom.Metric.at_random()                       # A random metric
```

Comparing against strings means you can check user input directly, and
`Metric(value)` turns a string from a command or config file back into an
enum.

## Reading metric data

Snapshots and gains store their data in dictionaries keyed by
[`Metric`][wom.Metric], split by category:

```py
result = await client.players.get_details("Jonxslays")
player = result.unwrap()

if player.latest_snapshot:
    data = player.latest_snapshot.data

    slayer = data.skills[wom.Metric.Slayer]
    print(f"Slayer level {slayer.level} ({slayer.experience:,} xp)")

    zulrah = data.bosses[wom.Metric.Zulrah]
    print(f"{zulrah.kills} Zulrah kills")
```

## Unknown values

WOM regularly adds new bosses, activities, and other enum values. If the API
sends a value your installed version of wom.py doesn't know about, it is
decoded as the enum's `Unknown` variant and an
[`UnknownEnumWarning`][wom.UnknownEnumWarning] is emitted instead of the
request failing.

- Upgrading wom.py (`pip install -U wom.py`) usually adds the new value.
- Iterating an enum skips its `Unknown` variant, so loops like
  `for metric in wom.Metric` only see real values.
- If you'd rather not see the warning, filter it like any other:

```py
import warnings

warnings.filterwarnings("ignore", category=wom.UnknownEnumWarning)
```

If a value has been missing for a while, please
[open an issue](https://github.com/Jonxslays/wom.py/issues/new/choose).
