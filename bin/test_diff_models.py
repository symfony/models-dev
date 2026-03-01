#!/usr/bin/env python3
"""Tests for diff_models.py."""

import unittest
from diff_models import diff


class TestDiff(unittest.TestCase):
    def test_identical(self):
        data = {"p": {"models": {"m1": {}}}}
        self.assertEqual(diff(data, data), "")

    def test_added_provider(self):
        old = {"p1": {"models": {"m1": {}}}}
        new = {"p1": {"models": {"m1": {}}}, "p2": {"models": {"m2": {}}}}
        result = diff(old, new)
        self.assertIn("1 new provider(s)", result)
        self.assertIn("**p2**", result)
        self.assertNotIn("New Models", result)

    def test_removed_provider(self):
        old = {"p1": {"models": {"m1": {}}}, "p2": {"models": {"m2": {}}}}
        new = {"p1": {"models": {"m1": {}}}}
        result = diff(old, new)
        self.assertIn("1 removed provider(s)", result)
        self.assertIn("**p2**", result)
        self.assertNotIn("Removed Models", result)

    def test_added_model(self):
        old = {"p": {"models": {"m1": {}}}}
        new = {"p": {"models": {"m1": {}, "m2": {}}}}
        result = diff(old, new)
        self.assertIn("1 new model(s)", result)
        self.assertIn("`m2`", result)
        self.assertIn("**p**", result)
        self.assertNotIn("New Providers", result)

    def test_removed_model(self):
        old = {"p": {"models": {"m1": {}, "m2": {}}}}
        new = {"p": {"models": {"m1": {}}}}
        result = diff(old, new)
        self.assertIn("1 removed model(s)", result)
        self.assertIn("`m2`", result)

    def test_metadata_only_change(self):
        old = {"p": {"models": {"m1": {"cost": 1}}}}
        new = {"p": {"models": {"m1": {"cost": 2}}}}
        result = diff(old, new)
        self.assertIn("Model metadata updated", result)

    def test_new_provider_models_not_in_model_section(self):
        old = {}
        new = {"p": {"models": {"m1": {}, "m2": {}}}}
        result = diff(old, new)
        self.assertIn("New Providers", result)
        self.assertNotIn("New Models", result)

    def test_removed_provider_models_not_in_model_section(self):
        old = {"p": {"models": {"m1": {}}}}
        new = {}
        result = diff(old, new)
        self.assertIn("Removed Providers", result)
        self.assertNotIn("Removed Models", result)

    def test_provider_without_models_key(self):
        old = {"p": {}}
        new = {"p": {"models": {"m1": {}}}}
        result = diff(old, new)
        self.assertIn("1 new model(s)", result)
        self.assertIn("`m1`", result)

    def test_combined_changes(self):
        old = {"p1": {"models": {"m1": {}}}, "p2": {"models": {"m2": {}}}}
        new = {"p1": {"models": {"m1": {}, "m3": {}}}, "p3": {"models": {"m4": {}}}}
        result = diff(old, new)
        self.assertIn("1 new provider(s)", result)
        self.assertIn("1 removed provider(s)", result)
        self.assertIn("1 new model(s)", result)
        self.assertIn("**p3**", result)
        self.assertIn("`m3`", result)
        self.assertNotIn("`m4`", result)


if __name__ == "__main__":
    unittest.main()
