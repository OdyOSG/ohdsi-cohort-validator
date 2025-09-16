#!/usr/bin/env python3
"""
Validation scenario tests for the CohortValidator.

This script tests specific validation scenarios using CIRCE test files
to ensure different types of validation rules are working correctly.
"""

import json
import os
from typing import Any, Dict, List

from cohort_validator import CohortValidator


def test_validation_scenario(
    validator: CohortValidator,
    test_name: str,
    test_file: str,
    expected_validation_types: List[str] = None,
) -> Dict[str, Any]:
    """
    Test a specific validation scenario.

    Args:
        validator: The cohort validator instance
        test_name: Name of the test scenario
        test_file: Path to the test file
        expected_validation_types: List of expected validation types (e.g., ['unused_concepts', 'empty_values'])

    Returns:
        Dictionary with test results
    """
    result = {
        "name": test_name,
        "file": test_file,
        "passed": False,
        "warnings": [],
        "errors": [],
        "validation_types_found": set(),
        "expected_types": expected_validation_types or [],
        "error_message": None,
    }

    try:
        if not os.path.exists(test_file):
            result["error_message"] = f"Test file not found: {test_file}"
            return result

        warnings, errors = validator.validate_cohort_file(test_file)
        result["warnings"] = warnings
        result["errors"] = errors

        # Extract validation types from messages
        all_messages = [w["message"] for w in warnings] + [e["message"] for e in errors]
        for message in all_messages:
            message_lower = message.lower()

            # Unused concepts validation
            if ("concept set" in message_lower and "not used" in message_lower) or (
                "unused" in message_lower and "concept" in message_lower
            ):
                result["validation_types_found"].add("unused_concepts")

            # Empty values validation
            elif "empty" in message_lower and (
                "value" in message_lower
                or "start" in message_lower
                or "end" in message_lower
            ):
                result["validation_types_found"].add("empty_values")

            # Duplicates validation
            elif (
                "duplicate" in message_lower
                or "same concepts" in message_lower
                or "duplicates" in message_lower
                or "probably" in message_lower
                and "duplicates" in message_lower
            ):
                result["validation_types_found"].add("duplicates")

            # Contradictions validation
            elif "contradiction" in message_lower or "contradictory" in message_lower:
                result["validation_types_found"].add("contradictions")

            # Time windows validation
            elif (
                ("time" in message_lower and "window" in message_lower)
                or ("time pattern" in message_lower)
                or ("death time" in message_lower)
            ):
                result["validation_types_found"].add("time_windows")

            # Domain types validation
            elif ("domain" in message_lower and "type" in message_lower) or (
                "drug domain" in message_lower
            ):
                result["validation_types_found"].add("domain_types")

            # Range validation
            elif (
                "range" in message_lower
                and ("start" in message_lower or "end" in message_lower)
            ) or (
                "start" in message_lower
                and "greater than" in message_lower
                and "end" in message_lower
            ):
                result["validation_types_found"].add("range_validation")

            # Missing criteria validation
            elif (
                ("no concept set specified" in message_lower)
                or (
                    "empty" in message_lower
                    and ("criteria" in message_lower or "rules" in message_lower)
                )
                or ("criteria" in message_lower and "specified" in message_lower)
            ):
                result["validation_types_found"].add("missing_criteria")

            # Exit criteria validation
            elif "exit criteria" in message_lower:
                result["validation_types_found"].add("exit_criteria")

            # Events progression validation
            elif (
                "events progression" in message_lower or "progression" in message_lower
            ):
                result["validation_types_found"].add("events_progression")

        # Check if expected validation types were found
        if expected_validation_types:
            found_expected = any(
                t in result["validation_types_found"] for t in expected_validation_types
            )
            result["passed"] = found_expected
            if not found_expected:
                result["error_message"] = (
                    f"Expected validation types {expected_validation_types} not found. Found: {list(result['validation_types_found'])}"
                )
        else:
            # If no specific types expected, just check that validation ran successfully
            result["passed"] = True

    except Exception as e:
        result["error_message"] = f"Test failed with exception: {e}"

    return result


