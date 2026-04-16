#!/usr/bin/env bash
# Pre-commit hook: build Docker image and run tests before committing

set -e

IMAGE="kata-tests"

echo "🐳 Building Docker image..."
docker build -t "$IMAGE" . >/dev/null

echo "🧪 Running tests..."
docker run --rm "$IMAGE"; code=$?; [ $code -eq 5 ] && exit 0 || exit $code

echo "✅ Tests passed."
