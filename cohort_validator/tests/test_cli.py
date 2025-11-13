"""
Comprehensive unit tests for cli.py
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import CLI module
from cohort_validator.cli import format_text_output
import cohort_validator.cli as cli


class TestFormatTextOutput:
    """Tests for format_text_output function."""

    def test_format_text_output_with_warnings_and_errors(self):
        """Test format_text_output with warnings and errors."""
        result = {
            "input_file": "test.json",
            "warnings": [
                {"severity": "WARNING", "message": "Warning 1"},
                {"severity": "WARNING", "message": "Warning 2"},
            ],
            "errors": [
                {"severity": "CRITICAL", "message": "Error 1"},
            ],
            "summary": {
                "total_warnings": 2,
                "total_errors": 1,
                "is_valid": False,
            },
        }

        output = format_text_output(result)

        assert "test.json" in output
        assert "Warning 1" in output
        assert "Warning 2" in output
        assert "Error 1" in output
        assert "Total Warnings: 2" in output
        assert "Total Errors: 1" in output
        assert "Valid: No" in output

    def test_format_text_output_empty(self):
        """Test format_text_output with no warnings or errors."""
        result = {
            "input_file": "test.json",
            "warnings": [],
            "errors": [],
            "summary": {
                "total_warnings": 0,
                "total_errors": 0,
                "is_valid": True,
            },
        }

        output = format_text_output(result)

        assert "test.json" in output
        assert "Total Warnings: 0" in output
        assert "Total Errors: 0" in output
        assert "Valid: Yes" in output


class TestMain:
    """Tests for main() function."""

    def test_main_with_valid_file_json_output(self, tmp_path, sample_cohort_dict):
        """Test main() with valid file and JSON output."""
        # Create temporary cohort file
        cohort_file = tmp_path / "test_cohort.json"
        with open(cohort_file, "w") as f:
            json.dump(sample_cohort_dict, f)

        # Mock sys.argv
        test_args = [
            "cohort-validate",
            str(cohort_file),
            "--format",
            "json",
        ]

        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new=MagicMock()) as mock_stdout:
                with patch("sys.exit") as mock_exit:
                    cli.main()

                    # Should print JSON output
                    mock_stdout.write.assert_called()
                    # Should exit with 0 if valid
                    mock_exit.assert_called_once()

    def test_main_with_valid_file_text_output(self, tmp_path, sample_cohort_dict):
        """Test main() with valid file and text output."""
        cohort_file = tmp_path / "test_cohort.json"
        with open(cohort_file, "w") as f:
            json.dump(sample_cohort_dict, f)

        test_args = [
            "cohort-validate",
            str(cohort_file),
            "--format",
            "text",
        ]

        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new=MagicMock()) as mock_stdout:
                with patch("sys.exit") as mock_exit:
                    cli.main()

                    mock_stdout.write.assert_called()
                    mock_exit.assert_called()

    def test_main_with_output_file(self, tmp_path, sample_cohort_dict):
        """Test main() with output file specified."""
        cohort_file = tmp_path / "test_cohort.json"
        output_file = tmp_path / "output.json"

        with open(cohort_file, "w") as f:
            json.dump(sample_cohort_dict, f)

        test_args = [
            "cohort-validate",
            str(cohort_file),
            "--output",
            str(output_file),
            "--format",
            "json",
        ]

        with patch.object(sys, "argv", test_args):
            with patch("sys.exit") as mock_exit:
                cli.main()

                # Check if output file was created
                assert output_file.exists()
                mock_exit.assert_called()

    def test_main_with_nonexistent_file(self):
        """Test main() with non-existent file."""
        test_args = [
            "cohort-validate",
            "nonexistent_file.json",
        ]

        with patch.object(sys, "argv", test_args):
            with patch("sys.stderr", new=MagicMock()) as mock_stderr:
                with patch("sys.exit") as mock_exit:
                    cli.main()

                    # Should print error to stderr
                    mock_stderr.write.assert_called()
                    # Should exit with error code
                    mock_exit.assert_called_once_with(1)