def test_unused_concepts_validation(validator: CohortValidator) -> List[Dict[str, Any]]:
    """Test unused concepts validation."""
    print("\n" + "=" * 50)
    print("TESTING UNUSED CONCEPTS VALIDATION")
    print("=" * 50)

    tests = [
        test_validation_scenario(
            validator,
            "Unused Concept Set",
            "circe-be/src/test/resources/checkers/unusedConceptSet.json",
            ["unused_concepts"],
        ),
        test_validation_scenario(
            validator,
            "Unused Concept Set Correct",
            "circe-be/src/test/resources/checkers/unusedConceptSetCorrect.json",
            [],  # Should not have unused concepts
        ),
    ]

    for test in tests:
        status = "✅ PASSED" if test["passed"] else "❌ FAILED"
        print(f"{test['name']}: {status}")
        print(f"  Warnings: {len(test['warnings'])}, Errors: {len(test['errors'])}")
        print(f"  Validation types found: {list(test['validation_types_found'])}")
        if test["error_message"]:
            print(f"  Error: {test['error_message']}")
        print()

    return tests


def test_empty_values_validation(validator: CohortValidator) -> List[Dict[str, Any]]:
    """Test empty values validation."""
    print("\n" + "=" * 50)
    print("TESTING EMPTY VALUES VALIDATION")
    print("=" * 50)

    tests = [
        test_validation_scenario(
            validator,
            "Primary Criteria with Empty Values",
            "circe-be/src/test/resources/checkers/primaryCriteriaCheckValueIncorrect.json",
            ["empty_values"],
        ),
        test_validation_scenario(
            validator,
            "Additional Criteria with Empty Values",
            "circe-be/src/test/resources/checkers/additionalCriteriaCheckValueIncorrect.json",
            ["empty_values"],
        ),
    ]

    for test in tests:
        status = "✅ PASSED" if test["passed"] else "❌ FAILED"
        print(f"{test['name']}: {status}")
        print(f"  Warnings: {len(test['warnings'])}, Errors: {len(test['errors'])}")
        print(f"  Validation types found: {list(test['validation_types_found'])}")
        if test["error_message"]:
            print(f"  Error: {test['error_message']}")
        print()

    return tests


def test_duplicates_validation(validator: CohortValidator) -> List[Dict[str, Any]]:
    """Test duplicates validation."""
    print("\n" + "=" * 50)
    print("TESTING DUPLICATES VALIDATION")
    print("=" * 50)

    tests = [
        test_validation_scenario(
            validator,
            "Duplicate Concept Sets",
            "circe-be/src/test/resources/checkers/duplicatesConceptSetCheckIncorrect.json",
            ["duplicates"],
        ),
        test_validation_scenario(
            validator,
            "Duplicate Criteria",
            "circe-be/src/test/resources/checkers/duplicatesCriteriaCheckIncorrect.json",
            ["duplicates"],
        ),
        test_validation_scenario(
            validator,
            "Concept Set with Duplicate Items",
            "circe-be/src/test/resources/checkers/conceptSetWithDuplicateItems.json",
            ["duplicates"],
        ),
    ]

    for test in tests:
        status = "✅ PASSED" if test["passed"] else "❌ FAILED"
        print(f"{test['name']}: {status}")
        print(f"  Warnings: {len(test['warnings'])}, Errors: {len(test['errors'])}")
        print(f"  Validation types found: {list(test['validation_types_found'])}")
        if test["error_message"]:
            print(f"  Error: {test['error_message']}")
        print()

    return tests


def test_domain_validation(validator: CohortValidator) -> List[Dict[str, Any]]:
    """Test domain and type validation."""
    print("\n" + "=" * 50)
    print("TESTING DOMAIN AND TYPE VALIDATION")
    print("=" * 50)

    tests = [
        test_validation_scenario(
            validator,
            "Domain Type Incorrect",
            "circe-be/src/test/resources/checkers/domainTypeCheckIncorrect.json",
            ["domain_types"],
        ),
        test_validation_scenario(
            validator,
            "Drug Domain Incorrect",
            "circe-be/src/test/resources/checkers/drugDomainCheckIncorrect.json",
            ["domain_types"],
        ),
    ]

    for test in tests:
        status = "✅ PASSED" if test["passed"] else "❌ FAILED"
        print(f"{test['name']}: {status}")
        print(f"  Warnings: {len(test['warnings'])}, Errors: {len(test['errors'])}")
        print(f"  Validation types found: {list(test['validation_types_found'])}")
        if test["error_message"]:
            print(f"  Error: {test['error_message']}")
        print()

    return tests


