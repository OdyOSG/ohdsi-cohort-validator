#!/usr/bin/env python3
"""
Simple comprehensive test suite for the CohortValidator.

This script tests the cohort validation functionality with a focused set
of CIRCE test files that are known to work well.
"""

import json
import os
from typing import Any, Dict, List

from cohort_validator import CohortValidator


def test_cohort_file(
    validator: CohortValidator,
    test_name: str,
    test_file: str,
    expect_errors: bool = False,
    min_warnings: int = 0,
) -> Dict[str, Any]:
    """
    Test a single cohort file.

    Args:
        validator: The cohort validator instance
        test_name: Name of the test
        test_file: Path to the test file
        expect_errors: Whether errors are expected
        min_warnings: Minimum number of warnings expected

    Returns:
        Dictionary with test results
    """
    result = {
        "name": test_name,
        "file": test_file,
        "passed": False,
        "warnings": [],
        "errors": [],
        "error_message": None,
    }

    try:
        if not os.path.exists(test_file):
            result["error_message"] = f"Test file not found: {test_file}"
            return result

        warnings, errors = validator.validate_cohort_file(test_file)
        result["warnings"] = warnings
        result["errors"] = errors

        # Check if test passed based on expectations
        if expect_errors:
            result["passed"] = len(errors) > 0
            if not result["passed"]:
                result["error_message"] = (
                    f"Expected errors but found none. Found {len(warnings)} warnings instead."
                )
        else:
            result["passed"] = len(errors) == 0 and len(warnings) >= min_warnings
            if not result["passed"]:
                if len(errors) > 0:
                    result["error_message"] = (
                        f"Expected no errors but found {len(errors)} errors."
                    )
                elif len(warnings) < min_warnings:
                    result["error_message"] = (
                        f"Expected at least {min_warnings} warnings but found {len(warnings)}."
                    )

    except Exception as e:
        result["error_message"] = f"Test failed with exception: {e}"

    return result


