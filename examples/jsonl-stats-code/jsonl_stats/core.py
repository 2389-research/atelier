"""Core stats functions for JSONL analysis."""

import json
from typing import Any


def load_records(path: str) -> list[dict]:
    """Parse a .jsonl file into a list of dicts; skip blank lines."""
    records = []
    with open(path, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped:  # skip blank lines
                records.append(json.loads(stripped))
    return records


def count_records(records: list[dict]) -> int:
    """Return the number of records."""
    return len(records)


def field_coverage(records: list[dict]) -> dict[str, float]:
    """Return field name -> fraction (0.0–1.0) of records containing that field."""
    if not records:
        return {}

    field_counts: dict[str, int] = {}
    for record in records:
        for field in record.keys():
            field_counts[field] = field_counts.get(field, 0) + 1

    total = len(records)
    return {field: count / total for field, count in field_counts.items()}


def type_histogram(records: list[dict]) -> dict[str, dict[str, int]]:
    """Return field name -> {python_type_name -> count} over records with the field."""
    histograms: dict[str, dict[str, int]] = {}

    for record in records:
        for field, value in record.items():
            type_name = type(value).__name__
            if field not in histograms:
                histograms[field] = {}
            histograms[field][type_name] = histograms[field].get(type_name, 0) + 1

    return histograms


def build_report(records: list[dict]) -> dict:
    """Assemble a report with count, coverage, and type histogram."""
    return {
        "count": count_records(records),
        "coverage": field_coverage(records),
        "types": type_histogram(records),
    }
