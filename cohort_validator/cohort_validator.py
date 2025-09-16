#!/usr/bin/env python3
"""
Cohort Validator - Python interface to OHDSI CIRCE Java validation library

This module provides a Python interface to the OHDSI CIRCE cohort validation library
using JPype1. It allows validation of cohort JSON expressions and returns warnings
and errors in a Python-friendly format.

Usage:
    from cohort_validator import CohortValidator

    validator = CohortValidator()
    warnings, errors = validator.validate_cohort(cohort_data_dict)
"""

import json
import os
from typing import Any, Dict, List, Tuple

import jpype
import jpype.imports
from jpype.types import *


class CohortValidator:
    """
    Python wrapper for OHDSI CIRCE cohort validation library.

    This class provides a Python interface to validate cohort expressions
    using the Java CIRCE library via JPype1.
    """

    def __init__(self, jar_path: str = None):
        """
        Initialize the cohort validator.

        Args:
            jar_path: Path to the CIRCE JAR file. If None, uses default path.
        """
        self._jvm_started = False
        self._jar_path = jar_path or self._get_default_jar_path()
        self._dependencies_path = self._get_dependencies_path()
        self._checker = None
        self._cohort_expression_class = None
        self._warning_class = None
        self._warning_severity_class = None

        self._start_jvm()
        self._load_classes()

    def _get_default_jar_path(self) -> str:
        """Get the default path to the CIRCE JAR file."""
        import pkg_resources

        # Try to find JAR in package data first
        try:
            jar_path = pkg_resources.resource_filename(
                "cohort_validator", "../circe-be/target/circe-1.13.0-SNAPSHOT.jar"
            )
            if os.path.exists(jar_path):
                return jar_path
        except:
            pass

        # Fallback to relative path from package directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        jar_path = os.path.join(
            current_dir, "..", "circe-be", "target", "circe-1.13.0-SNAPSHOT.jar"
        )
        abs_path = os.path.abspath(jar_path)
        print(f"DEBUG: Looking for JAR at: {abs_path}")
        print(f"DEBUG: JAR exists: {os.path.exists(abs_path)}")
        return abs_path

    def _get_dependencies_path(self) -> str:
        """Get the path to the dependencies directory."""
        import pkg_resources

        # Try to find dependencies in package data first
        try:
            deps_path = pkg_resources.resource_filename(
                "cohort_validator", "../circe-be/target/dependencies"
            )
            if os.path.exists(deps_path):
                return deps_path
        except:
            pass

        # Fallback to relative path from package directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        deps_path = os.path.join(
            current_dir, "..", "circe-be", "target", "dependencies"
        )
        abs_path = os.path.abspath(deps_path)
        print(f"DEBUG: Looking for dependencies at: {abs_path}")
        print(f"DEBUG: Dependencies exist: {os.path.exists(abs_path)}")
        return abs_path

    def _start_jvm(self):
        """Start the JVM and load the CIRCE library."""
        if self._jvm_started:
            return

        # Get all JAR files
        jar_files = [self._jar_path]

        # Add all dependency JAR files
        if os.path.exists(self._dependencies_path):
            for file in os.listdir(self._dependencies_path):
                if file.endswith(".jar"):
                    jar_files.append(os.path.join(self._dependencies_path, file))

        # Create classpath
        classpath = ":".join(jar_files)

        # Start JVM
        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=classpath)

        self._jvm_started = True

    def _load_classes(self):
        """Load the necessary Java classes."""
        try:
            # Import the main classes
            from org.ohdsi.circe.check import Checker, Warning, WarningSeverity
            from org.ohdsi.circe.cohortdefinition import CohortExpression

            self._checker = Checker()
            self._cohort_expression_class = CohortExpression
            self._warning_class = Warning
            self._warning_severity_class = WarningSeverity

        except Exception as e:
            raise RuntimeError(f"Failed to load Java classes: {e}")

    def validate_cohort(
        self, cohort_json: dict
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Validate a cohort expression dictionary.

        Args:
            cohort_json: Dictionary representing the cohort expression

        Returns:
            Tuple of (warnings, errors) where each is a list of dictionaries
            containing validation results
        """
        try:
            # Create CohortExpression from JSON
            cohort_expression = self._cohort_expression_class.fromJson(
                json.dumps(cohort_json)
            )

            # Run validation
            java_warnings = self._checker.check(cohort_expression)

            # Convert Java warnings to Python dictionaries
            warnings = []
            errors = []

            for java_warning in java_warnings:
                warning_dict = {
                    "message": str(java_warning.toMessage()),
                    "severity": (
                        str(java_warning.getSeverity())
                        if hasattr(java_warning, "getSeverity")
                        else "UNKNOWN"
                    ),
                    "type": str(java_warning.getClass().getSimpleName()),
                }

                # Categorize as warning or error based on severity
                severity = warning_dict["severity"].upper()
                if severity in ["CRITICAL", "ERROR"]:
                    errors.append(warning_dict)
                else:
                    warnings.append(warning_dict)

            return warnings, errors

        except json.JSONDecodeError as e:
            return [], [
                {
                    "message": f"Invalid JSON: {e}",
                    "severity": "CRITICAL",
                    "type": "JSON_ERROR",
                }
            ]
        except Exception as e:
            return [], [
                {
                    "message": f"Validation error: {e}",
                    "severity": "CRITICAL",
                    "type": "VALIDATION_ERROR",
                }
            ]

    def validate_cohort_file(
        self, file_path: str
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Validate a cohort expression from a JSON file.

        Args:
            file_path: Path to the JSON file containing the cohort expression

        Returns:
            Tuple of (warnings, errors) where each is a list of dictionaries
            containing validation results
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                cohort_json = f.read()
            return self.validate_cohort(cohort_json)
        except FileNotFoundError:
            return [], [
                {
                    "message": f"File not found: {file_path}",
                    "severity": "CRITICAL",
                    "type": "FILE_ERROR",
                }
            ]
        except Exception as e:
            return [], [
                {
                    "message": f"File read error: {e}",
                    "severity": "CRITICAL",
                    "type": "FILE_ERROR",
                }
            ]

    def shutdown(self):
        """Shutdown the JVM."""
        if jpype.isJVMStarted():
            jpype.shutdownJVM()
        self._jvm_started = False


def main():
    """Example usage of the CohortValidator."""
    import sys

    if len(sys.argv) != 2:
        print("Usage: python cohort_validator.py <cohort_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        validator = CohortValidator()
        warnings, errors = validator.validate_cohort_file(file_path)

        print(f"Validation Results for {file_path}:")
        print(f"Warnings: {len(warnings)}")
        print(f"Errors: {len(errors)}")

        if warnings:
            print("\nWarnings:")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. [{warning['severity']}] {warning['message']}")

        if errors:
            print("\nErrors:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. [{error['severity']}] {error['message']}")

        if not warnings and not errors:
            print("\nNo validation issues found!")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if "validator" in locals():
            validator.shutdown()


if __name__ == "__main__":
    main()
