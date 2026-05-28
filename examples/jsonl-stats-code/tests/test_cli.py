"""Integration tests for the jsonl_stats CLI."""

import subprocess
import sys


def test_cli_with_sample_file() -> None:
    """Test that the CLI runs successfully on the sample fixture and prints the record count."""
    result = subprocess.run(
        [sys.executable, "-m", "jsonl_stats", "tests/sample.jsonl"],
        cwd="/tmp/atelier-dogfood-code",
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI failed with: {result.stderr}"
    assert "Record count: 6" in result.stdout, f"Expected record count in output: {result.stdout}"


def test_cli_missing_file() -> None:
    """Test that the CLI exits with non-zero code on missing file."""
    result = subprocess.run(
        [sys.executable, "-m", "jsonl_stats", "/no/such/file.jsonl"],
        cwd="/tmp/atelier-dogfood-code",
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0, "CLI should exit non-zero on missing file"
    assert "Error" in result.stderr, f"Expected error message in stderr: {result.stderr}"
