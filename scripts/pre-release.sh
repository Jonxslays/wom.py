#!/usr/bin/env sh

echo "Pre-release initialized!";

LATEST_TAG=$(git tag -l | tail -1);
PROJECT_VERS=$(./scripts/version-check.sh);
LATEST_SHA=$(git rev-parse --short HEAD);

echo "Validating project versions...";

if [ ! "$LATEST_TAG" = "$PROJECT_VERS" ]; then
    echo "Latest tag $LATEST_TAG doesn't match project version!";
    exit 1;
fi

./scripts/update-sha.sh $LATEST_SHA;

echo "Pre-release complete!";
