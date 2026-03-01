#!/usr/bin/env python3
"""Compare two models-dev.json files and output a semantic changelog in Markdown."""

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
        old_m = set(old[p].get("models", {}).keys())
        new_m = set(new[p].get("models", {}).keys())
        added = sorted(new_m - old_m)
        removed = sorted(old_m - new_m)
        if added:
            added_models[p] = added
        if removed:
            removed_models[p] = removed

    total_added = sum(len(m) for m in added_models.values())
    total_removed = sum(len(m) for m in removed_models.values())

    sections = []

    # Summary line
    parts = []
    if added_providers:
        parts.append(f"{len(added_providers)} new provider(s)")
    if removed_providers:
        parts.append(f"{len(removed_providers)} removed provider(s)")
    if total_added:
        parts.append(f"{total_added} new model(s)")
    if total_removed:
        parts.append(f"{total_removed} removed model(s)")
    if parts:
        sections.append(", ".join(parts) + ".")

    # Providers
    if added_providers:
        sections.append("### New Providers\n\n" + "\n".join(f"- **{p}**" for p in added_providers))

    if removed_providers:
        sections.append("### Removed Providers\n\n" + "\n".join(f"- **{p}**" for p in removed_providers))

    # Models
    if added_models:
        lines = []
        for p in sorted(added_models.keys()):
            lines.append(f"- **{p}**: " + ", ".join(f"`{m}`" for m in added_models[p]))
        sections.append("### New Models\n\nThe following models have been added, grouped by provider:\n\n" + "\n".join(lines))

    if removed_models:
        lines = []
        for p in sorted(removed_models.keys()):
            lines.append(f"- **{p}**: " + ", ".join(f"`{m}`" for m in removed_models[p]))
        sections.append("### Removed Models\n\nThe following models have been removed, grouped by provider:\n\n" + "\n".join(lines))

    return "\n\n".join(sections)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <old.json> <new.json>", file=sys.stderr)
        sys.exit(1)

    old = load(sys.argv[1])
    new = load(sys.argv[2])
    result = diff(old, new)

    if result:
        print(result)
