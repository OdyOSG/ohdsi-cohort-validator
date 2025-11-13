"""
Comprehensive unit tests for models/cohort.py
"""

import json
import pytest
from cohort_validator.models.cohort import (
    CohortExpression,
    InclusionRule,
    PrimaryCriteria,
)
from cohort_validator.models.concept import ConceptSet, ConceptSetExpression
from cohort_validator.models.criteria import Criteria, ConditionOccurrence, CriteriaGroup
from cohort_validator.models.base import (
    CollapseSettings,
    ObservationFilter,
    ResultLimit,
)


class TestPrimaryCriteria:
    """Tests for PrimaryCriteria model."""

    def test_primary_criteria_creation(self):
        """Test creating a PrimaryCriteria."""
        criteria_list = [
            Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))
        ]
        observation_window = ObservationFilter(prior_days=0, post_days=0)
        primary_limit = ResultLimit(type="First")

        primary_criteria = PrimaryCriteria(
            criteria_list=criteria_list,
            observation_window=observation_window,
            primary_limit=primary_limit,
        )

        assert len(primary_criteria.criteria_list) == 1
        assert primary_criteria.observation_window == observation_window
        assert primary_criteria.primary_limit == primary_limit

    def test_primary_criteria_with_aliases(self):
        """Test PrimaryCriteria with alias fields."""
        primary_criteria = PrimaryCriteria(
            CriteriaList=[{"ConditionOccurrence": {"CodesetId": 0}}],
            ObservationWindow={"PriorDays": 0, "PostDays": 0},
            PrimaryCriteriaLimit={"Type": "First"},
        )

        assert len(primary_criteria.criteria_list) == 1
        assert primary_criteria.observation_window is not None
        assert primary_criteria.primary_limit is not None

    def test_primary_criteria_minimal(self):
        """Test PrimaryCriteria with minimal fields."""
        primary_criteria = PrimaryCriteria()
        assert primary_criteria.criteria_list == []
        assert primary_criteria.observation_window is None
        assert primary_criteria.primary_limit is not None  # Has default


class TestInclusionRule:
    """Tests for InclusionRule model."""

    def test_inclusion_rule_creation(self):
        """Test creating an InclusionRule."""
        criteria_group = CriteriaGroup(type="ALL")
        rule = InclusionRule(
            name="Test Rule",
            description="Test Description",
            expression=criteria_group,
        )

        assert rule.name == "Test Rule"
        assert rule.description == "Test Description"
        assert rule.expression == criteria_group

    def test_inclusion_rule_minimal(self):
        """Test InclusionRule with minimal fields."""
        rule = InclusionRule()
        assert rule.name is None
        assert rule.description is None
        assert rule.expression is None


class TestCohortExpression:
    """Tests for CohortExpression model."""

    def test_cohort_expression_creation(self):
        """Test creating a CohortExpression."""
        concept_set = ConceptSet(
            id=0, name="Test", expression=ConceptSetExpression(items=[])
        )
        primary_criteria = PrimaryCriteria(
            criteria_list=[Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))]
        )
        collapse_settings = CollapseSettings()

        expression = CohortExpression(
            title="Test Cohort",
            cdm_version_range=">=6.0.0",
            concept_sets=[concept_set],
            primary_criteria=primary_criteria,
            collapse_settings=collapse_settings,
        )

        assert expression.title == "Test Cohort"
        assert expression.cdm_version_range == ">=6.0.0"
        assert len(expression.concept_sets) == 1
        assert expression.primary_criteria == primary_criteria
        assert expression.collapse_settings == collapse_settings

    def test_cohort_expression_with_aliases(self):
        """Test CohortExpression with alias fields."""
        expression_data = {
            "Title": "Test Cohort",
            "cdmVersionRange": ">=6.0.0",
            "ConceptSets": [
                {
                    "id": 0,
                    "name": "Test Set",
                    "expression": {"items": []},
                }
            ],
            "PrimaryCriteria": {
                "CriteriaList": [{"ConditionOccurrence": {"CodesetId": 0}}],
            },
            "CollapseSettings": {"CollapseType": "ERA", "EraPad": 0},
        }
        expression = CohortExpression(**expression_data)

        assert expression.title == "Test Cohort"
        assert expression.cdm_version_range == ">=6.0.0"
        assert len(expression.concept_sets) == 1

    def test_cohort_expression_from_json_string(self):
        """Test CohortExpression.from_json() method."""
        json_str = json.dumps({
            "Title": "WIWI Cohort",
            "ConceptSets": [
                {
                    "id": 0,
                    "name": "Test Set",
                    "expression": {"items": []},
                }
            ],
            "PrimaryCriteria": {
                "CriteriaList": [{"ConditionOccurrence": {"CodesetId": 0}}],
            },
        })

        expression = CohortExpression.from_json(json_str)

        assert expression.title == "WIWI Cohort"
        assert len(expression.concept_sets) == 1

    def test_cohort_expression_from_json_with_wrapper(self):
        """Test CohortExpression.from_json() with wrapper object."""
        json_str = json.dumps({
            "cohort_definition": {
                "Title": "WIWI Cohort",
                "ConceptSets": [
                    {
                        "id": 0,
                        "name": "Test Set",
                        "expression": {"items": []},
                    }
                ],
                "PrimaryCriteria": {
                    "CriteriaList": [{"ConditionOccurrence": {"CodesetId": 0}}],
                },
            }
        })

        expression = CohortExpression.from_json(json_str)

        assert expression.title == "WIWI Cohort"
        assert len(expression.concept_sets) == 1

    def test_cohort_expression_to_json(self):
        """Test CohortExpression.to_json() method."""
        expression = CohortExpression(
            title="Test Cohort",
            concept_sets=[
                ConceptSet(
                    id=0, name="Test Set", expression=ConceptSetExpression(items=[])
                )
            ],
            primary_criteria=PrimaryCriteria(
                criteria_list=[
                    Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))
                ]
            ),
        )

        json_str = expression.to_json()
        assert isinstance(json_str, str)

        # Parse back to verify
        data = json.loads(json_str)
        assert data["Title"] == "Test Cohort"
        assert len(data["ConceptSets"]) == 1

    def test_cohort_expression_defaults(self):
        """Test CohortExpression with default values."""
        expression = CohortExpression()
        assert expression.concept_sets == []
        assert expression.inclusion_rules == []
        assert expression.censoring_criteria == []
        assert expression.title is None
        assert expression.cdm_version_range is None

    def test_cohort_expression_with_all_fields(self):
        """Test CohortExpression with all optional fields."""
        expression = CohortExpression(
            title="Complete Cohort",
            cdm_version_range=">=6.0.0",
            concept_sets=[
                ConceptSet(
                    id=0, name="Test Set", expression=ConceptSetExpression(items=[])
                )
            ],
            primary_criteria=PrimaryCriteria(
                criteria_list=[
                    Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))
                ]
            ),
            additional_criteria=CriteriaGroup(type="ALL"),
            inclusion_rules=[
                InclusionRule(name="Rule 1", expression=CriteriaGroup(type="ALL"))
            ],
            censoring_criteria=[Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))],
            collapse_settings=CollapseSettings(collapse_type="ERA", era_pad=0),
        )

        assert expression.title == "Complete Cohort"
        assert len(expression.concept_sets) == 1
        assert len(expression.inclusion_rules) == 1
        assert len(expression.censoring_criteria) == 1

