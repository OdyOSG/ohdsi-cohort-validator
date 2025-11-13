"""
Comprehensive unit tests for models/validation.py
"""

import pytest
from cohort_validator.models.validation import (
    ConceptSetWarning,
    DefaultWarning,
    ValidationResult,
    Warning,
    WarningSeverity,
)
from cohort_validator.models.concept import ConceptSet, ConceptSetExpression


class TestWarningSeverity:
    """Tests for WarningSeverity enum."""

    def test_warning_severity_values(self):
        """Test WarningSeverity enum values."""
        assert WarningSeverity.INFO == "INFO"
        assert WarningSeverity.WARNING == "WARNING"
        assert WarningSeverity.CRITICAL == "CRITICAL"

    def test_warning_severity_string_representation(self):
        """Test WarningSeverity string representation."""
        assert str(WarningSeverity.INFO) == "INFO"
        assert str(WarningSeverity.WARNING) == "WARNING"
        assert str(WarningSeverity.CRITICAL) == "CRITICAL"


class TestWarning:
    """Tests for Warning base class."""

    def test_warning_creation(self):
        """Test creating a Warning."""
        warning = Warning(severity=WarningSeverity.WARNING, message="Test warning")
        assert warning.severity == WarningSeverity.WARNING
        assert warning.message == "Test warning"

    def test_warning_to_message(self):
        """Test warning.to_message() method."""
        warning = Warning(severity=WarningSeverity.INFO, message="Test message")
        assert warning.to_message() == "Test message"


class TestDefaultWarning:
    """Tests for DefaultWarning class."""

    def test_default_warning_creation(self):
        """Test creating a DefaultWarning."""
        warning = DefaultWarning(severity=WarningSeverity.WARNING, message="Test")
        assert warning.severity == WarningSeverity.WARNING
        assert warning.message == "Test"
        assert isinstance(warning, Warning)

    def test_default_warning_to_message(self):
        """Test DefaultWarning.to_message() method."""
        warning = DefaultWarning(severity=WarningSeverity.ERROR, message="Error message")
        assert warning.to_message() == "Error message"


class TestConceptSetWarning:
    """Tests for ConceptSetWarning class."""

    def test_concept_set_warning_creation(self):
        """Test creating a ConceptSetWarning."""
        concept_set = ConceptSet(
            id=0, name="Test Set", expression=ConceptSetExpression(items=[])
        )
        warning = ConceptSetWarning(
            severity=WarningSeverity.WARNING,
            message="Test warning",
            concept_set=concept_set,
        )
        assert warning.severity == WarningSeverity.WARNING
        assert warning.message == "Test warning"
        assert warning.concept_set == concept_set

    def test_concept_set_warning_without_concept_set(self):
        """Test ConceptSetWarning without concept_set."""
        warning = ConceptSetWarning(
            severity=WarningSeverity.WARNING, message="Test warning"
        )
        assert warning.concept_set is None

    def test_concept_set_warning_to_message(self):
        """Test ConceptSetWarning.to_message() method."""
        warning = ConceptSetWarning(
            severity=WarningSeverity.WARNING, message="Test message"
        )
        assert warning.to_message() == "Test message"


