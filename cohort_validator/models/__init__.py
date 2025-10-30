"""
Pydantic models for cohort definition validation.
"""

from .base import CollapseType, DateRange, NumericRange, Period, ResultLimit, TextFilter
from .cohort import (
    CohortExpression,
    CollapseSettings,
    CriteriaGroup,
    InclusionRule,
    PrimaryCriteria,
)
from .concept import Concept, ConceptSet, ConceptSetExpression, ConceptSetSelection
from .criteria import (
    ConditionEra,
    ConditionOccurrence,
    CorelatedCriteria,
    Criteria,
    DateAdjustment,
    Death,
    DemographicCriteria,
    DeviceExposure,
    DoseEra,
    DrugEra,
    DrugExposure,
    LocationRegion,
    Measurement,
    Observation,
    ObservationPeriod,
    Occurrence,
    PayerPlanPeriod,
    ProcedureOccurrence,
    Specimen,
    VisitDetail,
    VisitOccurrence,
    Window,
    WindowedCriteria,
)
from .validation import (
    ConceptSetWarning,
    DefaultWarning,
    ValidationResult,
    Warning,
    WarningSeverity,
)

__all__ = [
    # Base models
    "DateRange",
    "NumericRange",
    "TextFilter",
    "ResultLimit",
    "Period",
    "CollapseType",
    # Concept models
    "Concept",
    "ConceptSetExpression",
    "ConceptSet",
    "ConceptSetSelection",
    # Cohort models
    "CohortExpression",
    "PrimaryCriteria",
    "CriteriaGroup",
    "InclusionRule",
    "CollapseSettings",
    # Criteria models
    "Criteria",
    "DrugExposure",
    "ConditionOccurrence",
    "VisitOccurrence",
    "VisitDetail",
    "ProcedureOccurrence",
    "Observation",
    "Measurement",
    "Death",
    "DeviceExposure",
    "Specimen",
    "PayerPlanPeriod",
    "ObservationPeriod",
    "ConditionEra",
    "DrugEra",
    "DoseEra",
    "LocationRegion",
    "DemographicCriteria",
    "CorelatedCriteria",
    "WindowedCriteria",
    "Window",
    "Occurrence",
    "DateAdjustment",
    # Validation models
    "Warning",
    "DefaultWarning",
    "ConceptSetWarning",
    "WarningSeverity",
    "ValidationResult",
]

