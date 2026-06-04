"""
Main cohort validator that runs all validation checks.
"""

from typing import List, Optional

from ..models.cohort import CohortExpression
from ..models.validation import ValidationResult, WarningSeverity
from .concept_checks import (
    DuplicatesConceptSetCheck,
    EmptyConceptSetCheck,
    UnusedConceptsCheck,
)
from .criteria_checks import (
    AdditionalCriteriaWarningCheck,
    AttributeCheck,
    CriteriaContradictionsCheck,
    DeathTimeWindowCheck,
    DomainTypeCheck,
    DrugDomainCheck,
    DrugEraCheck,
    DuplicatePrimaryCriteriaCheck,
    DuplicatesCriteriaCheck,
    EmptyAdditionalCriteriaValueCheck,
    EmptyCensoringCriteriaValueCheck,
    CensoringEventsWarningCheck,
    EmptyDemographicValueCheck,
    EmptyPrimaryCriteriaValueCheck,
    EventsProgressionCheck,
    IncompleteRuleCheck,
    InitialEventCheck,
    MissingConceptSetPrimaryCheck,
    MissingConceptSetInclusionCheck,
    NoExitCriteriaCheck,
    PrimaryCriteriaWarningCheck,
    RangeCheck,
    TimePatternCheck,
    TimeWindowCheck,
)


