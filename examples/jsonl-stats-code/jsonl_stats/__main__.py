"""Command-line interface for jsonl_stats."""

import argparse
import sys
from jsonl_stats.core import load_records, build_report


def main() -> None:
    """Parse a JSONL file and print a stats report."""
    parser = argparse.ArgumentParser(
        description="Analyze a JSON Lines file and report statistics."
    )
    parser.add_argument("path", help="Path to the JSONL file")
    args = parser.parse_args()

    try:
        records = load_records(args.path)
        report = build_report(records)

        # Print readable report
        print(f"Record count: {report['count']}")
        print("\nField coverage:")
        for field, coverage in sorted(report["coverage"].items()):
            percentage = coverage * 100
            print(f"  {field}: {percentage:.1f}%")

        print("\nType histogram:")
        for field, type_counts in sorted(report["types"].items()):
            print(f"  {field}:")
            for type_name, count in sorted(type_counts.items()):
                print(f"    {type_name}: {count}")

        sys.exit(0)

    except FileNotFoundError:
        print(f"Error: File not found: {args.path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
