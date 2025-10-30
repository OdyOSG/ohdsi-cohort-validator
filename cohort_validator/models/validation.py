"""
Validation models for warnings, errors, and validation results.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .concept import ConceptSet


class WarningSeverity(str, Enum):
    """Warning severity levels."""

    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class Warning(BaseModel):
    """Base warning class."""

    severity: WarningSeverity
    message: str

    def to_message(self) -> str:
        """Get the warning message."""
        return self.message


class DefaultWarning(Warning):
    """Default warning with severity and message."""

    def __init__(self, severity: WarningSeverity, message: str, **data):
        super().__init__(severity=severity, message=message, **data)


class ConceptSetWarning(Warning):
    """Warning specific to a concept set."""

    concept_set: Optional[ConceptSet] = Field(
        None, description="The concept set this warning refers to"
    )

    def __init__(
        self,
        severity: WarningSeverity,
        message: str,
        concept_set: Optional[ConceptSet] = None,
        **data,
    ):
        super().__init__(severity=severity, message=message, **data)
        self.concept_set = concept_set


class ValidationResult(BaseModel):
    """Result of cohort validation."""

    is_valid: bool = Field(description="Whether the cohort definition is valid")
    warnings: List[Warning] = Field(
        default_factory=list, description="List of warnings"
    )
    errors: List[Warning] = Field(default_factory=list, description="List of errors")
    info: List[Warning] = Field(
        default_factory=list, description="List of info messages"
    )

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0

    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    @property
    def has_info(self) -> bool:
        """Check if there are any info messages."""
        return len(self.info) > 0

    @property
    def total_issues(self) -> int:
        """Get total number of issues (warnings + errors + info)."""
        return len(self.warnings) + len(self.errors) + len(self.info)

    def add_warning(
        self,
        severity: WarningSeverity,
        message: str,
        concept_set: Optional[ConceptSet] = None,
    ):
        """Add a warning to the result."""
        if concept_set:
            warning = ConceptSetWarning(
                severity=severity, message=message, concept_set=concept_set
            )
        else:
            warning = DefaultWarning(severity=severity, message=message)

        if severity == WarningSeverity.CRITICAL:
            self.errors.append(warning)
        elif severity == WarningSeverity.WARNING:
            self.warnings.append(warning)
        else:
            self.info.append(warning)

        # Update is_valid based on errors
        self.is_valid = len(self.errors) == 0

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of validation results."""
        return {
            "is_valid": self.is_valid,
            "total_issues": self.total_issues,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "info": len(self.info),
            "summary": self._get_summary_text(),
        }

    def _get_summary_text(self) -> str:
        """Get human-readable summary text."""
        if self.is_valid and not self.has_warnings:
            return "Cohort definition is valid with no issues."
        elif self.is_valid:
            return f"Cohort definition is valid with {len(self.warnings)} warning(s) and {len(self.info)} info message(s)."
        else:
            return f"Cohort definition has {len(self.errors)} error(s), {len(self.warnings)} warning(s), and {len(self.info)} info message(s)."

    def get_all_messages(self) -> List[str]:
        """Get all warning/error messages as a list."""
        all_warnings = self.errors + self.warnings + self.info
        return [w.to_message() for w in all_warnings]

    def get_messages_by_severity(self, severity: WarningSeverity) -> List[str]:
        """Get messages by severity level."""
        if severity == WarningSeverity.CRITICAL:
            return [w.to_message() for w in self.errors]
        elif severity == WarningSeverity.WARNING:
            return [w.to_message() for w in self.warnings]
        else:
            return [w.to_message() for w in self.info]

    def merge(self, other: "ValidationResult") -> None:
        """Merge another validation result into this one."""
        # Merge all warnings
        self.warnings.extend(other.warnings)
        self.errors.extend(other.errors)
        self.info.extend(other.info)

        # Update is_valid - if either result is invalid, the merged result is invalid
        self.is_valid = self.is_valid and other.is_valid