def run_test_suite(validator: CohortValidator) -> List[Dict[str, Any]]:
    """Run a comprehensive test suite."""
    print("CIRCE Cohort Validator - Simple Comprehensive Test Suite")
    print("=" * 70)

    # Define test cases with their expectations
    test_cases = [
        # Correct cohorts (should have minimal errors, some warnings OK)
        (
            "Primary Criteria Correct",
            "circe-be/src/test/resources/checkers/primaryCriteriaCheckValueCorrect.json",
            False,
            0,
        ),
        (
            "Additional Criteria Correct",
            "circe-be/src/test/resources/checkers/additionalCriteriaCheckValueCorrect.json",
            False,
            0,
        ),
        (
            "Concept Set Criteria Correct",
            "circe-be/src/test/resources/checkers/conceptSetCriteriaCheckCorrect.json",
            False,
            0,
        ),
        (
            "Unused Concept Set Correct",
            "circe-be/src/test/resources/checkers/unusedConceptSetCorrect.json",
            False,
            0,
        ),
        (
            "Duplicates Concept Set Correct",
            "circe-be/src/test/resources/checkers/duplicatesConceptSetCheckCorrect.json",
            False,
            0,
        ),
        (
            "Duplicates Criteria Correct",
            "circe-be/src/test/resources/checkers/duplicatesCriteriaCheckCorrect.json",
            False,
            0,
        ),
        (
            "Domain Type Correct",
            "circe-be/src/test/resources/checkers/domainTypeCheckCorrect.json",
            False,
            0,
        ),
        (
            "Drug Domain Correct",
            "circe-be/src/test/resources/checkers/drugDomainCheckCorrect.json",
            False,
            0,
        ),
        (
            "Drug Era Correct",
            "circe-be/src/test/resources/checkers/drugEraCheckCorrect.json",
            False,
            0,
        ),
        (
            "Death Time Window Correct",
            "circe-be/src/test/resources/checkers/deathTimeWindowCheckCorrect.json",
            False,
            0,
        ),
        (
            "Time Pattern Correct",
            "circe-be/src/test/resources/checkers/timePatternCheckCorrect.json",
            False,
            0,
        ),
        (
            "Events Progression Correct",
            "circe-be/src/test/resources/checkers/eventsProgressionCheckCorrect.json",
            False,
            0,
        ),
        (
            "Contradictions Criteria Correct",
            "circe-be/src/test/resources/checkers/contradictionsCriteriaCheckCorrect.json",
            False,
            0,
        ),
        (
            "Inclusion Rules Correct",
            "circe-be/src/test/resources/checkers/inclusionRulesCheckValueCorrect.json",
            False,
            0,
        ),
        (
            "Censoring Event Correct",
            "circe-be/src/test/resources/checkers/censoringEventCheckValueCorrect.json",
            False,
            0,
        ),
        (
            "Empty Demographic Correct",
            "circe-be/src/test/resources/checkers/emptyDemographicCheckCorrect.json",
            False,
            0,
        ),
        # Complex correct cohorts
        (
            "Child Group Expression",
            "circe-be/src/test/resources/checkers/childGroupExpression.json",
            False,
            0,
        ),
        (
            "All Criteria Expression",
            "circe-be/src/test/resources/cohortgeneration/allCriteria/allCriteriaExpression.json",
            False,
            0,
        ),
        (
            "Censor Window Expression",
            "circe-be/src/test/resources/cohortgeneration/censorWindow/censorWindowExpression.json",
            False,
            0,
        ),
        (
            "Era Dupes Expression",
            "circe-be/src/test/resources/cohortgeneration/eraDupes/eraDupesExpression.json",
            False,
            0,
        ),
        (
            "Counts Expression",
            "circe-be/src/test/resources/cohortgeneration/correlatedCriteria/countsExpression.json",
            False,
            0,
        ),
        (
            "Group Expression",
            "circe-be/src/test/resources/cohortgeneration/correlatedCriteria/groupExpression.json",
            False,
            0,
        ),
        (
            "Visit Expression",
            "circe-be/src/test/resources/cohortgeneration/correlatedCriteria/visitExpression.json",
            False,
            0,
        ),
        (
            "First Occurrence Expression",
            "circe-be/src/test/resources/cohortgeneration/firstOccurrence/firstOccurrenceExpression.json",
            False,
            0,
        ),
        (
            "Inclusion Rules Expression",
            "circe-be/src/test/resources/cohortgeneration/inclusionRules/inclusionRulesExpression.json",
            False,
            0,
        ),
        (
            "Limits Expression",
            "circe-be/src/test/resources/cohortgeneration/limits/limitsExpression.json",
            False,
            0,
        ),
        (
            "Mixed Concept Sets Expression",
            "circe-be/src/test/resources/cohortgeneration/mixedConceptsets/mixedConceptsetsExpression.json",
            False,
            0,
        ),
        (
            "Dupilumab Expression",
            "circe-be/src/test/resources/conceptset/dupilumabExpression.json",
            False,
            0,
        ),
        (
            "Dupixent Expression",
            "circe-be/src/test/resources/conceptset/dupixentExpression.json",
            False,
            0,
        ),
        (
            "Payer Plan Cohort Expression",
            "circe-be/src/test/resources/versioning/payerPlanCohortExpression.json",
            False,
            0,
        ),
        # Incorrect cohorts (should have errors)
        (
            "Primary Criteria Incorrect",
            "circe-be/src/test/resources/checkers/primaryCriteriaCheckValueIncorrect.json",
            True,
            0,
        ),
        (
            "Additional Criteria Incorrect",
            "circe-be/src/test/resources/checkers/additionalCriteriaCheckValueIncorrect.json",
            True,
            0,
        ),
        (
            "Concept Set Criteria Incorrect",
            "circe-be/src/test/resources/checkers/conceptSetCriteriaCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Unused Concept Set",
            "circe-be/src/test/resources/checkers/unusedConceptSet.json",
            False,
            10,
        ),  # Should have many warnings
        (
            "Duplicates Concept Set Incorrect",
            "circe-be/src/test/resources/checkers/duplicatesConceptSetCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Duplicates Criteria Incorrect",
            "circe-be/src/test/resources/checkers/duplicatesCriteriaCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Domain Type Incorrect",
            "circe-be/src/test/resources/checkers/domainTypeCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Drug Domain Incorrect",
            "circe-be/src/test/resources/checkers/drugDomainCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Drug Era Incorrect",
            "circe-be/src/test/resources/checkers/drugEraCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Death Time Window Incorrect",
            "circe-be/src/test/resources/checkers/deathTimeWindowCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Time Pattern Incorrect",
            "circe-be/src/test/resources/checkers/timePatternCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Events Progression Incorrect",
            "circe-be/src/test/resources/checkers/eventsProgressionCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Contradictions Criteria Incorrect",
            "circe-be/src/test/resources/checkers/contradictionsCriteriaCheckIncorrect.json",
            True,
            0,
        ),
        (
            "Inclusion Rules Incorrect",
            "circe-be/src/test/resources/checkers/inclusionRulesCheckValueIncorrect.json",
            True,
            0,
        ),
        (
            "Censoring Event Incorrect",
            "circe-be/src/test/resources/checkers/censoringEventCheckValueIncorrect.json",
            True,
            0,
        ),
        (
            "Empty Demographic Incorrect",
            "circe-be/src/test/resources/checkers/emptyDemographicCheckIncorrect.json",
            True,
            0,
        ),
    ]

    results = []
    passed = 0
    total = len(test_cases)

    print(f"Running {total} test cases...\n")

    for i, (name, file_path, expect_errors, min_warnings) in enumerate(test_cases, 1):
        print(f"[{i:2d}/{total}] Testing: {name}")

        result = test_cohort_file(
            validator, name, file_path, expect_errors, min_warnings
        )
        results.append(result)

        if result["passed"]:
            passed += 1
            status = "✅ PASSED"
        else:
            status = "❌ FAILED"

        print(
            f"         {status} - Warnings: {len(result['warnings'])}, Errors: {len(result['errors'])}"
        )
        if result["error_message"]:
            print(f"         Error: {result['error_message']}")
        print()

    return results, passed, total


