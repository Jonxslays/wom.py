#!/usr/bin/env sh
# Compare the routes the upstream Wise Old Man server defines with the
# routes wom.py implements in wom/routes.py.
#
# Usage (from the repo root): sh .claude/skills/api-drift/route-diff.sh [ref]
#   ref: upstream branch, tag or sha to compare against (default: master)
#
# Path params are normalized to {} on both sides, so `/players/:username`
# and `/players/{}` compare equal. Prints routes only upstream has, then
# routes only wom.py has.

set -eu

REPO="wise-old-man/wise-old-man"
REF="${1:-master}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

gh api "repos/$REPO/git/trees/$REF?recursive=1" \
    --jq '.tree[].path | select(startswith("server/src/api/modules/") and endswith(".router.ts"))' \
    > "$WORK/routers.txt"

while read -r file; do
    gh api "repos/$REPO/contents/$file?ref=$REF" --jq .content | base64 -d \
        | tr '\n' ' ' \
        | grep -oE "router\.(get|post|put|patch|delete)\(\s*'[^']+'" || true
done < "$WORK/routers.txt" \
    | sed -E "s/router\.([a-z]+)\(\s*'([^']+)'/\1 \2/; s/:[A-Za-z]+/{}/g" \
    | awk '{ print toupper($1), $2 }' \
    | sort -u > "$WORK/upstream.txt"

grep -oE 'Route\("[A-Z]+", "[^"]+"\)' wom/routes.py \
    | sed -E 's/Route\("([A-Z]+)", "([^"]+)"\)/\1 \2/' \
    | sort -u > "$WORK/wom.txt"

echo "upstream routes: $(wc -l < "$WORK/upstream.txt")  wom.py routes: $(wc -l < "$WORK/wom.txt")"
echo
echo "--- only upstream (missing from wom.py)"
comm -23 "$WORK/upstream.txt" "$WORK/wom.txt"
echo
echo "--- only wom.py (removed or renamed upstream?)"
comm -13 "$WORK/upstream.txt" "$WORK/wom.txt"
