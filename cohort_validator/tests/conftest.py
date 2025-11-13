"""
Pytest fixtures and utilities for testing.
"""

import pytest
from cohort_validator.models.cohort import CohortExpression
from cohort_validator.models.concept import Concept, ConceptSet, ConceptSetExpression
from cohort_validator.models.cohort import PrimaryCriteria
from cohort_validator.models.criteria import (
    Criteria,
    CriteriaGroup,
    ConditionOccurrence,
)
from cohort_validator.validators.cohort_checks import CohortValidator


@pytest.fixture
def sample_concept():
    """Create a sample concept for testing."""
    return Concept(
        concept_id=201820,
        concept_name="Diabetes mellitus",
        domain_id="Condition",
        vocabulary_id="SNOMED",
        concept_code="73211009",
        standard_concept="S",
        invalid_reason="V",
    )


@pytest.fixture
def sample_concept_set(sample_concept):
    """Create a sample concept set for testing."""
    return ConceptSet(
        id=0,
        name="Diabetes Mellitus",
        expression=ConceptSetExpression(
            items=[
                {
                    "concept": sample_concept,
                    "includeDescendants": True,
                }
            ]
        ),
    )


@pytest.fixture
def minimal_cohort_expression():
    """Create a minimal valid cohort expression for testing."""
    return CohortExpression(
        concept_sets=[
            ConceptSet(
                id=0,
                name="Test Concept Set",
                expression=ConceptSetExpression(items=[]),
            )
        ],
        primary_criteria=PrimaryCriteria(
            criteria_list=[
                Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))
            ]
        ),
    )


@pytest.fixture
def complete_cohort_expression():
    """Create a complete cohort expression with all fields for testing."""
    from cohort_validator.models.base import CollapseSettings, ObservationFilter

    return CohortExpression(
        title="Test Cohort",
        cdm_version_range=">=6.0.0",
        concept_sets=[
            ConceptSet(
                id=0,
                name="Test Concept Set",
                expression=ConceptSetExpression(
                    items=[
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
                ),
            )
        ],
        primary_criteria=PrimaryCriteria(
            criteria_list=[
                Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))
            ],
            observation_window=ObservationFilter(prior_days=0, post_days=0),
        ),
        additional_criteria=CriteriaGroup(type="ALL"),
        collapse_settings=CollapseSettings(collapse_type="ERA", era_pad=0),
    )


@pytest.fixture
def validator():
    """Create a CohortValidator instance for testing."""
    return CohortValidator()


@pytest.fixture
def sample_cohort_dict():
    """Create a sample cohort as a dictionary for testing."""
    return {
        "ConceptSets": [
            {
                "id": 0,
                "name": "Test Concept Set",
                "expression": {
                    "items": [
                        {
                            "concept": {
                                "CONCEPT_ID": 201820,
                                "CONCEPT_NAME": "Diabetes mellitus",
                                "DOMAIN_ID": "Condition",
                                "VOCABULARY_ID": "SNOMED",
                                "CONCEPT_CODE": "73211009",
                                "STANDARD_CONCEPT": "S",
                                "INVALID_REASON": "V",
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
    }

