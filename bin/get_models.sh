#!/bin/bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
curl -fsSL https://models.dev/api.json | jq -S . > "$DIR/../models-dev.json.tmp"
mv "$DIR/../models-dev.json.tmp" "$DIR/../models-dev.json"