class CohortValidator:
    """Main validator for cohort definitions."""

    def __init__(self):
        """Initialize the validator with all checks."""
        self.checks = [
            # Concept checks
            UnusedConceptsCheck(),
            EmptyConceptSetCheck(),
            DuplicatesConceptSetCheck(),
            # Criteria checks
            RangeCheck(),
            AttributeCheck(),
            IncompleteRuleCheck(),
            InitialEventCheck(),
            DrugEraCheck(),
            DuplicatesCriteriaCheck(),
            DuplicatePrimaryCriteriaCheck(),
            DrugDomainCheck(),
            EventsProgressionCheck(),
            TimeWindowCheck(),
            TimePatternCheck(),
            DomainTypeCheck(),
            CriteriaContradictionsCheck(),
            DeathTimeWindowCheck(),
            EmptyDemographicValueCheck(),
            EmptyPrimaryCriteriaValueCheck(),
            PrimaryCriteriaWarningCheck(),
            EmptyAdditionalCriteriaValueCheck(),
            AdditionalCriteriaWarningCheck(),
            EmptyCensoringCriteriaValueCheck(),
            CensoringEventsWarningCheck(),
            MissingConceptSetPrimaryCheck(),
            MissingConceptSetInclusionCheck(),
            NoExitCriteriaCheck(),
        ]

    def validate(self, expression: CohortExpression) -> ValidationResult:
        """
        Validate a cohort expression and return comprehensive results.

        Args:
            expression: The cohort expression to validate

        Returns:
            ValidationResult with all warnings, errors, and info messages
        """
        result = ValidationResult(is_valid=True)

        # Run all checks and collect all warnings
        for check in self.checks:
            try:
                warnings = check.check(expression)
                for warning in warnings:
                    result.add_warning(
                        severity=warning.severity,
                        message=warning.to_message(),
                        concept_set=getattr(warning, "concept_set", None),
                    )
            except Exception as e:
                # If a check fails, add it as an error with a user-friendly message
                error_message = self._clean_error_message(str(e))
                result.add_warning(
                    severity=WarningSeverity.CRITICAL,
                    message=f"Validation check failed: {error_message}",
                )

        return result

    def validate_json(self, json_str: str) -> ValidationResult:
        """
        Validate a cohort expression from JSON string.

        Args:
            json_str: JSON string containing the cohort definition

        Returns:
            ValidationResult with all warnings, errors, and info messages
        """
        result = ValidationResult(is_valid=True)

        # First, run JSON-level checks (like invalid criteria types)
        for check in self.checks:
            if hasattr(check, "check_json"):
                try:
                    check.check_json(json_str, result)
                except Exception as e:
                    result.add_warning(
                        severity=WarningSeverity.CRITICAL,
                        message=f"JSON validation check failed: {str(e)}",
                    )

        # Try to parse the JSON
        try:
            expression = CohortExpression.from_json(json_str)
            # If parsing succeeds, run full validation
            validation_result = self.validate(expression)
            # Merge the results
            result.merge(validation_result)
        except Exception as e:
            # If parsing fails, add the error but continue with partial validation
            result.is_valid = False
            # Clean up the error message to be more user-friendly
            error_message = self._clean_error_message(str(e))
            result.add_warning(
                severity=WarningSeverity.CRITICAL,
                message=f"Failed to parse cohort definition: {error_message}",
            )

            # Try to parse as much as possible for partial validation
            try:
                import json

                data = json.loads(json_str)

                # Handle wrapper objects like {"cohort_definition": {...}}
                if "cohort_definition" in data:
                    data = data["cohort_definition"]

                # Try to create a partial expression for validation
                # We'll create a minimal valid structure and then update it
                partial_expression = self._create_partial_expression(data)
                if partial_expression:
                    # Run validation on the partial expression
                    partial_result = self.validate(partial_expression)
                    result.merge(partial_result)

            except Exception as parse_error:
                # If even partial parsing fails, just add the error
                error_message = self._clean_error_message(str(parse_error))
                result.add_warning(
                    severity=WarningSeverity.CRITICAL,
                    message=f"Failed to parse JSON: {error_message}",
                )

        return result

    def _clean_error_message(self, error_message: str) -> str:
        """Clean up technical error messages to be more user-friendly."""
        # Handle Pydantic validation errors
        if "validation error for" in error_message:
            # Extract the field name and error type
            lines = error_message.split("\n")
            if len(lines) >= 2:
                field_line = lines[1].strip()
                # Clean up field names to be more readable
                field_name = self._format_validation_path(field_line)
                field_name = field_name.replace("CollapseSettings ", "").replace(
                    "CollapseType", "Collapse Type"
                )
                field_name = field_name.replace(
                    "PrimaryCriteria ", "Primary Criteria "
                ).replace("InclusionRules ", "Inclusion Rule ")
                field_name = field_name.replace("ConceptSets ", "Concept Set ").replace(
                    "CriteriaList ", "Criteria "
                )

                # Look for specific error patterns and provide user-friendly messages
                if (
                    "Input should be 'ERA'" in error_message
                    and "input_value=''" in error_message
                ):
                    return f"Collapse Type field is empty. Please set it to 'ERA' or remove the field to use the default value."
                elif "Input should be 'ERA'" in error_message:
                    return f"Collapse Type field has an invalid value. Please set it to 'ERA'."
                elif "Input should be" in error_message:
                    return f"Field '{field_name}' has an invalid value. Please check the allowed values."
                elif "Field required" in error_message:
                    return f"Required field '{field_name}' is missing."
                elif "Extra inputs are not permitted" in error_message:
                    return f"Field '{field_name}' contains unexpected data. Please check the field name and structure."
                else:
                    return f"Field '{field_name}' has an invalid value."

        # Handle comparison errors
        if "'<' not supported between instances of 'dict' and 'dict'" in error_message:
            return "Unable to compare concept sets due to complex data structure. Please check that concept sets are properly defined."
        elif "not supported between instances" in error_message:
            return "Unable to compare data due to incompatible data types. Please check the data structure."

        # Handle JSON parsing errors
        if "Expecting" in error_message and "JSON" in error_message:
            return "Invalid JSON format. Please check the file structure and syntax."
        elif "JSONDecodeError" in error_message:
            return "Invalid JSON format. Please check the file structure and syntax."

        # Clean up other technical terms
        cleaned = error_message
        cleaned = cleaned.replace("type=enum", "type")
        cleaned = cleaned.replace("input_value=", "value: ")
        cleaned = cleaned.replace("input_type=", "type: ")
        cleaned = cleaned.replace(
            "For further information visit", "For more details, see"
        )
        cleaned = cleaned.replace("Pydantic", "Validation")
        cleaned = cleaned.replace("BaseModel", "Data Model")

        return cleaned

    def _format_validation_path(self, field_path: str) -> str:
        """Format Pydantic field paths and show list indexes as 1-based."""
        formatted_parts = []
        for part in field_path.split("."):
            if part.isdigit():
                formatted_parts.append(str(int(part) + 1))
            else:
                formatted_parts.append(part)
        return " ".join(formatted_parts)

    def _create_partial_expression(self, data: dict) -> Optional[CohortExpression]:
        """Create a partial expression for validation when full parsing fails."""
        try:
            # Create a minimal valid expression with default values
            from ..models.base import CollapseSettings, CollapseType
            from ..models.cohort import CohortExpression

            # Set default values for required fields that might be causing parsing issues
            if "CollapseSettings" in data:
                collapse_settings = data["CollapseSettings"]
                if collapse_settings.get("CollapseType") == "":
                    collapse_settings["CollapseType"] = "ERA"

            # Try to create the expression with the corrected data
            return CohortExpression(**data)
        except Exception:
            # If we still can't create a partial expression, return None
            return None

    def get_validation_summary(self, result: ValidationResult) -> str:
        """
        Get a human-readable summary of validation results.

        Args:
            result: The validation result

        Returns:
            Human-readable summary string
        """
        return result._get_summary_text()

    def get_all_messages(self, result: ValidationResult) -> List[str]:
        """
        Get all validation messages as a list.

        Args:
            result: The validation result

        Returns:
            List of all validation messages
        """
        return result.get_all_messages()

    def get_messages_by_severity(
        self, result: ValidationResult, severity: WarningSeverity
    ) -> List[str]:
        """
        Get validation messages by severity level.

        Args:
            result: The validation result
            severity: The severity level to filter by

        Returns:
            List of messages with the specified severity
        """
        return result.get_messages_by_severity(severity)
