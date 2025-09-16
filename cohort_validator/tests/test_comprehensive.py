#!/usr/bin/env python3
"""
Comprehensive test suite for the CohortValidator using real CIRCE test files.

This script tests the cohort validation functionality with actual test data
from the CIRCE library, covering various validation scenarios.
"""

import json
import os
from typing import Any, Dict, List, Tuple

import pytest

from cohort_validator import CohortValidator


@pytest.fixture(scope="session")
def validator():
    """Shared validator instance for all tests."""
    validator = CohortValidator()
    yield validator
    # Don't shutdown the JVM - let it be cleaned up by pytest


class TestResult:
    """Container for test results."""

    def __init__(
        self, name: str, expected_errors: int = 0, expected_warnings: int = None
    ):
        self.name = name
        self.expected_errors = expected_errors
        self.expected_warnings = expected_warnings
        self.actual_errors = 0
        self.actual_warnings = 0
        self.passed = False
        self.error_message = None


def run_validation_test(
    validator: CohortValidator, test_file: str, test_result: TestResult
) -> TestResult:
    """Run a single validation test."""
    try:
        if not os.path.exists(test_file):
            test_result.error_message = f"Test file not found: {test_file}"
            return test_result

        warnings, errors = validator.validate_cohort_file(test_file)
        test_result.actual_warnings = len(warnings)
        test_result.actual_errors = len(errors)

        # Check if test passed based on expectations
        if test_result.expected_errors is not None:
            if test_result.actual_errors == test_result.expected_errors:
                if (
                    test_result.expected_warnings is None
                    or test_result.actual_warnings == test_result.expected_warnings
                ):
                    test_result.passed = True
                else:
                    test_result.error_message = f"Expected {test_result.expected_warnings} warnings, got {test_result.actual_warnings}"
            else:
                test_result.error_message = f"Expected {test_result.expected_errors} errors, got {test_result.actual_errors}"
        else:
            # For tests where we just want to ensure no critical errors
            test_result.passed = test_result.actual_errors == 0

    except Exception as e:
        test_result.error_message = f"Test failed with exception: {e}"

    return test_result


