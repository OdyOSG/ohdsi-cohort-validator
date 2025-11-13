"""
Base validation classes for cohort definition validation.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional

from ..models.cohort import CohortExpression, CriteriaGroup, PrimaryCriteria
from ..models.criteria import CorelatedCriteria, Criteria
from ..models.validation import Warning, WarningSeverity


class WarningReporter:
    """Functional interface for reporting warnings."""

    def __init__(self, callback: Callable[[str, ...], None]):
        self.callback = callback

    def add(self, template: str, *params) -> None:
        """Add a warning with template and parameters."""
        self.callback(template, *params)


class BaseCheck(ABC):
    """Base class for all validation checks."""

    INCLUSION_RULE = "inclusion rule "
    ADDITIONAL_RULE = "additional rule"
    INITIAL_EVENT = "initial event"

    def check(self, expression: CohortExpression) -> List[Warning]:
        """Run the validation check and return warnings."""
        warnings = []
        reporter = self._create_reporter(warnings)
        self._check(expression, reporter)
        return warnings

    def _create_reporter(self, warnings: List[Warning]) -> WarningReporter:
        """Create a warning reporter for this check."""
        severity = self._define_severity()
        return WarningReporter(
            lambda template, *params: warnings.append(
                self._create_warning(severity, template, *params)
            )
        )

    def _create_warning(
        self, severity: WarningSeverity, template: str, *params
    ) -> Warning:
        """Create a warning instance."""
        from ..models.validation import DefaultWarning

        message = template.format(*params) if params else template
        return DefaultWarning(severity=severity, message=message)

    def _define_severity(self) -> WarningSeverity:
        """Define the default severity for this check."""
        return WarningSeverity.CRITICAL

    @abstractmethod
    def _check(self, expression: CohortExpression, reporter: WarningReporter) -> None:
        """Perform the actual validation check."""
        pass


class BaseValueCheck(BaseCheck):
    """Base class for value-based validation checks."""

    INCLUSION_CRITERIA = "Inclusion criteria "
    PRIMARY_CRITERIA = "Primary criteria"
    ADDITIONAL_CRITERIA = "Additional criteria"
    CENSORING_CRITERIA = "Censoring events"

    def _check(self, expression: CohortExpression, reporter: WarningReporter) -> None:
        """Check all criteria in the expression."""
        self._check_primary_criteria(expression.primary_criteria, reporter)
        self._check_additional_criteria(expression.additional_criteria, reporter)
        self._check_inclusion_rules(expression, reporter)
        self._check_censoring_criteria(expression, reporter)

    def _check_primary_criteria(
        self, primary_criteria: Optional[PrimaryCriteria], reporter: WarningReporter
    ) -> None:
        """Check primary criteria."""
        if primary_criteria and primary_criteria.criteria_list:
            for criteria in primary_criteria.criteria_list:
                self._check_criteria(criteria, reporter, self.PRIMARY_CRITERIA)

    def _check_additional_criteria(
        self, criteria_group: Optional[CriteriaGroup], reporter: WarningReporter
    ) -> None:
        """Check additional criteria."""
        if criteria_group:
            for criteria in criteria_group.criteria_list:
                self._check_criteria(criteria, reporter, self.ADDITIONAL_CRITERIA)
            for criteria in criteria_group.demographic_criteria_list:
                self._check_criteria(criteria, reporter, self.ADDITIONAL_CRITERIA)
            for group in criteria_group.groups:
                self._check_additional_criteria(group, reporter)

    def _check_censoring_criteria(
        self, expression: CohortExpression, reporter: WarningReporter
    ) -> None:
        """Check censoring criteria."""
        if expression.censoring_criteria:
            for criteria in expression.censoring_criteria:
                self._check_criteria(criteria, reporter, self.CENSORING_CRITERIA)

    def _check_inclusion_rules(
        self, expression: CohortExpression, reporter: WarningReporter
    ) -> None:
        """Check inclusion rules."""
        for rule in expression.inclusion_rules:
            if rule.expression:
                for criteria in rule.expression.criteria_list:
                    self._check_criteria(
                        criteria, reporter, f'{self.INCLUSION_CRITERIA}"{rule.name}"'
                    )
                for criteria in rule.expression.demographic_criteria_list:
                    self._check_criteria(
                        criteria, reporter, f'{self.INCLUSION_CRITERIA}"{rule.name}"'
                    )

    def _check_criteria(
        self, criteria: Any, reporter: WarningReporter, name: str
    ) -> None:
        """Check individual criteria (handles Criteria, CorelatedCriteria, and DemographicCriteria)."""
        # Check for CorelatedCriteria (has start_window, end_window, occurrence attributes)
        if (
            hasattr(criteria, "start_window")
            or hasattr(criteria, "end_window")
            or hasattr(criteria, "occurrence")
        ):
            # This is a CorelatedCriteria
            if hasattr(criteria, "criteria") and criteria.criteria:
                self._check_criteria(criteria.criteria, reporter, name)
        # Check for DemographicCriteria (has age, gender, race, ethnicity attributes)
        elif (
            hasattr(criteria, "age")
            or hasattr(criteria, "gender")
            or hasattr(criteria, "race")
            or hasattr(criteria, "ethnicity")
        ):
            # This is a DemographicCriteria
            self._get_factory(reporter, name).check(criteria)
        # Otherwise, it's a Criteria
        else:
            # Check regular criteria
            if (
                hasattr(criteria, "correlated_criteria")
                and criteria.correlated_criteria
            ):
                self._check_criteria_group(criteria.correlated_criteria, reporter, name)
            self._get_factory(reporter, name).check(criteria)

    def _check_criteria_group(
        self, criteria_group: CriteriaGroup, reporter: WarningReporter, name: str
    ) -> None:
        """Check criteria group."""
        for criteria in criteria_group.criteria_list:
            self._check_criteria(criteria, reporter, name)
        for criteria in criteria_group.demographic_criteria_list:
            self._check_criteria(criteria, reporter, name)
        for group in criteria_group.groups:
            self._check_criteria_group(group, reporter, name)

    @abstractmethod
    def _get_factory(
        self, reporter: WarningReporter, name: str
    ) -> "BaseCheckerFactory":
        """Get the appropriate checker factory."""
        pass


class BaseCorelatedCriteriaCheck(BaseCheck):
    """Base class for correlated criteria validation checks."""

    def _check(self, expression: CohortExpression, reporter: WarningReporter) -> None:
        """Check all inclusion rules for correlated criteria."""
        for inclusion_rule in expression.inclusion_rules:
            if inclusion_rule.expression:
                for criteria in inclusion_rule.expression.criteria_list:
                    self._check_criteria(
                        criteria,
                        f"{self.INCLUSION_RULE}{inclusion_rule.name}",
                        reporter,
                    )
                    self._check_criteria_group(
                        criteria.criteria,
                        f"{self.INCLUSION_RULE}{inclusion_rule.name}",
                        reporter,
                    )

    def _check_criteria_group(
        self, criteria: Optional[Criteria], group_name: str, reporter: WarningReporter
    ) -> None:
        """Check criteria group for correlated criteria."""
        if criteria and criteria.correlated_criteria:
            for correlated_criteria in criteria.correlated_criteria.criteria_list:
                self._check_criteria(correlated_criteria, group_name, reporter)
                self._check_criteria_group(
                    correlated_criteria.criteria, group_name, reporter
                )
            for group in criteria.correlated_criteria.groups:
                for correlated_criteria in group.criteria_list:
                    self._check_criteria(correlated_criteria, group_name, reporter)
                    self._check_criteria_group(
                        correlated_criteria.criteria, group_name, reporter
                    )

    @abstractmethod
    def _check_criteria(
        self, criteria: CorelatedCriteria, group_name: str, reporter: WarningReporter
    ) -> None:
        """Check individual correlated criteria."""
        pass


class BaseCheckerFactory(ABC):
    """Base class for checker factories."""

    def __init__(self, reporter: WarningReporter, name: str):
        self.reporter = reporter
        self.name = name

    @abstractmethod
    def check(self, criteria: Any) -> None:
        """Check the criteria."""
        pass
