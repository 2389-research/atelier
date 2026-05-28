"""jsonl_stats — analyze JSON Lines files."""

from jsonl_stats.core import (
    build_report,
    count_records,
    field_coverage,
    load_records,
    type_histogram,
)

__all__ = [
    "load_records",
    "count_records",
    "field_coverage",
    "type_histogram",
    "build_report",
]
