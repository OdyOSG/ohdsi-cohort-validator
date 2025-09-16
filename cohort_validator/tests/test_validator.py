#!/usr/bin/env python3
"""
Test script for the CohortValidator.

This script tests the cohort validation functionality with sample data.
"""

import json
import os

from cohort_validator import CohortValidator


def create_sample_cohort():
    """Create a sample cohort expression for testing."""
    # Use a minimal valid cohort expression that matches the Java structure
    # Based on the actual test files from CIRCE
    return {
        "ConceptSets": [
            {
                "id": 0,
                "name": "Parent Conceptset",
                "expression": {
                    "items": [
                        {
                            "concept": {
                                "CONCEPT_CLASS_ID": "Clinical Finding",
                                "CONCEPT_CODE": "P1",
                                "CONCEPT_ID": 1,
                                "CONCEPT_NAME": "Parent 1",
                                "DOMAIN_ID": "CONDITION",
                                "INVALID_REASON": "V",
                                "INVALID_REASON_CAPTION": "Valid",
                                "STANDARD_CONCEPT": "S",
                                "STANDARD_CONCEPT_CAPTION": "Standard",
                                "VOCABULARY_ID": "TestVocab",
                            },
                            "includeDescendants": True,
                        }
                    ]
                },
            }
        ],
        "PrimaryCriteria": {
            "CriteriaList": [{"ConditionOccurrence": {"CodesetId": 0}}],
            "ObservationWindow": {"PriorDays": 0, "PostDays": 0},
            "PrimaryCriteriaLimit": {"Type": "All"},
        },
        "AdditionalCriteria": {
            "Type": "ALL",
            "CriteriaList": [
                {
                    "Criteria": {"ConditionOccurrence": {"CodesetId": 0}},
                    "StartWindow": {
                        "Start": {"Coeff": -1},
                        "End": {"Days": 1, "Coeff": -1},
                        "UseEventEnd": False,
                    },
                    "Occurrence": {"Type": 2, "Count": 1},
                }
            ],
            "DemographicCriteriaList": [],
            "Groups": [],
        },
        "QualifiedLimit": {"Type": "All"},
        "ExpressionLimit": {"Type": "All"},
        "InclusionRules": [],
        "EndStrategy": {"DateOffset": {"DateField": "StartDate", "Offset": 1}},
        "CensoringCriteria": [],
        "CollapseSettings": {"CollapseType": "ERA", "EraPad": 60},
        "CensorWindow": {},
    }


def test_valid_cohort():
    """Test validation with a valid cohort."""
    print("Testing valid cohort...")

    validator = CohortValidator()
    cohort_data = create_sample_cohort()

    warnings, errors = validator.validate_cohort(cohort_data)

    print(f"Warnings: {len(warnings)}")
    print(f"Errors: {len(errors)}")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning['message']}")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error['message']}")

    # Don't shutdown here - we'll use the same validator for other tests
    assert len(errors) == 0


def test_invalid_json():
    """Test validation with invalid JSON."""
    print("\nTesting invalid JSON...")

    validator = CohortValidator()

    invalid_json = {"invalid": "json structure"}

    warnings, errors = validator.validate_cohort(invalid_json)

    print(f"Warnings: {len(warnings)}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error['message']}")

    assert len(errors) > 0


def test_file_validation():
    """Test validation from a file."""
    print("\nTesting file validation...")

    validator = CohortValidator()

    # Create a temporary test file
    test_file = "test_cohort.json"
    cohort_data = create_sample_cohort()

    with open(test_file, "w") as f:
        json.dump(cohort_data, f, indent=2)

    try:
        with open(test_file, "r") as f:
            cohort_data = json.load(f)

        warnings, errors = validator.validate_cohort(cohort_data)

        print(f"Warnings: {len(warnings)}")
        print(f"Errors: {len(errors)}")

        assert len(errors) == 0
    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)


def main():
    """Run all tests."""
    print("Cohort Validator Test Suite")
    print("=" * 40)

    results = []
    validator = None

    try:
        # Test 1: Valid Cohort
        try:
            result, validator = test_valid_cohort()
            results.append(("Valid Cohort", result, None))
            print(f"✓ Valid Cohort: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            results.append(("Valid Cohort", False, str(e)))
            print(f"✗ Valid Cohort: FAILED - {e}")

        # Test 2: Invalid JSON (using same validator)
        if validator:
            try:
                result = test_invalid_json(validator)
                results.append(("Invalid JSON", result, None))
                print(f"✓ Invalid JSON: {'PASSED' if result else 'FAILED'}")
            except Exception as e:
                results.append(("Invalid JSON", False, str(e)))
                print(f"✗ Invalid JSON: FAILED - {e}")

        # Test 3: File Validation (using same validator)
        if validator:
            try:
                result = test_file_validation(validator)
                results.append(("File Validation", result, None))
                print(f"✓ File Validation: {'PASSED' if result else 'FAILED'}")
            except Exception as e:
                results.append(("File Validation", False, str(e)))
                print(f"✗ File Validation: FAILED - {e}")

    finally:
        # Clean up validator
        if validator:
            validator.shutdown()

    print("\n" + "=" * 40)
    print("Test Summary:")
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("All tests passed! 🎉")
    else:
        print("Some tests failed. Check the output above.")
        for test_name, result, error in results:
            if not result:
                print(f"  - {test_name}: {error or 'Failed'}")


if __name__ == "__main__":
    main()
