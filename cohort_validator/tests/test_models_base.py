"""
Comprehensive unit tests for models/base.py
"""

import pytest
from pydantic import ValidationError

from cohort_validator.models.base import (
    CollapseSettings,
    CollapseType,
    DateAdjustment,
    DateRange,
    NumericRange,
    ObservationFilter,
    Period,
    ResultLimit,
    TextFilter,
)


class TestDateRange:
    """Tests for DateRange model."""

    def test_date_range_creation(self):
        """Test creating a DateRange with all fields."""
        date_range = DateRange(value="2020-01-01", Op="gt", extent="2020-12-31")
        assert date_range.value == "2020-01-01"
        assert date_range.op == "gt"
        assert date_range.extent == "2020-12-31"

    def test_date_range_with_aliases(self):
        """Test DateRange with alias fields."""
        date_range = DateRange(Value="2020-01-01", Op="bt", Extent="2020-12-31")
        assert date_range.value == "2020-01-01"
        assert date_range.op == "bt"
        assert date_range.extent == "2020-12-31"

    def test_date_range_minimal(self):
        """Test DateRange with minimal fields."""
        date_range = DateRange(value="2020-01-01")
        assert date_range.value == "2020-01-01"
        assert date_range.op is None
        assert date_range.extent is None

    def test_date_range_empty(self):
        """Test DateRange with no fields."""
        date_range = DateRange()
        assert date_range.value is None
        assert date_range.op is None
        assert date_range.extent is None


class TestNumericRange:
    """Tests for NumericRange model."""

    def test_numeric_range_int(self):
        """Test NumericRange with integer values."""
        num_range = NumericRange(value=100, op="gt", extent=200)
        assert num_range.value == 100
        assert num_range.op == "gt"
        assert num_range.extent == 200

    def test_numeric_range_float(self):
        """Test NumericRange with float values."""
        num_range = NumericRange(value=10.5, op="lt", extent=20.5)
        assert num_range.value == 10.5
        assert num_range.op == "lt"
        assert num_range.extent == 20.5

    def test_numeric_range_with_aliases(self):
        """Test NumericRange with alias fields."""
        num_range = NumericRange(Value=50, Op="bt", Extent=100)
        assert num_range.value == 50
        assert num_range.op == "bt"
        assert num_range.extent == 100

    def test_numeric_range_minimal(self):
        """Test NumericRange with minimal fields."""
        num_range = NumericRange(value=42)
        assert num_range.value == 42
        assert num_range.op is None
        assert num_range.extent is None


class TestTextFilter:
    """Tests for TextFilter model."""

    def test_text_filter_creation(self):
        """Test creating a TextFilter."""
        text_filter = TextFilter(text="test", op="contains")
        assert text_filter.text == "test"
        assert text_filter.op == "contains"

    def test_text_filter_empty(self):
        """Test TextFilter with no fields."""
        text_filter = TextFilter()
        assert text_filter.text is None
        assert text_filter.op is None


class TestResultLimit:
    """Tests for ResultLimit model."""

    def test_result_limit_default(self):
        """Test ResultLimit with default value."""
        limit = ResultLimit()
        assert limit.type == "First"

    def test_result_limit_all(self):
        """Test ResultLimit with 'All' type."""
        limit = ResultLimit(type="All")
        assert limit.type == "All"


class TestPeriod:
    """Tests for Period model."""

    def test_period_creation(self):
        """Test creating a Period with dates."""
        period = Period(
            start_date="2020-01-01", end_date="2020-12-31"
        )
        assert period.start_date == "2020-01-01"
        assert period.end_date == "2020-12-31"

    def test_period_with_aliases(self):
        """Test Period with alias fields."""
        period = Period(StartDate="2020-01-01", EndDate="2020-12-31")
        assert period.start_date == "2020-01-01"
        assert period.end_date == "2020-12-31"

    def test_period_minimal(self):
        """Test Period with minimal fields."""
        period = Period(start_date="2020-01-01")
        assert period.start_date == "2020-01-01"
        assert period.end_date is None


class TestCollapseType:
    """Tests for CollapseType enum."""

    def test_collapse_type_era(self):
        """Test CollapseType.ERA."""
        assert CollapseType.ERA == "ERA"
        assert CollapseType.ERA.value == "ERA"


class TestCollapseSettings:
    """Tests for CollapseSettings model."""

    def test_collapse_settings_default(self):
        """Test CollapseSettings with default values."""
        settings = CollapseSettings()
        assert settings.collapse_type == CollapseType.ERA
        assert settings.era_pad == 0

    def test_collapse_settings_custom(self):
        """Test CollapseSettings with custom values."""
        settings = CollapseSettings(collapse_type=CollapseType.ERA, era_pad=30)
        assert settings.collapse_type == CollapseType.ERA
        assert settings.era_pad == 30

    def test_collapse_settings_with_aliases(self):
        """Test CollapseSettings with alias fields."""
        settings = CollapseSettings(CollapseType="ERA", EraPad=60)
        assert settings.collapse_type == CollapseType.ERA
        assert settings.era_pad == 60


class TestDateAdjustment:
    """Tests for DateAdjustment model."""

    def test_date_adjustment_creation(self):
        """Test creating a DateAdjustment (currently minimal)."""
        adjustment = DateAdjustment()
        assert adjustment is not None


class TestObservationFilter:
    """Tests for ObservationFilter model."""

    def test_observation_filter_creation(self):
        """Test creating an ObservationFilter."""
        filter_obj = ObservationFilter(prior_days=30, post_days=60)
        assert filter_obj.prior_days == 30
        assert filter_obj.post_days == 60

    def test_observation_filter_with_aliases(self):
        """Test ObservationFilter with alias fields."""
        filter_obj = ObservationFilter(PriorDays=30, PostDays=60)
        assert filter_obj.prior_days == 30
        assert filter_obj.post_days == 60

    def test_observation_filter_minimal(self):
        """Test ObservationFilter with minimal fields."""
        filter_obj = ObservationFilter(prior_days=0)
        assert filter_obj.prior_days == 0
        assert filter_obj.post_days is None

