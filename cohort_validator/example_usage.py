#!/usr/bin/env python3
"""
Example usage of the CohortValidator.

This script demonstrates how to use the CohortValidator to validate
cohort expressions and handle the results.
"""

import json

from cohort_validator import CohortValidator


def main():
    """Demonstrate cohort validation usage."""

    # Sample cohort expression
    sample_cohort = {
        "ConceptSets": [
            {
                "id": 0,
                "name": "Diabetes",
                "expression": {
                    "items": [
                        {
                            "concept": {
                                "CONCEPT_ID": 201820,
                                "CONCEPT_NAME": "Diabetes mellitus",
                                "DOMAIN_ID": "Condition",
                                "VOCABULARY_ID": "SNOMED",
                            },
                            "includeDescendants": True,
                        }
                    ]
                },
            }
        ],
        "PrimaryCriteria": {
            "CriteriaList": [
                {
                    "ConditionOccurrence": {
                        "OccurrenceStartDate": {
                            "Value": "2020-01-01",
                            "Extent": "2023-12-31",
                            "Op": "bt",
                        }
                    }
                }
            ],
            "ObservationWindow": {"PriorDays": 0, "PostDays": 0},
            "PrimaryCriteriaLimit": {"Type": "First"},
        },
        "AdditionalCriteria": {
            "Type": "ALL",
            "CriteriaList": [],
            "DemographicCriteriaList": [],
            "Groups": [],
        },
        "QualifiedLimit": {"Type": "First"},
        "ExpressionLimit": {"Type": "First"},
        "InclusionRules": [],
        "CensoringCriteria": [],
        "CollapseSettings": {"CollapseType": "ERA", "EraPad": 0},
        "CensorWindow": {},
        "cdmVersionRange": ">=6.1.0",
    }

    print("Cohort Validator Example")
    print("=" * 50)

    # Initialize validator
    print("Initializing validator...")
    validator = CohortValidator()

    try:
        # Convert to JSON string
        cohort_json = json.dumps(sample_cohort, indent=2)

        print("\nValidating cohort expression...")
        print(f"Cohort: {sample_cohort['ConceptSets'][0]['name']} condition")

        # Validate the cohort
        warnings, errors = validator.validate_cohort(cohort_json)

        # Display results
        print(f"\nValidation Results:")
        print(f"  Warnings: {len(warnings)}")
        print(f"  Errors: {len(errors)}")

        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. [{warning['severity']}] {warning['message']}")

        if errors:
            print(f"\nErrors ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. [{error['severity']}] {error['message']}")

        if not warnings and not errors:
            print("\n✅ No validation issues found!")
        elif not errors:
            print(f"\n⚠️  Found {len(warnings)} warnings but no errors.")
        else:
            print(f"\n❌ Found {len(errors)} errors that need to be fixed.")

        # Demonstrate file validation
        print(f"\n" + "=" * 50)
        print("File Validation Example")

        # Save cohort to file
        filename = "example_cohort.json"
        with open(filename, "w") as f:
            json.dump(sample_cohort, f, indent=2)

        print(f"Saved cohort to {filename}")

        # Validate from file
        file_warnings, file_errors = validator.validate_cohort_file(filename)

        print(f"File validation results:")
        print(f"  Warnings: {len(file_warnings)}")
        print(f"  Errors: {len(file_errors)}")

        # Clean up
        import os

        if os.path.exists(filename):
            os.remove(filename)
            print(f"Cleaned up {filename}")

    finally:
        # Always shutdown the validator
        validator.shutdown()
        print("\nValidator shutdown complete.")


if __name__ == "__main__":
    main()
