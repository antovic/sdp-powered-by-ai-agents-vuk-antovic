#!/usr/bin/env bash
set -e

PLANTUML_JAR="$HOME/.local/share/plantuml/plantuml.jar"
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep '\.puml$' || true)

if [ -z "$STAGED" ]; then
  exit 0
fi

if [ ! -f "$PLANTUML_JAR" ]; then
  echo "⚠️  PlantUML jar not found at $PLANTUML_JAR. Run scripts/setup.sh first."
  exit 1
fi

for PUML in $STAGED; do
  echo "🔄 Generating SVG for $PUML"
  java -jar "$PLANTUML_JAR" -tsvg "$PUML"
  SVG="${PUML%.puml}.svg"
  if [ -f "$SVG" ]; then
    git add "$SVG"
    echo "✅ Staged $SVG"
  fi
done
