#!/usr/bin/env python3
"""Compare two models-dev.json files and output a semantic changelog in Markdown."""

import json
import sys


def load(path):
    with open(path) as f:
        return json.load(f)


def compute_diff(old, new):
    old_providers = set(old.keys())
    new_providers = set(new.keys())

    added_providers = sorted(new_providers - old_providers)
    removed_providers = sorted(old_providers - new_providers)

    added_models = {}
    removed_models = {}

    for p in sorted(old_providers & new_providers):
        old_m = set(old[p].get("models", {}).keys())
        new_m = set(new[p].get("models", {}).keys())
        added = sorted(new_m - old_m)
        removed = sorted(old_m - new_m)
        if added:
            added_models[p] = added
        if removed:
            removed_models[p] = removed

    return {
        "added_providers": added_providers,
        "removed_providers": removed_providers,
        "added_models": added_models,
        "removed_models": removed_models,
    }


def is_breaking(result):
    return bool(result["removed_providers"] or result["removed_models"])


def format_diff(result, old, new):
    added_providers = result["added_providers"]
    removed_providers = result["removed_providers"]
    added_models = result["added_models"]
    removed_models = result["removed_models"]

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

    if not sections and old != new:
        sections.append("Model metadata updated (no providers or models added/removed).")

    return "\n\n".join(sections)


if __name__ == "__main__":
    usage = f"Usage: {sys.argv[0]} [--breaking] <old.json> <new.json>"

    args = sys.argv[1:]
    breaking_mode = False
    if args and args[0] == "--breaking":
        breaking_mode = True
        args = args[1:]

    if len(args) != 2:
        print(usage, file=sys.stderr)
        sys.exit(1)

    old = load(args[0])
    new = load(args[1])
    result = compute_diff(old, new)

    if breaking_mode:
        print("true" if is_breaking(result) else "false")
    else:
        output = format_diff(result, old, new)
        if output:
            print(output)
