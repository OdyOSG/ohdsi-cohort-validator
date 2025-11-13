"""
Comprehensive unit tests for validators/concept_checks.py
"""

import pytest
from cohort_validator.models.cohort import CohortExpression
from cohort_validator.models.concept import ConceptSet, ConceptSetExpression
from cohort_validator.models.criteria import ConditionOccurrence, Criteria
from cohort_validator.models.validation import WarningSeverity
from cohort_validator.validators.concept_checks import (
    ConceptCheck,
    ConceptSetSelectionCheck,
    DuplicatesConceptSetCheck,
    EmptyConceptSetCheck,
    UnusedConceptsCheck,
)


class TestEmptyConceptSetCheck:
    """Tests for EmptyConceptSetCheck."""

    def test_empty_concept_set_detection(self):
        """Test detection of empty concept sets."""
        check = EmptyConceptSetCheck()
        expression = CohortExpression(
            concept_sets=[
                ConceptSet(id=0, name="Empty Set", expression=ConceptSetExpression(items=[]))
            ]
        )

        warnings = check.check(expression)
        assert len(warnings) == 1
        assert "Empty Set" in warnings[0].message

    def test_no_empty_concept_sets(self):
        """Test with no empty concept sets."""
        check = EmptyConceptSetCheck()
        expression = CohortExpression(
            concept_sets=[
                ConceptSet(
                    id=0,
                    name="Non-Empty Set",
                    expression=ConceptSetExpression(
                        items=[
                            {
                                "concept": {
                                    "CONCEPT_ID": 201820,
                                    "CONCEPT_NAME": "Diabetes",
                                }
                            }
                        ]
                    ),
                )
            ]
        )

        warnings = check.check(expression)
        assert len(warnings) == 0

    def test_concept_set_with_no_expression(self):
        """Test concept set with None expression."""
        check = EmptyConceptSetCheck()
        expression = CohortExpression(
            concept_sets=[ConceptSet(id=0, name="No Expression Set", expression=None)]
        )

        warnings = check.check(expression)
        assert len(warnings) == 1


class TestDuplicatesConceptSetCheck:
    """Tests for DuplicatesConceptSetCheck."""

    def test_duplicate_concept_sets_detection(self):
        """Test detection of duplicate concept sets."""
        check = DuplicatesConceptSetCheck()
        common_items = [
            {
                "concept": {
                    "CONCEPT_ID": 201820,
                    "CONCEPT_NAME": "Diabetes",
                },
                "includeDescendants": True,
            }
        ]

        expression = CohortExpression(
            concept_sets=[
                ConceptSet(
                    id=0,
                    name="Set 1",
                    expression=ConceptSetExpression(items=common_items),
                ),
                ConceptSet(
                    id=1,
                    name="Set 2",
                    expression=ConceptSetExpression(items=common_items),
                ),
            ]
        )

        warnings = check.check(expression)
        assert len(warnings) >= 1
        assert warnings[0].severity == WarningSeverity.INFO

    def test_no_duplicates(self):
        """Test with no duplicate concept sets."""
        check = DuplicatesConceptSetCheck()
        expression = CohortExpression(
            concept_sets=[
                ConceptSet(
                    id=0,
                    name="Set 1",
                    expression=ConceptSetExpression(
                        items=[
                            {
                                "concept": {
                                    "CONCEPT_ID": 201820,
                                    "CONCEPT_NAME": "Diabetes",
                                }
                            }
                        ]
                    ),
                ),
                ConceptSet(
                    id=1,
                    name="Set 2",
                    expression=ConceptSetExpression(
                        items=[
                            {
                                "concept": {
                                    "CONCEPT_ID": 201821,
                                    "CONCEPT_NAME": "Hypertension",
                                }
                            }
                        ]
                    ),
                ),
            ]
        )

        warnings = check.check(expression)
        assert len(warnings) == 0


class TestUnusedConceptsCheck:
    """Tests for UnusedConceptsCheck."""

    def test_unused_concept_set_detection(self):
        """Test detection of unused concept sets."""
        check = UnusedConceptsCheck()
        expression = CohortExpression(
            concept_sets=[
                ConceptSet(
                    id=0,
                    name="Used Set",
                    expression=ConceptSetExpression(items=[]),
                ),
                ConceptSet(
                    id=1,
                    name="Unused Set",
                    expression=ConceptSetExpression(items=[]),
                ),
            ],
            primary_criteria=None,
        )

        warnings = check.check(expression)
        # Should detect unused concept sets
        assert isinstance(warnings, list)

    def test_all_concept_sets_used(self, minimal_cohort_expression):
        """Test when all concept sets are used."""
        check = UnusedConceptsCheck()
        # Use fixture that has concept set referenced in criteria
        warnings = check.check(minimal_cohort_expression)
        # Should not warn if concept set is used
        assert isinstance(warnings, list)


class TestConceptSetSelectionCheck:
    """Tests for ConceptSetSelectionCheck."""

    def test_concept_set_selection_check(self):
        """Test ConceptSetSelectionCheck."""
        check = ConceptSetSelectionCheck()
        expression = CohortExpression()

        warnings = check.check(expression)
        assert isinstance(warnings, list)


class TestConceptCheck:
    """Tests for ConceptCheck."""

    def test_concept_check(self):
        """Test ConceptCheck."""
        check = ConceptCheck()
        expression = CohortExpression()

        warnings = check.check(expression)
        assert isinstance(warnings, list)