def print_detailed_results(results: List[Dict[str, Any]], passed: int, total: int):
    """Print detailed test results."""
    print("=" * 70)
    print("DETAILED TEST RESULTS")
    print("=" * 70)

    print(f"Overall Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    # Group results by category
    correct_tests = [
        r
        for r in results
        if not r["name"].endswith("Incorrect") and not r["name"] == "Unused Concept Set"
    ]
    incorrect_tests = [
        r
        for r in results
        if r["name"].endswith("Incorrect") or r["name"] == "Unused Concept Set"
    ]

    print(
        f"\nCorrect Cohorts: {sum(1 for r in correct_tests if r['passed'])}/{len(correct_tests)} passed"
    )
    print(
        f"Incorrect Cohorts: {sum(1 for r in incorrect_tests if r['passed'])}/{len(incorrect_tests)} passed"
    )

    # Show failed tests
    failed_tests = [r for r in results if not r["passed"]]
    if failed_tests:
        print(f"\nFailed Tests ({len(failed_tests)}):")
        for test in failed_tests:
            print(f"  - {test['name']}: {test['error_message'] or 'Unexpected result'}")

    # Show validation statistics
    total_warnings = sum(len(r["warnings"]) for r in results)
    total_errors = sum(len(r["errors"]) for r in results)
    print(f"\nValidation Statistics:")
    print(f"  Total Warnings Found: {total_warnings}")
    print(f"  Total Errors Found: {total_errors}")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The cohort validator is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check the details above.")


def main():
    """Run the simple comprehensive test suite."""
    validator = CohortValidator()

    try:
        results, passed, total = run_test_suite(validator)
        print_detailed_results(results, passed, total)

    finally:
        validator.shutdown()
        print("\nValidator shutdown complete.")


if __name__ == "__main__":
    main()