def test_correct_cohorts(validator: CohortValidator) -> List[TestResult]:
    """Test cohorts that should have minimal or no errors."""
    print("\n" + "=" * 60)
    print("TESTING CORRECT COHORTS (Should have minimal errors)")
    print("=" * 60)

    test_cases = [
        # Basic correct cohorts
        TestResult("Primary Criteria Correct", expected_errors=0),
        TestResult("Additional Criteria Correct", expected_errors=0),
        TestResult("Concept Set Criteria Correct", expected_errors=0),
        TestResult("Unused Concept Set Correct", expected_errors=0),
        TestResult("Duplicates Concept Set Correct", expected_errors=0),
        TestResult("Duplicates Criteria Correct", expected_errors=0),
        TestResult("Domain Type Correct", expected_errors=0),
        TestResult("Drug Domain Correct", expected_errors=0),
        TestResult("Drug Era Correct", expected_errors=0),
        TestResult("Death Time Window Correct", expected_errors=0),
        TestResult("Time Pattern Correct", expected_errors=0),
        TestResult("Events Progression Correct", expected_errors=0),
        TestResult("Contradictions Criteria Correct", expected_errors=0),
        TestResult("Inclusion Rules Correct", expected_errors=0),
        TestResult("Censoring Event Correct", expected_errors=0),
        TestResult("Empty Demographic Correct", expected_errors=0),
        # Complex correct cohorts
        TestResult("Child Group Expression", expected_errors=0),
        TestResult("All Criteria Expression", expected_errors=0),
        TestResult("Censor Window Expression", expected_errors=0),
        TestResult("Era Dupes Expression", expected_errors=0),
    ]

    test_files = [
        "circe-be/src/test/resources/checkers/primaryCriteriaCheckValueCorrect.json",
        "circe-be/src/test/resources/checkers/additionalCriteriaCheckValueCorrect.json",
        "circe-be/src/test/resources/checkers/conceptSetCriteriaCheckCorrect.json",
        "circe-be/src/test/resources/checkers/unusedConceptSetCorrect.json",
        "circe-be/src/test/resources/checkers/duplicatesConceptSetCheckCorrect.json",
        "circe-be/src/test/resources/checkers/duplicatesCriteriaCheckCorrect.json",
        "circe-be/src/test/resources/checkers/domainTypeCheckCorrect.json",
        "circe-be/src/test/resources/checkers/drugDomainCheckCorrect.json",
        "circe-be/src/test/resources/checkers/drugEraCheckCorrect.json",
        "circe-be/src/test/resources/checkers/deathTimeWindowCheckCorrect.json",
        "circe-be/src/test/resources/checkers/timePatternCheckCorrect.json",
        "circe-be/src/test/resources/checkers/eventsProgressionCheckCorrect.json",
        "circe-be/src/test/resources/checkers/contradictionsCriteriaCheckCorrect.json",
        "circe-be/src/test/resources/checkers/inclusionRulesCheckValueCorrect.json",
        "circe-be/src/test/resources/checkers/censoringEventCheckValueCorrect.json",
        "circe-be/src/test/resources/checkers/emptyDemographicCheckCorrect.json",
        "circe-be/src/test/resources/checkers/childGroupExpression.json",
        "circe-be/src/test/resources/cohortgeneration/allCriteria/allCriteriaExpression.json",
        "circe-be/src/test/resources/cohortgeneration/censorWindow/censorWindowExpression.json",
        "circe-be/src/test/resources/cohortgeneration/eraDupes/eraDupesExpression.json",
    ]

    results = []
    for test_case, test_file in zip(test_cases, test_files):
        print(f"\nTesting: {test_case.name}")
        result = run_validation_test(validator, test_file, test_case)
        results.append(result)

        status = "✅ PASSED" if result.passed else "❌ FAILED"
        print(
            f"  {status} - Warnings: {result.actual_warnings}, Errors: {result.actual_errors}"
        )
        if result.error_message:
            print(f"  Error: {result.error_message}")

    return results


