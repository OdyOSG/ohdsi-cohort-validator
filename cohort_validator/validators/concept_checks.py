"""
Concept-related validation checks.
"""

from typing import List, Optional

from ..models.cohort import CohortExpression, ConceptSet
from ..models.validation import ConceptSetWarning, WarningSeverity
from .base import BaseCheck, BaseIterableCheck, WarningReporter


class EmptyConceptSetCheck(BaseCheck):
    """Check for empty concept sets."""

    EMPTY_ERROR = 'Concept set "{}" contains no concepts'

    def _check(self, expression: CohortExpression, reporter: WarningReporter) -> None:
        """Check for empty concept sets."""
        for concept_set in expression.concept_sets:
            if (
                not concept_set.expression
                or not concept_set.expression.items
                or len(concept_set.expression.items) == 0
            ):
                reporter.add(self.EMPTY_ERROR, concept_set.name)


class DuplicatesConceptSetCheck(BaseCheck):
    """Check for duplicate concept sets."""

    DUPLICATES_WARNING = 'Concept set "{}" contains the same concepts like {}'

    def _define_severity(self) -> WarningSeverity:
        return WarningSeverity.INFO

    def _check(self, expression: CohortExpression, reporter: WarningReporter) -> None:
        """Check for duplicate concept sets."""
        if len(expression.concept_sets) > 1:
            for i, concept_set in enumerate(expression.concept_sets):
                duplicates = []
                for j, other_concept_set in enumerate(
                    expression.concept_sets[i + 1 :], i + 1
                ):
                    if self._are_concept_sets_equal(concept_set, other_concept_set):
                        duplicates.append(other_concept_set.name)

                if duplicates:
                    reporter.add(
                        self.DUPLICATES_WARNING,
                        concept_set.name,
                        ", ".join(duplicates),
                    )

    def _are_concept_sets_equal(self, set1: ConceptSet, set2: ConceptSet) -> bool:
        """Check if two concept sets are equal."""
        if not set1.expression or not set2.expression:
            return False

        items1 = set1.expression.items or []
        items2 = set2.expression.items or []

        if len(items1) != len(items2):
            return False

        # Simple comparison - convert to JSON strings for safe comparison
        try:
            import json

            items1_json = [
                json.dumps(item.model_dump(), sort_keys=True) for item in items1
            ]
            items2_json = [
                json.dumps(item.model_dump(), sort_keys=True) for item in items2
            ]
            return sorted(items1_json) == sorted(items2_json)
        except Exception:
            # Fallback to string comparison if JSON serialization fails
            return str(items1) == str(items2)


