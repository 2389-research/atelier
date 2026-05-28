"""Unit tests for jsonl_stats.core."""

import json
import tempfile
from pathlib import Path

import pytest

from jsonl_stats.core import (
    build_report,
    count_records,
    field_coverage,
    load_records,
    type_histogram,
)


class TestLoadRecords:
    """Test load_records function."""

    def test_load_simple_records(self):
        """Load a simple JSONL file with multiple records."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write('{"id": 1, "name": "Alice"}\n')
            f.write('{"id": 2, "name": "Bob"}\n')
            f.flush()
            path = f.name

        try:
            records = load_records(path)
            assert len(records) == 2
            assert records[0] == {"id": 1, "name": "Alice"}
            assert records[1] == {"id": 2, "name": "Bob"}
        finally:
            Path(path).unlink()

    def test_load_records_skip_blank_lines(self):
        """Blank lines should be skipped, not counted as records."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write('{"id": 1}\n')
            f.write('\n')
            f.write('  \n')
            f.write('{"id": 2}\n')
            f.flush()
            path = f.name

        try:
            records = load_records(path)
            assert len(records) == 2
            assert records[0] == {"id": 1}
            assert records[1] == {"id": 2}
        finally:
            Path(path).unlink()


class TestCountRecords:
    """Test count_records function."""

    def test_count_empty(self):
        """Empty list should return 0."""
        assert count_records([]) == 0

    def test_count_multiple(self):
        """Count multiple records."""
        records = [{"a": 1}, {"b": 2}, {"c": 3}]
        assert count_records(records) == 3


class TestFieldCoverage:
    """Test field_coverage function."""

    def test_coverage_empty(self):
        """Empty records should return empty dict."""
        assert field_coverage([]) == {}

    def test_coverage_all_records_have_field(self):
        """Field present in all records → 1.0."""
        records = [{"id": 1}, {"id": 2}, {"id": 3}]
        coverage = field_coverage(records)
        assert coverage == {"id": 1.0}

    def test_coverage_partial(self):
        """Field present in some records → 0.0–1.0."""
        records = [
            {"id": 1, "name": "Alice"},
            {"id": 2},
            {"id": 3, "name": "Charlie"},
        ]
        coverage = field_coverage(records)
        assert coverage["id"] == 1.0
        assert coverage["name"] == 2 / 3  # 2 of 3 records have "name"

    def test_coverage_multiple_fields(self):
        """Multiple fields with varying coverage."""
        records = [
            {"a": 1, "b": "x", "c": True},
            {"a": 2, "b": "y"},
            {"a": 3},
        ]
        coverage = field_coverage(records)
        assert coverage["a"] == 1.0
        assert coverage["b"] == 2 / 3
        assert coverage["c"] == 1 / 3


class TestTypeHistogram:
    """Test type_histogram function."""

    def test_histogram_single_type(self):
        """All values of same type."""
        records = [{"count": 1}, {"count": 2}, {"count": 3}]
        histogram = type_histogram(records)
        assert histogram == {"count": {"int": 3}}

    def test_histogram_mixed_types(self):
        """Same field with different types across records."""
        records = [
            {"value": 42},
            {"value": "hello"},
            {"value": 3.14},
            {"value": True},
            {"value": None},
        ]
        histogram = type_histogram(records)
        assert histogram["value"] == {
            "int": 1,
            "str": 1,
            "float": 1,
            "bool": 1,
            "NoneType": 1,
        }

    def test_histogram_multiple_fields(self):
        """Multiple fields each with type counts."""
        records = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "tags": ["x", "y"]},
        ]
        histogram = type_histogram(records)
        assert histogram["id"] == {"int": 3}
        assert histogram["name"] == {"str": 2}
        assert histogram["tags"] == {"list": 1}

    def test_histogram_complex_types(self):
        """Nested structures (dict, list)."""
        records = [
            {"data": {"nested": True}},
            {"data": [1, 2, 3]},
        ]
        histogram = type_histogram(records)
        assert histogram["data"] == {"dict": 1, "list": 1}


class TestBuildReport:
    """Test build_report function."""

    def test_build_report_structure(self):
        """Report has correct keys and types."""
        records = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]
        report = build_report(records)
        assert "count" in report
        assert "coverage" in report
        assert "types" in report
        assert report["count"] == 2
        assert isinstance(report["coverage"], dict)
        assert isinstance(report["types"], dict)

    def test_build_report_complete(self):
        """Full report with mixed coverage and types."""
        records = [
            {"id": 1, "name": "Alice", "active": True},
            {"id": 2, "name": "Bob"},
            {"id": 3, "score": 95.5},
        ]
        report = build_report(records)
        assert report["count"] == 3
        assert report["coverage"]["id"] == 1.0
        assert report["coverage"]["name"] == 2 / 3
        assert report["coverage"]["active"] == 1 / 3
        assert report["coverage"]["score"] == 1 / 3
        assert report["types"]["id"] == {"int": 3}
        assert report["types"]["name"] == {"str": 2}
        assert report["types"]["active"] == {"bool": 1}
        assert report["types"]["score"] == {"float": 1}
