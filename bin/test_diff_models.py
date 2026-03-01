#!/usr/bin/env python3
"""Tests for diff_models.py."""

import unittest
from diff_models import compute_diff, format_diff, is_breaking


class TestComputeDiff(unittest.TestCase):
    def test_identical(self):
        data = {"p": {"models": {"m1": {}}}}
        result = compute_diff(data, data)
        self.assertEqual(result["added_providers"], [])
        self.assertEqual(result["removed_providers"], [])
        self.assertEqual(result["added_models"], {})
        self.assertEqual(result["removed_models"], {})

    def test_added_provider(self):
        old = {"p1": {"models": {"m1": {}}}}
        new = {"p1": {"models": {"m1": {}}}, "p2": {"models": {"m2": {}}}}
        result = compute_diff(old, new)
        self.assertEqual(result["added_providers"], ["p2"])
        self.assertEqual(result["removed_providers"], [])
        self.assertEqual(result["added_models"], {})

    def test_removed_provider(self):
        old = {"p1": {"models": {"m1": {}}}, "p2": {"models": {"m2": {}}}}
        new = {"p1": {"models": {"m1": {}}}}
        result = compute_diff(old, new)
        self.assertEqual(result["removed_providers"], ["p2"])
        self.assertEqual(result["added_providers"], [])
        self.assertEqual(result["removed_models"], {})

    def test_added_model(self):
        old = {"p": {"models": {"m1": {}}}}
        new = {"p": {"models": {"m1": {}, "m2": {}}}}
        result = compute_diff(old, new)
        self.assertEqual(result["added_models"], {"p": ["m2"]})
        self.assertEqual(result["removed_models"], {})

    def test_removed_model(self):
        old = {"p": {"models": {"m1": {}, "m2": {}}}}
        new = {"p": {"models": {"m1": {}}}}
        result = compute_diff(old, new)
        self.assertEqual(result["removed_models"], {"p": ["m2"]})
        self.assertEqual(result["added_models"], {})

    def test_provider_without_models_key(self):
        old = {"p": {}}
        new = {"p": {"models": {"m1": {}}}}
        result = compute_diff(old, new)
        self.assertEqual(result["added_models"], {"p": ["m1"]})

    def test_combined_changes(self):
        old = {"p1": {"models": {"m1": {}}}, "p2": {"models": {"m2": {}}}}
        new = {"p1": {"models": {"m1": {}, "m3": {}}}, "p3": {"models": {"m4": {}}}}
        result = compute_diff(old, new)
        self.assertEqual(result["added_providers"], ["p3"])
        self.assertEqual(result["removed_providers"], ["p2"])
        self.assertEqual(result["added_models"], {"p1": ["m3"]})
        self.assertEqual(result["removed_models"], {})


class TestIsBreaking(unittest.TestCase):
    def test_additions_only(self):
        result = {"added_providers": ["p"], "removed_providers": [], "added_models": {"p": ["m"]}, "removed_models": {}}
        self.assertFalse(is_breaking(result))

    def test_removed_provider(self):
        result = {"added_providers": [], "removed_providers": ["p"], "added_models": {}, "removed_models": {}}
        self.assertTrue(is_breaking(result))

    def test_removed_model(self):
        result = {"added_providers": [], "removed_providers": [], "added_models": {}, "removed_models": {"p": ["m"]}}
        self.assertTrue(is_breaking(result))

    def test_no_changes(self):
        result = {"added_providers": [], "removed_providers": [], "added_models": {}, "removed_models": {}}
        self.assertFalse(is_breaking(result))


class TestFormatDiff(unittest.TestCase):
    def test_identical(self):
        data = {"p": {"models": {"m1": {}}}}
        result = compute_diff(data, data)
        self.assertEqual(format_diff(result, data, data), "")

    def test_metadata_only_change(self):
        old = {"p": {"models": {"m1": {"cost": 1}}}}
        new = {"p": {"models": {"m1": {"cost": 2}}}}
        result = compute_diff(old, new)
        self.assertIn("Model metadata updated", format_diff(result, old, new))

    def test_added_provider_not_in_model_section(self):
        old = {}
        new = {"p": {"models": {"m1": {}, "m2": {}}}}
        result = compute_diff(old, new)
        output = format_diff(result, old, new)
        self.assertIn("New Providers", output)
        self.assertNotIn("New Models", output)

    def test_removed_provider_not_in_model_section(self):
        old = {"p": {"models": {"m1": {}}}}
        new = {}
        result = compute_diff(old, new)
        output = format_diff(result, old, new)
        self.assertIn("Removed Providers", output)
        self.assertNotIn("Removed Models", output)

    def test_summary_line(self):
        old = {"p": {"models": {"m1": {}}}}
        new = {"p": {"models": {"m1": {}, "m2": {}, "m3": {}}}}
        result = compute_diff(old, new)
        output = format_diff(result, old, new)
        self.assertIn("2 new model(s)", output)

    def test_model_section_grouped_by_provider(self):
        old = {"p1": {"models": {}}, "p2": {"models": {}}}
        new = {"p1": {"models": {"m1": {}}}, "p2": {"models": {"m2": {}}}}
        result = compute_diff(old, new)
        output = format_diff(result, old, new)
        self.assertIn("**p1**: `m1`", output)
        self.assertIn("**p2**: `m2`", output)


if __name__ == "__main__":
    unittest.main()
