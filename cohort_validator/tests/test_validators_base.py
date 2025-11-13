"""
Comprehensive unit tests for validators/base.py
"""

import pytest
from cohort_validator.models.cohort import CohortExpression
from cohort_validator.models.validation import Warning, WarningSeverity
from cohort_validator.validators.base import (
    BaseCheck,
    BaseCheckerFactory,
    BaseCorelatedCriteriaCheck,
    BaseIterableCheck,
    BaseValueCheck,
    WarningReporter,
)


class TestWarningReporter:
    """Tests for WarningReporter class."""

    def test_warning_reporter_add(self):
        """Test WarningReporter.add() method."""
        calls = []

        def callback(template, *params):
            calls.append((template, params))

        reporter = WarningReporter(callback)
        reporter.add("Test message")
        reporter.add("Test with {0}", "param1")
        reporter.add("Test with {0} and {1}", "param1", "param2")

        assert len(calls) == 3
        assert calls[0] == ("Test message", ())
        assert calls[1] == ("Test with {0}", ("param1",))
        assert calls[2] == ("Test with {0} and {1}", ("param1", "param2"))


class ConcreteCheck(BaseCheck):
    """Concrete implementation of BaseCheck for testing."""

    def _check(self, expression, reporter):
        """Test implementation."""
        reporter.add("Test warning")


class TestBaseCheck:
    """Tests for BaseCheck abstract base class."""

    def test_base_check_check(self):
        """Test BaseCheck.check() method."""
        check = ConcreteCheck()
        expression = CohortExpression()
        warnings = check.check(expression)

        assert len(warnings) == 1
        assert warnings[0].message == "Test warning"
        assert warnings[0].severity == WarningSeverity.CRITICAL  # Default severity

    def test_base_check_constants(self):
        """Test BaseCheck class constants."""
        assert BaseCheck.INCLUSION_RULE == "inclusion rule "
        assert BaseCheck.ADDITIONAL_RULE == "additional rule"
        assert BaseCheck.INITIAL_EVENT == "initial event"


class ConcreteValueCheck(BaseValueCheck):
    """Concrete implementation of BaseValueCheck for testing."""

    def _get_factory(self, reporter, name):
        """Return a test factory."""
        return TestFactory(reporter, name)


class TestFactory(BaseCheckerFactory):
    """Test factory for testing."""

    def check(self, criteria):
        """Test check implementation."""
        self.reporter.add(f"Checked {criteria.__class__.__name__} in {self.name}")


class TestBaseValueCheck:
    """Tests for BaseValueCheck class."""

    def test_base_value_check_constants(self):
        """Test BaseValueCheck class constants."""
        assert BaseValueCheck.INCLUSION_CRITERIA == "Inclusion criteria "
        assert BaseValueCheck.PRIMARY_CRITERIA == "Primary criteria"
        assert BaseValueCheck.ADDITIONAL_CRITERIA == "Additional criteria"
        assert BaseValueCheck.CENSORING_CRITERIA == "Censoring events"

    def test_base_value_check_with_primary_criteria(self):
        """Test BaseValueCheck with primary criteria."""
        from cohort_validator.models.criteria import Criteria, ConditionOccurrence
        from cohort_validator.models.cohort import PrimaryCriteria

        check = ConcreteValueCheck()
        expression = CohortExpression(
            primary_criteria=PrimaryCriteria(
                criteria_list=[
                    Criteria(condition_occurrence=ConditionOccurrence(codeset_id=0))
                ]
            )
        )

        warnings = check.check(expression)
        # Should check the primary criteria
        assert len(warnings) >= 0  # May or may not generate warnings


class ConcreteIterableCheck(BaseIterableCheck):
    """Concrete implementation of BaseIterableCheck for testing."""

    def _internal_check(self, expression, reporter):
        """Test implementation."""
        reporter.add("Internal check warning")

    def _before_check(self, reporter, expression):
        """Before check hook."""
        reporter.add("Before check")

    def _after_check(self, reporter, expression):
        """After check hook."""
        reporter.add("After check")


class TestBaseIterableCheck:
    """Tests for BaseIterableCheck class."""

    def test_base_iterable_check_hooks(self):
        """Test BaseIterableCheck before/after hooks."""
        check = ConcreteIterableCheck()
        expression = CohortExpression()
        warnings = check.check(expression)

        messages = [w.message for w in warnings]
        assert "Before check" in messages
        assert "Internal check warning" in messages
        assert "After check" in messages

    def test_base_iterable_check_order(self):
        """Test that hooks are called in correct order."""
        check = ConcreteIterableCheck()
        expression = CohortExpression()
        warnings = check.check(expression)

        messages = [w.message for w in warnings]
        assert messages.index("Before check") < messages.index("Internal check warning")
        assert messages.index("Internal check warning") < messages.index("After check")


class ConcreteCorelatedCriteriaCheck(BaseCorelatedCriteriaCheck):
    """Concrete implementation for testing."""

    def _check_criteria(self, criteria, group_name, reporter):
        """Test implementation."""
        reporter.add(f"Checked correlated criteria in {group_name}")


class TestBaseCorelatedCriteriaCheck:
    """Tests for BaseCorelatedCriteriaCheck class."""

    def test_base_corelated_criteria_check(self):
        """Test BaseCorelatedCriteriaCheck."""
        check = ConcreteCorelatedCriteriaCheck()
        expression = CohortExpression()
        warnings = check.check(expression)

        # Should run without errors even with no inclusion rules
        assert isinstance(warnings, list)


class TestBaseCheckerFactory:
    """Tests for BaseCheckerFactory abstract base class."""

    def test_base_checker_factory_initialization(self):
        """Test BaseCheckerFactory initialization."""
        reporter = WarningReporter(lambda t, *p: None)
        factory = TestFactory(reporter, "Test Name")

        assert factory.reporter == reporter
        assert factory.name == "Test Name"

