#!/usr/bin/env bash
# Pre-push hook: build Docker image and run tests before pushing

set -e

IMAGE="kata-tests"
DOCKER_BUILD_QUIET="${DOCKER_BUILD_QUIET:-0}"

echo "🐳 Building Docker image..."
if [ "$DOCKER_BUILD_QUIET" = "1" ]; then
  docker build -t "$IMAGE" . >/dev/null
else
  docker build -t "$IMAGE" .
fi

echo "🧪 Running tests..."
docker run --rm "$IMAGE"

echo "✅ Tests passed."