class TestValidationResult:
    """Tests for ValidationResult class."""

    def test_validation_result_creation_valid(self):
        """Test creating a valid ValidationResult."""
        result = ValidationResult(is_valid=True)
        assert result.is_valid is True
        assert result.warnings == []
        assert result.errors == []
        assert result.info == []

    def test_validation_result_creation_invalid(self):
        """Test creating an invalid ValidationResult."""
        result = ValidationResult(is_valid=False)
        assert result.is_valid is False

    def test_validation_result_has_warnings(self):
        """Test has_warnings property."""
        result = ValidationResult(is_valid=True)
        assert result.has_warnings is False

        result.add_warning(WarningSeverity.WARNING, "Test warning")
        assert result.has_warnings is True

    def test_validation_result_has_errors(self):
        """Test has_errors property."""
        result = ValidationResult(is_valid=True)
        assert result.has_errors is False

        result.add_warning(WarningSeverity.CRITICAL, "Critical error")
        assert result.has_errors is True

    def test_validation_result_has_info(self):
        """Test has_info property."""
        result = ValidationResult(is_valid=True)
        assert result.has_info is False

        result.add_warning(WarningSeverity.INFO, "Info message")
        assert result.has_info is True

    def test_validation_result_total_issues(self):
        """Test total_issues property."""
        result = ValidationResult(is_valid=True)
        assert result.total_issues == 0

        result.add_warning(WarningSeverity.WARNING, "Warning 1")
        result.add_warning(WarningSeverity.WARNING, "Warning 2")
        result.add_warning(WarningSeverity.CRITICAL, "Error 1")
        result.add_warning(WarningSeverity.INFO, "Info 1")

        assert result.total_issues == 4

    def test_add_warning_warning_level(self):
        """Test add_warning with WARNING severity."""
        result = ValidationResult(is_valid=True)
        result.add_warning(WarningSeverity.WARNING, "Test warning")

        assert len(result.warnings) == 1
        assert len(result.errors) == 0
        assert len(result.info) == 0
        assert result.warnings[0].message == "Test warning"
        assert result.is_valid is True  # Warnings don't invalidate

    def test_add_warning_critical_level(self):
        """Test add_warning with CRITICAL severity."""
        result = ValidationResult(is_valid=True)
        result.add_warning(WarningSeverity.CRITICAL, "Critical error")

        assert len(result.warnings) == 0
        assert len(result.errors) == 1
        assert len(result.info) == 0
        assert result.errors[0].message == "Critical error"
        assert result.is_valid is False  # Errors invalidate

    def test_add_warning_info_level(self):
        """Test add_warning with INFO severity."""
        result = ValidationResult(is_valid=True)
        result.add_warning(WarningSeverity.INFO, "Info message")

        assert len(result.warnings) == 0
        assert len(result.errors) == 0
        assert len(result.info) == 1
        assert result.info[0].message == "Info message"
        assert result.is_valid is True

    def test_add_warning_with_concept_set(self):
        """Test add_warning with concept_set."""
        result = ValidationResult(is_valid=True)
        concept_set = ConceptSet(
            id=0, name="Test Set", expression=ConceptSetExpression(items=[])
        )
        result.add_warning(
            WarningSeverity.WARNING, "Warning with concept set", concept_set=concept_set
        )

        assert len(result.warnings) == 1
        assert isinstance(result.warnings[0], ConceptSetWarning)
        assert result.warnings[0].concept_set == concept_set

    def test_get_summary(self):
        """Test get_summary() method."""
        result = ValidationResult(is_valid=True)
        result.add_warning(WarningSeverity.WARNING, "Warning 1")
        result.add_warning(WarningSeverity.CRITICAL, "Error 1")
        result.add_warning(WarningSeverity.INFO, "Info 1")

        summary = result.get_summary()
        assert summary["is_valid"] is False
        assert summary["total_issues"] == 3
        assert summary["errors"] == 1
        assert summary["warnings"] == 1
        assert summary["info"] == 1
        assert "summary" in summary

    def test_get_all_messages(self):
        """Test get_all_messages() method."""
        result = ValidationResult(is_valid=True)
        result.add_warning(WarningSeverity.WARNING, "Warning 1")
        result.add_warning(WarningSeverity.CRITICAL, "Error 1")
        result.add_warning(WarningSeverity.INFO, "Info 1")

        messages = result.get_all_messages()
        assert len(messages) == 3
        assert "Warning 1" in messages
        assert "Error 1" in messages
        assert "Info 1" in messages

    def test_get_messages_by_severity(self):
        """Test get_messages_by_severity() method."""
        result = ValidationResult(is_valid=True)
        result.add_warning(WarningSeverity.WARNING, "Warning 1")
        result.add_warning(WarningSeverity.WARNING, "Warning 2")
        result.add_warning(WarningSeverity.CRITICAL, "Error 1")
        result.add_warning(WarningSeverity.INFO, "Info 1")

        warnings = result.get_messages_by_severity(WarningSeverity.WARNING)
        assert len(warnings) == 2
        assert "Warning 1" in warnings
        assert "Warning 2" in warnings

        errors = result.get_messages_by_severity(WarningSeverity.CRITICAL)
        assert len(errors) == 1
        assert "Error 1" in errors

        info = result.get_messages_by_severity(WarningSeverity.INFO)
        assert len(info) == 1
        assert "Info 1" in info

    def test_merge(self):
        """Test merge() method."""
        result1 = ValidationResult(is_valid=True)
        result1.add_warning(WarningSeverity.WARNING, "Warning 1")

        result2 = ValidationResult(is_valid=True)
        result2.add_warning(WarningSeverity.CRITICAL, "Error 1")
        result2.add_warning(WarningSeverity.INFO, "Info 1")

        result1.merge(result2)

        assert len(result1.warnings) == 1
        assert len(result1.errors) == 1
        assert len(result1.info) == 1
        assert result1.total_issues == 3

    def test_merge_invalid_result(self):
        """Test merge() with invalid result."""
        result1 = ValidationResult(is_valid=True)
        result2 = ValidationResult(is_valid=False)
        result2.add_warning(WarningSeverity.CRITICAL, "Error 1")

        result1.merge(result2)

        assert result1.is_valid is False  # Merged result should be invalid

    def test_is_valid_updates_on_error(self):
        """Test is_valid updates when errors are added."""
        result = ValidationResult(is_valid=True)
        assert result.is_valid is True

        result.add_warning(WarningSeverity.CRITICAL, "Error")
        assert result.is_valid is False

        # Adding more warnings doesn't change is_valid state
        result.add_warning(WarningSeverity.WARNING, "Warning")
        assert result.is_valid is False  # Still invalid due to error

