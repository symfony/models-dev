PHP models.dev Package
======================

This repository provides a daily snapshot of the [models.dev](https://models.dev)
API as a Composer package. It makes the full catalog of AI model metadata
(providers, models, pricing, context limits, modalities, …) available to any PHP
project via a simple `composer require`.

How it works
------------

A GitHub Actions workflow runs every day at 06:00 UTC:

1. It fetches the latest data from `https://models.dev/api.json`.
2. If the data has changed, it commits the updated `models-dev.json` file.
3. It creates a GitHub Release with a new version tag and a changelog describing
   added/removed providers and models. The version follows semver: minor bumps
   for additions and metadata updates (`v1.0` → `v1.1`), major bumps when
   models or providers are removed (`v1.3` → `v2.0`).

Installation
------------

Releases follow semver: minor versions add new models or providers, major versions
indicate removals. Use the `^` constraint to automatically receive new
models/providers while staying protected from removals:

```bash
composer require symfony/models-dev:^1.0
```

When a new major version is released, review the release notes to see what was
removed before upgrading.

The `models-dev.json` file at the root of the package contains the full dataset.

Usage
-----

This package can be used in conjunction with the
[Symfony AI Models.dev bridge](https://github.com/symfony/ai-models-dev-platform),
which provides a universal platform giving access to all AI providers available on
models.dev with automatic capability discovery, pricing, and routing to specialized
bridges. See the
[full documentation](https://symfony.com/doc/current/ai/components/platform/models-dev.html)
for details.

You can also use the JSON data directly:

```php
$models = json_decode(
    file_get_contents(__DIR__.'/vendor/symfony/models-dev/models-dev.json'),
    true,
);

// List all providers
$providers = array_keys($models);

// Get all models for a given provider
$openaiModels = $models['openai']['models'];
```