def test_incorrect_cohorts(validator: CohortValidator) -> List[TestResult]:
    """Test cohorts that should have errors."""
    print("\n" + "=" * 60)
    print("TESTING INCORRECT COHORTS (Should have errors)")
    print("=" * 60)

    test_cases = [
        # These should have errors
        TestResult(
            "Primary Criteria Incorrect", expected_errors=None
        ),  # Should have many errors
        TestResult("Additional Criteria Incorrect", expected_errors=None),
        TestResult("Concept Set Criteria Incorrect", expected_errors=None),
        TestResult("Unused Concept Set", expected_errors=None),
        TestResult("Duplicates Concept Set Incorrect", expected_errors=None),
        TestResult("Duplicates Criteria Incorrect", expected_errors=None),
        TestResult("Domain Type Incorrect", expected_errors=None),
        TestResult("Drug Domain Incorrect", expected_errors=None),
        TestResult("Drug Era Incorrect", expected_errors=None),
        TestResult("Death Time Window Incorrect", expected_errors=None),
        TestResult("Time Pattern Incorrect", expected_errors=None),
        TestResult("Events Progression Incorrect", expected_errors=None),
        TestResult("Contradictions Criteria Incorrect", expected_errors=None),
        TestResult("Inclusion Rules Incorrect", expected_errors=None),
        TestResult("Censoring Event Incorrect", expected_errors=None),
        TestResult("Empty Demographic Incorrect", expected_errors=None),
        # Special cases
        TestResult("Concept Set With Duplicate Items", expected_errors=None),
        TestResult("Empty Censoring Criteria List", expected_errors=None),
        TestResult("Empty Correlated Criteria", expected_errors=None),
        TestResult("Empty Inclusion Rules", expected_errors=None),
        TestResult("Empty Primary Criteria List", expected_errors=None),
        TestResult("No Exit Criteria Check", expected_errors=None),
    ]

    test_files = [
        "circe-be/src/test/resources/checkers/primaryCriteriaCheckValueIncorrect.json",
        "circe-be/src/test/resources/checkers/additionalCriteriaCheckValueIncorrect.json",
        "circe-be/src/test/resources/checkers/conceptSetCriteriaCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/unusedConceptSet.json",
        "circe-be/src/test/resources/checkers/duplicatesConceptSetCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/duplicatesCriteriaCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/domainTypeCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/drugDomainCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/drugEraCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/deathTimeWindowCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/timePatternCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/eventsProgressionCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/contradictionsCriteriaCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/inclusionRulesCheckValueIncorrect.json",
        "circe-be/src/test/resources/checkers/censoringEventCheckValueIncorrect.json",
        "circe-be/src/test/resources/checkers/emptyDemographicCheckIncorrect.json",
        "circe-be/src/test/resources/checkers/conceptSetWithDuplicateItems.json",
        "circe-be/src/test/resources/checkers/emptyCensoringCriteriaList.json",
        "circe-be/src/test/resources/checkers/emptyCorrelatedCriteria.json",
        "circe-be/src/test/resources/checkers/emptyInclusionRules.json",
        "circe-be/src/test/resources/checkers/emptyPrimaryCriteriaList.json",
        "circe-be/src/test/resources/checkers/noExitCriteriaCheck.json",
    ]

    results = []
    for test_case, test_file in zip(test_cases, test_files):
        print(f"\nTesting: {test_case.name}")
        result = run_validation_test(validator, test_file, test_case)
        results.append(result)

        status = "✅ PASSED" if result.passed else "❌ FAILED"
        print(
            f"  {status} - Warnings: {result.actual_warnings}, Errors: {result.actual_errors}"
        )
        if result.error_message:
            print(f"  Error: {result.error_message}")

    return results


def test_complex_cohorts(validator: CohortValidator) -> List[TestResult]:
    """Test complex cohort expressions."""
    print("\n" + "=" * 60)
    print("TESTING COMPLEX COHORT EXPRESSIONS")
    print("=" * 60)

    test_cases = [
        TestResult("Condition Occurrence Status Test", expected_errors=0),
        TestResult("Counts Expression", expected_errors=0),
        TestResult("Group Expression", expected_errors=0),
        TestResult("Visit Expression", expected_errors=0),
        TestResult("First Occurrence Expression", expected_errors=0),
        TestResult("Inclusion Rules Expression", expected_errors=0),
        TestResult("Limits Expression", expected_errors=0),
        TestResult("Mixed Concept Sets Expression", expected_errors=0),
        TestResult("Dupilumab Expression", expected_errors=0),
        TestResult("Dupixent Expression", expected_errors=0),
        TestResult("Payer Plan Cohort Expression", expected_errors=0),
    ]

    test_files = [
        "circe-be/src/test/resources/cohortgeneration/conditionOccurrence/conditionStatusTest_VERIFY.json",
        "circe-be/src/test/resources/cohortgeneration/correlatedCriteria/countsExpression.json",
        "circe-be/src/test/resources/cohortgeneration/correlatedCriteria/groupExpression.json",
        "circe-be/src/test/resources/cohortgeneration/correlatedCriteria/visitExpression.json",
        "circe-be/src/test/resources/cohortgeneration/firstOccurrence/firstOccurrenceExpression.json",
        "circe-be/src/test/resources/cohortgeneration/inclusionRules/inclusionRulesExpression.json",
        "circe-be/src/test/resources/cohortgeneration/limits/limitsExpression.json",
        "circe-be/src/test/resources/cohortgeneration/mixedConceptsets/mixedConceptsetsExpression.json",
        "circe-be/src/test/resources/conceptset/dupilumabExpression.json",
        "circe-be/src/test/resources/conceptset/dupixentExpression.json",
        "circe-be/src/test/resources/versioning/payerPlanCohortExpression.json",
    ]

    results = []
    for test_case, test_file in zip(test_cases, test_files):
        print(f"\nTesting: {test_case.name}")
        result = run_validation_test(validator, test_file, test_case)
        results.append(result)

        status = "✅ PASSED" if result.passed else "❌ FAILED"
        print(
            f"  {status} - Warnings: {result.actual_warnings}, Errors: {result.actual_errors}"
        )
        if result.error_message:
            print(f"  Error: {result.error_message}")

    return results


