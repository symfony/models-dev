#!/usr/bin/env python3
"""Compare two models-dev.json files and output a semantic commit message."""

import json
import sys


def load(path):
    with open(path) as f:
        return json.load(f)


def diff(old, new):
    old_providers = set(old.keys())
    new_providers = set(new.keys())

    added_providers = sorted(new_providers - old_providers)
    removed_providers = sorted(old_providers - new_providers)
    common_providers = sorted(old_providers & new_providers)

    added_models = {}
    removed_models = {}

    for p in added_providers:
        models = sorted(new[p].get("models", {}).keys())
        if models:
            added_models[p] = models

    for p in removed_providers:
        models = sorted(old[p].get("models", {}).keys())
        if models:
            removed_models[p] = models

    for p in common_providers:
        old_models = set(old[p].get("models", {}).keys())
        new_models = set(new[p].get("models", {}).keys())
        added = sorted(new_models - old_models)
        removed = sorted(old_models - new_models)
        if added:
            added_models[p] = added
        if removed:
            removed_models[p] = removed

    lines = []

    if added_providers:
        lines.append("Added providers: " + ", ".join(added_providers))

    if removed_providers:
        lines.append("Removed providers: " + ", ".join(removed_providers))

    if added_models:
        lines.append("")
        lines.append("Added models:")
        for p in sorted(added_models.keys()):
            lines.append(f"  {p}: " + ", ".join(added_models[p]))

    if removed_models:
        lines.append("")
        lines.append("Removed models:")
        for p in sorted(removed_models.keys()):
            lines.append(f"  {p}: " + ", ".join(removed_models[p]))

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <old.json> <new.json>", file=sys.stderr)
        sys.exit(1)

    old = load(sys.argv[1])
    new = load(sys.argv[2])
    result = diff(old, new)

    if result:
        print(result)
