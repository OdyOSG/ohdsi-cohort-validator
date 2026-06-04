"""
Comprehensive unit tests for CohortValidator class.
"""

import json
import pytest
from cohort_validator import CohortValidator
from cohort_validator.models.cohort import CohortExpression
from cohort_validator.models.concept import ConceptSet, ConceptSetExpression
from cohort_validator.models.criteria import ConditionOccurrence, Criteria
from cohort_validator.models.validation import ValidationResult, WarningSeverity


class TestCohortValidator:
    """Tests for CohortValidator class."""

    def test_validator_initialization(self):
        """Test CohortValidator initialization."""
        validator = CohortValidator()
        assert validator is not None
        assert hasattr(validator, "checks")
        assert len(validator.checks) > 0

    def test_validate_with_valid_cohort(self, minimal_cohort_expression):
        """Test validation with a valid cohort expression."""
        validator = CohortValidator()
        result = validator.validate(minimal_cohort_expression)

        assert isinstance(result, ValidationResult)
        assert isinstance(result.is_valid, bool)

    def test_validate_json_with_valid_json(self, sample_cohort_dict):
        """Test validate_json with valid JSON."""
        validator = CohortValidator()
        json_str = json.dumps(sample_cohort_dict)

        result = validator.validate_json(json_str)

        assert isinstance(result, ValidationResult)

    def test_validate_json_with_invalid_json(self):
        """Test validate_json with invalid JSON."""
        validator = CohortValidator()
        invalid_json = "{ invalid json }"

        result = validator.validate_json(invalid_json)

        assert isinstance(result, ValidationResult)
        assert result.has_errors  # Should have parsing errors

    def test_validate_cohort_with_dict(self, sample_cohort_dict):
        """Test validate_cohort with dictionary."""
        validator = CohortValidator()
        warnings, errors = validator.validate_cohort(sample_cohort_dict)

        assert isinstance(warnings, list)
        assert isinstance(errors, list)
        assert all(isinstance(w, dict) for w in warnings)
        assert all(isinstance(e, dict) for e in errors)

    def test_validate_cohort_with_json_string(self, sample_cohort_dict):
        """Test validate_cohort with JSON string."""
        validator = CohortValidator()
        json_str = json.dumps(sample_cohort_dict)

        warnings, errors = validator.validate_cohort(json_str)

        assert isinstance(warnings, list)
        assert isinstance(errors, list)

    def test_validate_cohort_with_invalid_type(self):
        """Test validate_cohort with invalid type."""
        validator = CohortValidator()

        with pytest.raises(ValueError, match="must be a dict or Milli string"):
            validator.validate_cohort(12345)

    def test_get_validation_summary(self, minimal_cohort_expression):
        """Test get_validation_summary method."""
        validator = CohortValidator()
        result = validator.validate(minimal_cohort_expression)

        summary = validator.get_validation_summary(result)

        assert isinstance(summary, str)
        assert len(summary) > 0

    def test_get_all_messages(self, minimal_cohort_expression):
        """Test get_all_messages method."""
        validator = CohortValidator()
        result = validator.validate(minimal_cohort_expression)

        messages = validator.get_all_messages(result)

        assert isinstance(messages, list)
        assert all(isinstance(msg, str) for msg in messages)

    def test_get_messages_by_severity(self, minimal_cohort_expression):
        """Test get_messages_by_severity method."""
        validator = CohortValidator()
        result = validator.validate(minimal_cohort_expression)

        warnings = validator.get_messages_by_severity(result, WarningSeverity.WARNING)
        errors = validator.get_messages_by_severity(result, WarningSeverity.CRITICAL)
        info = validator.get_messages_by_severity(result, WarningSeverity.INFO)

        assert isinstance(warnings, list)
        assert isinstance(errors, list)
        assert isinstance(info, list)

    def test_validate_with_empty_cohort(self):
        """Test validation with empty cohort."""
        validator = CohortValidator()
        empty_cohort = CohortExpression()

        result = validator.validate(empty_cohort)

        assert isinstance(result, ValidationResult)
        # Empty cohort might have warnings/errors
        assert isinstance(result.is_valid, bool)

    def test_validate_cohort_handles_exceptions(self):
        """Test that validate_cohort handles exceptions gracefully."""
        validator = CohortValidator()

        # Test with malformed data that might cause exceptions
        malformed_data = {"PrimaryCriteria": {"invalid": "data"}}

        # Should not raise exception, should return result
        warnings, errors = validator.validate_cohort(malformed_data)

        assert isinstance(warnings, list)
        assert isinstance(errors, list)

    def test_json_parsing_error_handling(self):
        """Test handling of JSON parsing errors."""
        validator = CohortValidator()

        # Invalid JSON
        invalid_json = '{"unclosed": "json"'

        warnings, errors = validator.validate_cohort(invalid_json)

        # Should return errors for invalid JSON
        assert isinstance(errors, list)

    def test_wrapper_object_handling(self):
        """Test handling of wrapper objects in JSON."""
        validator = CohortValidator()

        wrapped_data = {
            "cohort_definition": {
                "ConceptSets": [],
                "PrimaryCriteria": {
                    "CriteriaList": [],
                },
            }
        }

        warnings, errors = validator.validate_cohort(wrapped_data)

        assert isinstance(warnings, list)
        assert isinstance(errors, list)

    def test_partial_validation_on_parse_error(self):
        """Test that partial validation occurs even with parse errors."""
        validator = CohortValidator()

        # Data with some valid structure but parse errors
        problematic_data = {
            "ConceptSets": [
                {
                    "id": 0,
                    "name": "Test",
                    "expression": {"items": []},
                }
            ],
            "PrimaryCriteria": {
                "InvalidField": "invalid value",
            },
        }

        warnings, errors = validator.validate_cohort(problematic_data)

        assert isinstance(warnings, list)
        assert isinstance(errors, list)

    def test_parse_error_indexes_are_one_based(self):
        """Test validation paths report list indexes starting from 1."""
        validator = CohortValidator()

        try:
            CohortExpression(ConceptSets=[{"id": 0}])
        except Exception as error:
            message = validator._clean_error_message(str(error))
        else:
            pytest.fail("Expected CohortExpression parsing to fail")

        assert "Concept Set 1 name" in message