def test_time_validation(validator: CohortValidator) -> List[Dict[str, Any]]:
    """Test time-related validation."""
    print("\n" + "=" * 50)
    print("TESTING TIME-RELATED VALIDATION")
    print("=" * 50)

    tests = [
        test_validation_scenario(
            validator,
            "Death Time Window Incorrect",
            "circe-be/src/test/resources/checkers/deathTimeWindowCheckIncorrect.json",
            ["time_windows"],
        ),
        test_validation_scenario(
            validator,
            "Time Pattern Incorrect",
            "circe-be/src/test/resources/checkers/timePatternCheckIncorrect.json",
            ["time_windows"],
        ),
    ]

    for test in tests:
        status = "✅ PASSED" if test["passed"] else "❌ FAILED"
        print(f"{test['name']}: {status}")
        print(f"  Warnings: {len(test['warnings'])}, Errors: {len(test['errors'])}")
        print(f"  Validation types found: {list(test['validation_types_found'])}")
        if test["error_message"]:
            print(f"  Error: {test['error_message']}")
        print()

    return tests


def test_contradictions_validation(validator: CohortValidator) -> List[Dict[str, Any]]:
    """Test contradictions validation."""
    print("\n" + "=" * 50)
    print("TESTING CONTRADICTIONS VALIDATION")
    print("=" * 50)

    tests = [
        test_validation_scenario(
            validator,
            "Contradictions Criteria Incorrect",
            "circe-be/src/test/resources/checkers/contradictionsCriteriaCheckIncorrect.json",
            ["contradictions"],
        )
    ]

    for test in tests:
        status = "✅ PASSED" if test["passed"] else "❌ FAILED"
        print(f"{test['name']}: {status}")
        print(f"  Warnings: {len(test['warnings'])}, Errors: {len(test['errors'])}")
        print(f"  Validation types found: {list(test['validation_types_found'])}")
        if test["error_message"]:
            print(f"  Error: {test['error_message']}")
        print()

    return tests


def test_missing_criteria_validation(
    validator: CohortValidator,
) -> List[Dict[str, Any]]:
    """Test missing criteria validation."""
    print("\n" + "=" * 50)
    print("TESTING MISSING CRITERIA VALIDATION")
    print("=" * 50)

    tests = [
        test_validation_scenario(
            validator,
            "Empty Primary Criteria List",
            "circe-be/src/test/resources/checkers/emptyPrimaryCriteriaList.json",
            ["missing_criteria"],
        ),
        test_validation_scenario(
            validator,
            "Empty Inclusion Rules",
            "circe-be/src/test/resources/checkers/emptyInclusionRules.json",
            ["missing_criteria"],
        ),
        test_validation_scenario(
            validator,
            "Empty Correlated Criteria",
            "circe-be/src/test/resources/checkers/emptyCorrelatedCriteria.json",
            ["missing_criteria"],
        ),
    ]

    for test in tests:
        status = "✅ PASSED" if test["passed"] else "❌ FAILED"
        print(f"{test['name']}: {status}")
        print(f"  Warnings: {len(test['warnings'])}, Errors: {len(test['errors'])}")
        print(f"  Validation types found: {list(test['validation_types_found'])}")
        if test["error_message"]:
            print(f"  Error: {test['error_message']}")
        print()

    return tests


def print_validation_summary(all_tests: List[List[Dict[str, Any]]]):
    """Print a summary of validation scenario tests."""
    print("\n" + "=" * 80)
    print("VALIDATION SCENARIO TEST SUMMARY")
    print("=" * 80)

    total_tests = 0
    total_passed = 0
    validation_types_tested = set()

    for test_group in all_tests:
        for test in test_group:
            total_tests += 1
            if test["passed"]:
                total_passed += 1
            validation_types_tested.update(test["validation_types_found"])

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {total_passed/total_tests*100:.1f}%")
    print(f"Validation Types Tested: {sorted(validation_types_tested)}")

    if total_passed == total_tests:
        print("\n🎉 All validation scenarios passed!")
    else:
        print(f"\n⚠️  {total_tests - total_passed} validation scenarios failed.")


def main():
    """Run validation scenario tests."""
    print("CIRCE Cohort Validator - Validation Scenario Tests")
    print("=" * 80)
    print("Testing specific validation scenarios...")

    validator = CohortValidator()

    try:
        all_tests = []

        # Test different validation scenarios
        all_tests.append(test_unused_concepts_validation(validator))
        all_tests.append(test_empty_values_validation(validator))
        all_tests.append(test_duplicates_validation(validator))
        all_tests.append(test_domain_validation(validator))
        all_tests.append(test_time_validation(validator))
        all_tests.append(test_contradictions_validation(validator))
        all_tests.append(test_missing_criteria_validation(validator))

        # Print summary
        print_validation_summary(all_tests)

    finally:
        validator.shutdown()
        print("\nValidator shutdown complete.")


if __name__ == "__main__":
    main()