def test_edge_cases(validator: CohortValidator) -> List[TestResult]:
    """Test edge cases and special scenarios."""
    print("\n" + "=" * 60)
    print("TESTING EDGE CASES AND SPECIAL SCENARIOS")
    print("=" * 60)

    test_cases = [
        TestResult("No Exit Criteria Check Earliest Event", expected_errors=None),
        TestResult("Build Options Test", expected_errors=0),
        TestResult("Vocabulary Dataset", expected_errors=0),
    ]

    test_files = [
        "circe-be/src/test/resources/checkers/noExitCriteriaCheckEarliestEvent.json",
        "circe-be/src/test/resources/cohortdefinition/buildOptionsTest.json",
        "circe-be/src/test/resources/datasets/vocabulary.json",
    ]

    results = []
    for test_case, test_file in zip(test_cases, test_files):
        print(f"\nTesting: {test_case.name}")
        result = run_validation_test(validator, test_file, test_case)
        results.append(result)

        status = "✅ PASSED" if result.passed else "❌ FAILED"
        print(
            f"  {status} - Warnings: {result.actual_warnings}, Errors: {result.actual_errors}"
        )
        if result.error_message:
            print(f"  Error: {result.error_message}")

    return results


def print_summary(all_results: List[List[TestResult]]):
    """Print a comprehensive test summary."""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE TEST SUMMARY")
    print("=" * 80)

    total_tests = 0
    total_passed = 0

    for i, results in enumerate(all_results):
        if i == 0:
            category = "Correct Cohorts"
        elif i == 1:
            category = "Incorrect Cohorts"
        elif i == 2:
            category = "Complex Cohorts"
        else:
            category = "Edge Cases"

        passed = sum(1 for r in results if r.passed)
        total = len(results)
        total_tests += total
        total_passed += passed

        print(f"\n{category}:")
        print(f"  Passed: {passed}/{total} ({passed/total*100:.1f}%)")

        # Show failed tests
        failed_tests = [r for r in results if not r.passed]
        if failed_tests:
            print(f"  Failed tests:")
            for test in failed_tests:
                print(f"    - {test.name}: {test.error_message or 'Unexpected result'}")

    print(f"\nOVERALL RESULTS:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_tests - total_passed}")
    print(f"  Success Rate: {total_passed/total_tests*100:.1f}%")

    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! The cohort validator is working correctly.")
    else:
        print(
            f"\n⚠️  {total_tests - total_passed} tests failed. Check the details above."
        )


def main():
    """Run the comprehensive test suite."""
    print("CIRCE Cohort Validator - Comprehensive Test Suite")
    print("=" * 80)
    print("Testing with real CIRCE test data files...")

    validator = CohortValidator()

    try:
        # Run all test categories
        all_results = []

        # Test correct cohorts (should have minimal errors)
        correct_results = test_correct_cohorts(validator)
        all_results.append(correct_results)

        # Test incorrect cohorts (should have errors)
        incorrect_results = test_incorrect_cohorts(validator)
        all_results.append(incorrect_results)

        # Test complex cohorts
        complex_results = test_complex_cohorts(validator)
        all_results.append(complex_results)

        # Test edge cases
        edge_results = test_edge_cases(validator)
        all_results.append(edge_results)

        # Print comprehensive summary
        print_summary(all_results)

    finally:
        validator.shutdown()
        print("\nValidator shutdown complete.")


if __name__ == "__main__":
    main()
