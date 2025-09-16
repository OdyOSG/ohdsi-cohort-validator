"""
Command-line interface for Cohort Validator.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from .cohort_validator import CohortValidator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate cohort expressions using OHDSI CIRCE library"
    )
    parser.add_argument(
        "input_file", type=str, help="Path to JSON file containing cohort expression"
    )
    parser.add_argument(
        "--output", "-o", type=str, help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--jar-path",
        type=str,
        help="Path to CIRCE JAR file (auto-detected if not provided)",
    )
    parser.add_argument(
        "--deps-path",
        type=str,
        help="Path to CIRCE dependencies directory (auto-detected if not provided)",
    )

    args = parser.parse_args()

    try:
        # Load cohort expression from file
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
            sys.exit(1)

        with open(input_path, "r", encoding="utf-8") as f:
            cohort_data = json.load(f)

        # Initialize validator
        validator_kwargs = {}
        if args.jar_path:
            validator_kwargs["jar_path"] = args.jar_path
        if args.deps_path:
            validator_kwargs["deps_path"] = args.deps_path

        validator = CohortValidator(**validator_kwargs)

        # Validate cohort
        warnings, errors = validator.validate_cohort(cohort_data)

        # Prepare output
        result = {
            "input_file": str(input_path),
            "warnings": warnings,
            "errors": errors,
            "summary": {
                "total_warnings": len(warnings),
                "total_errors": len(errors),
                "is_valid": len(errors) == 0,
            },
        }

        # Output results
        if args.format == "json":
            output = json.dumps(result, indent=2)
        else:
            output = format_text_output(result)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
        else:
            print(output)

        # Exit with appropriate code
        sys.exit(0 if len(errors) == 0 else 1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def format_text_output(result: Dict[str, Any]) -> str:
    """Format validation results as human-readable text."""
    lines = []
    lines.append(f"Validation Results for: {result['input_file']}")
    lines.append("=" * 50)

    summary = result["summary"]
    lines.append(f"Total Warnings: {summary['total_warnings']}")
    lines.append(f"Total Errors: {summary['total_errors']}")
    lines.append(f"Valid: {'Yes' if summary['is_valid'] else 'No'}")
    lines.append("")

    if result["warnings"]:
        lines.append("WARNINGS:")
        lines.append("-" * 20)
        for i, warning in enumerate(result["warnings"], 1):
            lines.append(
                f"{i}. [{warning.get('severity', 'UNKNOWN')}] {warning.get('message', 'No message')}"
            )
        lines.append("")

    if result["errors"]:
        lines.append("ERRORS:")
        lines.append("-" * 20)
        for i, error in enumerate(result["errors"], 1):
            lines.append(
                f"{i}. [{error.get('severity', 'UNKNOWN')}] {error.get('message', 'No message')}"
            )
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
