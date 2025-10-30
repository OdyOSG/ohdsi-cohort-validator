"""
Main cohort definition models.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from .base import CollapseSettings, CollapseType, ObservationFilter, Period, ResultLimit
from .concept import ConceptSet
from .criteria import (
    CorelatedCriteria,
    Criteria,
    CriteriaGroup,
    DemographicCriteria,
    EndStrategy,
)
from .validation import WarningSeverity


class PrimaryCriteria(BaseModel):
    """Primary criteria for cohort definition."""

    criteria_list: List[Criteria] = Field(default_factory=list, alias="CriteriaList")
    observation_window: Optional[ObservationFilter] = Field(
        None, alias="ObservationWindow"
    )
    primary_limit: ResultLimit = Field(
        default_factory=ResultLimit, alias="PrimaryCriteriaLimit"
    )


class InclusionRule(BaseModel):
    """Inclusion rule for cohort definition."""

    name: Optional[str] = Field(None, description="Name of the inclusion rule")
    description: Optional[str] = Field(
        None, description="Description of the inclusion rule"
    )
    expression: Optional[CriteriaGroup] = Field(
        None, description="Criteria group expression"
    )


class CohortExpression(BaseModel):
    """Main cohort definition model."""

    cdm_version_range: Optional[str] = Field(
        None, alias="cdmVersionRange", description="CDM version range requirement"
    )
    title: Optional[str] = Field(None, alias="Title", description="Title of the cohort")
    primary_criteria: Optional[PrimaryCriteria] = Field(
        None, alias="PrimaryCriteria", description="Primary criteria"
    )
    additional_criteria: Optional[CriteriaGroup] = Field(
        None, alias="AdditionalCriteria", description="Additional criteria"
    )
    concept_sets: List[ConceptSet] = Field(
        default_factory=list, alias="ConceptSets", description="Concept sets"
    )
    qualified_limit: ResultLimit = Field(
        default_factory=ResultLimit,
        alias="QualifiedLimit",
        description="Qualified limit",
    )
    expression_limit: ResultLimit = Field(
        default_factory=ResultLimit,
        alias="ExpressionLimit",
        description="Expression limit",
    )
    inclusion_rules: List[InclusionRule] = Field(
        default_factory=list, alias="InclusionRules", description="Inclusion rules"
    )
    end_strategy: Optional[EndStrategy] = Field(
        None, alias="EndStrategy", description="End strategy"
    )
    censoring_criteria: List[Criteria] = Field(
        default_factory=list,
        alias="CensoringCriteria",
        description="Censoring criteria",
    )
    collapse_settings: CollapseSettings = Field(
        default_factory=CollapseSettings,
        alias="CollapseSettings",
        description="Collapse settings",
    )
    censor_window: Optional[Period] = Field(
        None, alias="CensorWindow", description="Censor window"
    )

    @classmethod
    def from_json(cls, json_str: str) -> "CohortExpression":
        """Create CohortExpression from JSON string."""
        import json

        data = json.loads(json_str)

        # Handle wrapper objects like {"cohort_definition": {...}}
        if "cohort_definition" in data:
            data = data["cohort_definition"]

        return cls(**data)

    def to_json(self) -> str:
        """Convert CohortExpression to JSON string."""
        import json

        return json.dumps(self.model_dump(by_alias=True, exclude_none=True), indent=2)


# Update forward references
CohortExpression.model_rebuild()
