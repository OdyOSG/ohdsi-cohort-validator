"""
Comprehensive unit tests for models/criteria.py
"""

import pytest
from cohort_validator.models.criteria import (
    ConditionOccurrence,
    Criteria,
    CriteriaGroup,
    DemographicCriteria,
    DrugExposure,
    VisitOccurrence,
)
from cohort_validator.models.base import DateRange, NumericRange, TextFilter


class TestCriteria:
    """Tests for Criteria base class."""

    def test_criteria_creation(self):
        """Test creating a Criteria."""
        criteria = Criteria()
        assert criteria.correlated_criteria is None
        assert criteria.date_adjustment is None

    def test_criteria_with_condition_occurrence(self):
        """Test Criteria with ConditionOccurrence."""
        condition = ConditionOccurrence(codeset_id=0)
        criteria = Criteria(condition_occurrence=condition)
        assert criteria.condition_occurrence == condition

    def test_criteria_with_drug_exposure(self):
        """Test Criteria with DrugExposure."""
        drug = DrugExposure(codeset_id=0)
        criteria = Criteria(drug_exposure=drug)
        assert criteria.drug_exposure == drug


class TestConditionOccurrence:
    """Tests for ConditionOccurrence model."""

    def test_condition_occurrence_creation(self):
        """Test creating a ConditionOccurrence."""
        condition = ConditionOccurrence(codeset_id=0)
        assert condition.codeset_id == 0

    def test_condition_occurrence_with_aliases(self):
        """Test ConditionOccurrence with alias fields."""
        condition = ConditionOccurrence(CodesetId=1)
        assert condition.codeset_id == 1

    def test_condition_occurrence_with_date_range(self):
        """Test ConditionOccurrence with date range."""
        date_range = DateRange(value="2020-01-01", op="gt")
        condition = ConditionOccurrence(
            codeset_id=0, occurrence_start_date=date_range
        )
        assert condition.occurrence_start_date == date_range

    def test_condition_occurrence_with_numeric_range(self):
        """Test ConditionOccurrence with numeric range."""
        age_range = NumericRange(value=18, op="gte", extent=65)
        condition = ConditionOccurrence(codeset_id=0, age=age_range)
        assert condition.age == age_range


class TestDrugExposure:
    """Tests for DrugExposure model."""

    def test_drug_exposure_creation(self):
        """Test creating a DrugExposure."""
        drug = DrugExposure(codeset_id=0)
        assert drug.codeset_id == 0

    def test_drug_exposure_with_refills(self):
        """Test DrugExposure with refills."""
        refills = NumericRange(value=1, op="gte")
        drug = DrugExposure(codeset_id=0, refills=refills)
        assert drug.refills == refills

    def test_drug_exposure_with_quantity(self):
        """Test DrugExposure with quantity."""
        quantity = NumericRange(value=30, op="gte")
        drug = DrugExposure(codeset_id=0, quantity=quantity)
        assert drug.quantity == quantity

    def test_drug_exposure_with_stop_reason(self):
        """Test DrugExposure with stop reason."""
        stop_reason = TextFilter(text="Completed", op="eq")
        drug = DrugExposure(codeset_id=0, stop_reason=stop_reason)
        assert drug.stop_reason == stop_reason


class TestVisitOccurrence:
    """Tests for VisitOccurrence model."""

    def test_visit_occurrence_creation(self):
        """Test creating a VisitOccurrence."""
        visit = VisitOccurrence(codeset_id=0)
        assert visit.codeset_id == 0

    def test_visit_occurrence_with_date_range(self):
        """Test VisitOccurrence with date range."""
        date_range = DateRange(value="2020-01-01", op="gt")
        visit = VisitOccurrence(codeset_id=0, occurrence_start_date=date_range)
        assert visit.occurrence_start_date == date_range


class TestCriteriaGroup:
    """Tests for CriteriaGroup model."""

    def test_criteria_group_creation(self):
        """Test creating a CriteriaGroup."""
        group = CriteriaGroup(type="ALL")
        assert group.type == "ALL"
        assert group.criteria_list == []
        assert group.demographic_criteria_list == []
        assert group.groups == []

    def test_criteria_group_with_criteria(self):
        """Test CriteriaGroup with criteria."""
        criteria = Criteria(condition_occurrence=ConditionOccurangan(codeset_id=0))
        group = CriteriaGroup(type="ALL", criteria_list=[criteria])
        assert len(group.criteria_list) == 1

    def test_criteria_group_with_groups(self):
        """Test CriteriaGroup with nested groups."""
        sub_group = CriteriaGroup(type="ANY")
        group = CriteriaGroup(type="ALL", groups=[sub_group])
        assert len(group.groups) == 1


class TestDemographicCriteria:
    """Tests for DemographicCriteria model."""

    def test_demographic_criteria_creation(self):
        """Test creating a DemographicCriteria."""
        demo = DemographicCriteria()
        assert demo.age is None
        assert demo.gender is None

    def test_demographic_criteria_with_age(self):
        """Test DemographicCriteria with age."""
        age_range = NumericRange(value=18, op="gte", extent=65)
        demo = DemographicCriteria(age=age_range)
        assert demo.age == age_range

