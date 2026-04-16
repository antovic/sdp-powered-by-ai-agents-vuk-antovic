#!/usr/bin/env bash
# Pre-push hook: build Docker image and run tests before pushing

set -e

IMAGE="kata-tests"

echo "🐳 Building Docker image..."
docker build -t "$IMAGE" . >/dev/null

echo "🧪 Running tests..."
docker run --rm "$IMAGE"

echo "✅ Tests passed."
