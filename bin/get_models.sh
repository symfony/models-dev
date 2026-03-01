#!/bin/bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
curl -fsSL https://models.dev/api.json | jq -S . > "$DIR/../models-dev.json"
