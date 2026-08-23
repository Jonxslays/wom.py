# Supported endpoints

wom.py aims to provide one service method for every endpoint of the
[Wise Old Man API](https://docs.wiseoldman.net/). This page lists what is
currently available, grouped by [service](services.md). Each service is a
property on the [`Client`][wom.Client].

Every method returns a [`Result`][wom.Result] - see the
[result guide](result.md) - and the linked reference pages document their full
signatures.

## Players - `client.players`

[`PlayerService`][wom.PlayerService]

| Method | Description |
| --- | --- |
| `search_players` | Searches for a player by partial username. |
| `update_player` | Updates the given player. |
| `assert_player_type` | Asserts, and fixes, a player's type. |
| `get_details` | Gets the details for a given player. |
| `get_details_by_id` | Gets the details for a given player id. |
| `get_achievements` | Gets the achievements for a given player. |
| `get_achievement_progress` | Gets the progress towards achievements for a given player. |
| `get_competition_participations` | Gets the competition participations for a given player. |
| `get_competition_standings` | Gets the competition standings for a given player. |
| `get_group_memberships` | Gets the group memberships for the given player. |
| `get_gains` | Gets the gains made by a player over the given time span. |
| `get_records` | Gets the records held by a player. |
| `get_snapshots` | Gets the snapshots for a player. |
| `get_snapshots_timeline` | Gets the snapshots timeline for a given player and metric. |
| `get_name_changes` | Gets the name changes for a player. |
| `get_archives` | Gets the archives for a given player. |

## Groups - `client.groups`

[`GroupService`][wom.GroupService]

| Method | Description |
| --- | --- |
| `search_groups` | Searches for groups that partially match the given name. |
| `get_details` | Gets the details for a given group id. |
| `create_group` | Creates a new group. |
| `edit_group` | Edits an existing group. |
| `delete_group` | Deletes an existing group. |
| `add_members` | Adds members to an existing group. |
| `remove_members` | Removes members from an existing group. |
| `change_member_role` | Changes the role for a member in an existing group. |
| `update_outdated_members` | Attempts to update all outdated group members. |
| `get_competitions` | Gets competitions for a given group. |
| `get_gains` | Gets the gains for a group over a time frame. |
| `get_bulk_gains` | Gets the bulk gains of all metrics for a group over a time frame. |
| `get_achievements` | Gets the achievements for the group. |
| `get_records` | Gets the records held by players in the group. |
| `get_hiscores` | Gets the hiscores for the group. |
| `get_bulk_hiscores` | Gets the bulk hiscores for the group. |
| `get_name_changes` | Gets the past name changes for the group. |
| `get_statistics` | Gets the statistics for the group. |
| `get_activity` | Gets the activity for the group (paginated). |
| `get_members_csv` | Gets members in the group in CSV format. |

## Competitions - `client.competitions`

[`CompetitionService`][wom.CompetitionService]

| Method | Description |
| --- | --- |
| `search_competitions` | Searches for competitions with the given criteria. |
| `get_details` | Gets details for the given competition. |
| `get_top_participant_history` | Gets the history for the top 5 progressing participants. |
| `create_competition` | Creates a new competition. |
| `edit_competition` | Edits an existing competition. |
| `delete_competition` | Deletes a competition. |
| `add_participants` | Adds participants to a competition. |
| `remove_participants` | Removes participants from a competition. |
| `add_teams` | Adds teams to a competition. |
| `remove_teams` | Removes teams from a competition. |
| `update_outdated_participants` | Attempts to update all outdated competition participants. |
| `get_details_csv` | Gets details about the competition in CSV format. |

## Name changes - `client.names`

[`NameChangeService`][wom.NameChangeService]

| Method | Description |
| --- | --- |
| `search_name_changes` | Searches for name changes. |
| `submit_name_change` | Submits a new name change. |
| `bulk_submit_name_changes` | Submits multiple name changes at once. |
| `get_name_change_details` | Gets the details of a name change. |

## Deltas - `client.deltas`

[`DeltaService`][wom.DeltaService]

| Method | Description |
| --- | --- |
| `get_global_leaderboards` | Gets the top global delta leaderboard for a metric. |

## Records - `client.records`

[`RecordService`][wom.RecordService]

| Method | Description |
| --- | --- |
| `get_global_leaderboards` | Gets the global record leaderboards. |

## Efficiency - `client.efficiency`

[`EfficiencyService`][wom.EfficiencyService]

| Method | Description |
| --- | --- |
| `get_global_leaderboards` | Gets the top global efficiency leaderboard. |
| `get_rates` | Gets the efficiency rates for a given algorithm type and metric. |

## General - `client.general`

[`GeneralService`][wom.GeneralService]

| Method | Description |
| --- | --- |
| `get_stats` | Gets global statistics about the data tracked by WOM. |