class UnusedConceptsCheck(BaseIterableCheck):
    """Check for unused concept sets."""

    UNUSED_WARNING = 'Concept Set "{}" is not used'

    def _define_severity(self) -> WarningSeverity:
        return WarningSeverity.WARNING

    def _internal_check(
        self, expression: CohortExpression, reporter: WarningReporter
    ) -> None:
        """Check for unused concept sets."""
        additional_criteria = self._get_additional_criteria(expression)

        for concept_set in expression.concept_sets:
            if not self._is_concept_set_used(
                expression, additional_criteria, concept_set
            ):
                reporter.add(self.UNUSED_WARNING, concept_set.name)

    def _get_additional_criteria(self, expression: CohortExpression) -> List:
        """Get all additional criteria."""
        additional_criteria = []
        if expression.additional_criteria:
            additional_criteria.extend(expression.additional_criteria.criteria_list)
            additional_criteria.extend(
                self._get_criteria_from_groups(expression.additional_criteria.groups)
            )
        return additional_criteria

    def _get_criteria_from_groups(self, groups: List) -> List:
        """Recursively get criteria from groups."""
        criteria = []
        for group in groups:
            criteria.extend(group.criteria_list)
            criteria.extend(self._get_criteria_from_groups(group.groups))
        return criteria

    def _is_concept_set_used(
        self,
        expression: CohortExpression,
        additional_criteria: List,
        concept_set: ConceptSet,
    ) -> bool:
        """Check if a concept set is used anywhere."""
        # Check primary criteria
        if expression.primary_criteria and expression.primary_criteria.criteria_list:
            if self._is_concept_set_used_in_criteria_list(
                expression.primary_criteria.criteria_list, concept_set
            ):
                return True

        # Check additional criteria
        if self._is_concept_set_used_in_criteria_list(additional_criteria, concept_set):
            return True

        # Check inclusion rules
        for rule in expression.inclusion_rules:
            if rule.expression and self._is_concept_set_used_in_criteria_group(
                rule.expression, concept_set
            ):
                return True

        # Check censoring criteria
        if self._is_concept_set_used_in_criteria_list(
            expression.censoring_criteria, concept_set
        ):
            return True

        return False

    def _is_concept_set_used_in_criteria_list(
        self, criteria_list: List, concept_set: ConceptSet
    ) -> bool:
        """Check if concept set is used in a criteria list."""
        for criteria in criteria_list:
            # Check if criteria has codeset_id directly
            if (
                hasattr(criteria, "codeset_id")
                and criteria.codeset_id == concept_set.id
            ):
                return True

            # Check if this is a CorelatedCriteria with a nested Criteria
            if hasattr(criteria, "criteria") and criteria.criteria:
                codeset_id = self._get_codeset_id_from_criteria(criteria.criteria)
                if codeset_id == concept_set.id:
                    return True

            # Check domain-specific criteria
            codeset_id = self._get_codeset_id_from_criteria(criteria)
            if codeset_id == concept_set.id:
                return True

            if (
                hasattr(criteria, "correlated_criteria")
                and criteria.correlated_criteria
            ):
                if self._is_concept_set_used_in_criteria_group(
                    criteria.correlated_criteria, concept_set
                ):
                    return True
        return False

    def _get_codeset_id_from_criteria(self, criteria) -> Optional[int]:
        """Get codeset ID from criteria."""
        if hasattr(criteria, "drug_exposure") and criteria.drug_exposure:
            return criteria.drug_exposure.codeset_id
        elif (
            hasattr(criteria, "condition_occurrence") and criteria.condition_occurrence
        ):
            return criteria.condition_occurrence.codeset_id
        elif hasattr(criteria, "visit_occurrence") and criteria.visit_occurrence:
            return criteria.visit_occurrence.codeset_id
        elif (
            hasattr(criteria, "procedure_occurrence") and criteria.procedure_occurrence
        ):
            return criteria.procedure_occurrence.codeset_id
        elif hasattr(criteria, "observation") and criteria.observation:
            return criteria.observation.codeset_id
        elif hasattr(criteria, "measurement") and criteria.measurement:
            return criteria.measurement.codeset_id
        elif hasattr(criteria, "death") and criteria.death:
            return criteria.death.codeset_id
        elif hasattr(criteria, "device_exposure") and criteria.device_exposure:
            return criteria.device_exposure.codeset_id
        elif hasattr(criteria, "specimen") and criteria.specimen:
            return criteria.specimen.codeset_id
        elif hasattr(criteria, "condition_era") and criteria.condition_era:
            return criteria.condition_era.codeset_id
        elif hasattr(criteria, "drug_era") and criteria.drug_era:
            return criteria.drug_era.codeset_id
        elif hasattr(criteria, "dose_era") and criteria.dose_era:
            return criteria.dose_era.codeset_id
        elif hasattr(criteria, "visit_detail") and criteria.visit_detail:
            return criteria.visit_detail.codeset_id
        elif hasattr(criteria, "location_region") and criteria.location_region:
            return criteria.location_region.codeset_id
        return None

    def _is_concept_set_used_in_criteria_group(
        self, criteria_group, concept_set: ConceptSet
    ) -> bool:
        """Check if concept set is used in a criteria group."""
        if self._is_concept_set_used_in_criteria_list(
            criteria_group.criteria_list, concept_set
        ):
            return True
        for group in criteria_group.groups:
            if self._is_concept_set_used_in_criteria_group(group, concept_set):
                return True
        return False


class ConceptSetSelectionCheck(BaseCheck):
    """Check concept set selections."""

    def _check(self, expression: CohortExpression, reporter: WarningReporter) -> None:
        """Check concept set selections."""
        # This would implement concept set selection validation
        # For now, it's a placeholder
        pass


class ConceptCheck(BaseCheck):
    """Check individual concepts."""

    def _check(self, expression: CohortExpression, reporter: WarningReporter) -> None:
        """Check individual concepts."""
        # This would implement concept validation
        # For now, it's a placeholder
        pass
