"""
Criteria models for different domain types in cohort definitions.
"""

from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from .base import DateAdjustment, DateRange, NumericRange, Period, TextFilter
from .concept import Concept, ConceptSetSelection


class Criteria(BaseModel):
    """Base class for all criteria types."""

    correlated_criteria: Optional["CriteriaGroup"] = Field(
        None, alias="CorrelatedCriteria"
    )
    date_adjustment: Optional[DateAdjustment] = Field(None, alias="DateAdjustment")

    @field_validator("*", mode="before")
    @classmethod
    def convert_numeric_values_to_numeric_range(cls, v, info):
        """Convert simple numeric values to NumericRange when the field expects NumericRange."""
        if isinstance(v, (int, float)) and info.field_name:
            # Check if the field is supposed to be a NumericRange
            field_info = cls.model_fields.get(info.field_name)
            if field_info and hasattr(field_info, "annotation"):
                # Check if the annotation is NumericRange or Optional[NumericRange]
                annotation = field_info.annotation
                if hasattr(annotation, "__origin__") and annotation.__origin__ is Union:
                    # Handle Optional[NumericRange] case
                    args = annotation.__args__
                    if len(args) == 2 and type(None) in args:
                        other_type = args[0] if args[1] is type(None) else args[1]
                        if other_type == NumericRange:
                            return NumericRange(value=v, op="eq")
                elif annotation == NumericRange:
                    return NumericRange(value=v, op="eq")
        return v

    # Domain-specific criteria fields
    drug_exposure: Optional["DrugExposure"] = Field(None, alias="DrugExposure")
    condition_occurrence: Optional["ConditionOccurrence"] = Field(
        None, alias="ConditionOccurrence"
    )
    visit_occurrence: Optional["VisitOccurrence"] = Field(None, alias="VisitOccurrence")
    visit_detail: Optional["VisitDetail"] = Field(None, alias="VisitDetail")
    procedure_occurrence: Optional["ProcedureOccurrence"] = Field(
        None, alias="ProcedureOccurrence"
    )
    observation: Optional["Observation"] = Field(None, alias="Observation")
    measurement: Optional["Measurement"] = Field(None, alias="Measurement")
    death: Optional["Death"] = Field(None, alias="Death")
    device_exposure: Optional["DeviceExposure"] = Field(None, alias="DeviceExposure")
    specimen: Optional["Specimen"] = Field(None, alias="Specimen")
    payer_plan_period: Optional["PayerPlanPeriod"] = Field(
        None, alias="PayerPlanPeriod"
    )
    observation_period: Optional["ObservationPeriod"] = Field(
        None, alias="ObservationPeriod"
    )
    condition_era: Optional["ConditionEra"] = Field(None, alias="ConditionEra")
    drug_era: Optional["DrugEra"] = Field(None, alias="DrugEra")
    dose_era: Optional["DoseEra"] = Field(None, alias="DoseEra")
    location_region: Optional["LocationRegion"] = Field(None, alias="LocationRegion")


class GeoCriteria(Criteria):
    """Base class for geographic criteria."""

    start_date: Optional[DateRange] = Field(None, alias="StartDate")
    end_date: Optional[DateRange] = Field(None, alias="EndDate")


class DrugExposure(Criteria):
    """Drug exposure criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    occurrence_end_date: Optional[DateRange] = Field(None, alias="OccurrenceEndDate")
    drug_type: Optional[List[Concept]] = Field(None, alias="DrugType")
    drug_type_cs: Optional[ConceptSetSelection] = Field(None, alias="DrugTypeCS")
    drug_type_exclude: bool = Field(False, alias="DrugTypeExclude")
    stop_reason: Optional[TextFilter] = Field(None, alias="StopReason")
    refills: Optional[NumericRange] = Field(None, alias="Refills")
    quantity: Optional[NumericRange] = Field(None, alias="Quantity")
    days_supply: Optional[NumericRange] = Field(None, alias="DaysSupply")
    route_concept: Optional[List[Concept]] = Field(None, alias="RouteConcept")
    route_concept_cs: Optional[ConceptSetSelection] = Field(
        None, alias="RouteConceptCS"
    )
    effective_drug_dose: Optional[NumericRange] = Field(None, alias="EffectiveDrugDose")
    dose_unit: Optional[List[Concept]] = Field(None, alias="DoseUnit")
    dose_unit_cs: Optional[ConceptSetSelection] = Field(None, alias="DoseUnitCS")
    lot_number: Optional[TextFilter] = Field(None, alias="LotNumber")
    drug_source_concept: Optional[int] = Field(None, alias="DrugSourceConcept")
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    provider_specialty: Optional[List[Concept]] = Field(None, alias="ProviderSpecialty")
    provider_specialty_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProviderSpecialtyCS"
    )
    visit_type: Optional[List[Concept]] = Field(None, alias="VisitType")
    visit_type_cs: Optional[ConceptSetSelection] = Field(None, alias="VisitTypeCS")


class ConditionOccurrence(Criteria):
    """Condition occurrence criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    occurrence_end_date: Optional[DateRange] = Field(None, alias="OccurrenceEndDate")
    condition_type: Optional[List[Concept]] = Field(None, alias="ConditionType")
    condition_type_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ConditionTypeCS"
    )
    condition_type_exclude: Optional[bool] = Field(None, alias="ConditionTypeExclude")
    stop_reason: Optional[TextFilter] = Field(None, alias="StopReason")
    condition_source_concept: Optional[int] = Field(
        None, alias="ConditionSourceConcept"
    )
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    provider_specialty: Optional[List[Concept]] = Field(None, alias="ProviderSpecialty")
    provider_specialty_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProviderSpecialtyCS"
    )
    visit_type: Optional[List[Concept]] = Field(None, alias="VisitType")
    visit_type_cs: Optional[ConceptSetSelection] = Field(None, alias="VisitTypeCS")
    condition_status: Optional[List[Concept]] = Field(None, alias="ConditionStatus")
    condition_status_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ConditionStatusCS"
    )


class VisitOccurrence(Criteria):
    """Visit occurrence criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    occurrence_end_date: Optional[DateRange] = Field(None, alias="OccurrenceEndDate")
    visit_type: Optional[List[Concept]] = Field(None, alias="VisitType")
    visit_type_cs: Optional[ConceptSetSelection] = Field(None, alias="VisitTypeCS")
    visit_type_exclude: bool = Field(False, alias="VisitTypeExclude")
    visit_source_concept: Optional[int] = Field(None, alias="VisitSourceConcept")
    visit_length: Optional[NumericRange] = Field(None, alias="VisitLength")
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    provider_specialty: Optional[List[Concept]] = Field(None, alias="ProviderSpecialty")
    provider_specialty_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProviderSpecialtyCS"
    )
    place_of_service: Optional[List[Concept]] = Field(None, alias="PlaceOfService")
    place_of_service_cs: Optional[ConceptSetSelection] = Field(
        None, alias="PlaceOfServiceCS"
    )
    place_of_service_location: Optional[int] = Field(
        None, alias="PlaceOfServiceLocation"
    )


class VisitDetail(Criteria):
    """Visit detail criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    visit_detail_start_date: Optional[DateRange] = Field(
        None, alias="VisitDetailStartDate"
    )
    visit_detail_end_date: Optional[DateRange] = Field(None, alias="VisitDetailEndDate")
    visit_detail_type_cs: Optional[ConceptSetSelection] = Field(
        None, alias="VisitDetailTypeCS"
    )
    visit_detail_source_concept: Optional[int] = Field(
        None, alias="VisitDetailSourceConcept"
    )
    visit_detail_length: Optional[NumericRange] = Field(None, alias="VisitDetailLength")
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    provider_specialty_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProviderSpecialtyCS"
    )
    place_of_service_cs: Optional[ConceptSetSelection] = Field(
        None, alias="PlaceOfServiceCS"
    )
    place_of_service_location: Optional[int] = Field(
        None, alias="PlaceOfServiceLocation"
    )


class ProcedureOccurrence(Criteria):
    """Procedure occurrence criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    procedure_type: Optional[List[Concept]] = Field(None, alias="ProcedureType")
    procedure_type_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProcedureTypeCS"
    )
    procedure_type_exclude: bool = Field(False, alias="ProcedureTypeExclude")
    modifier: Optional[List[Concept]] = Field(None, alias="Modifier")
    modifier_cs: Optional[ConceptSetSelection] = Field(None, alias="ModifierCS")
    quantity: Optional[NumericRange] = Field(None, alias="Quantity")
    procedure_source_concept: Optional[int] = Field(
        None, alias="ProcedureSourceConcept"
    )
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    provider_specialty: Optional[List[Concept]] = Field(None, alias="ProviderSpecialty")
    provider_specialty_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProviderSpecialtyCS"
    )
    visit_type: Optional[List[Concept]] = Field(None, alias="VisitType")
    visit_type_cs: Optional[ConceptSetSelection] = Field(None, alias="VisitTypeCS")


class Observation(Criteria):
    """Observation criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    observation_type: Optional[List[Concept]] = Field(None, alias="ObservationType")
    observation_type_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ObservationTypeCS"
    )
    observation_type_exclude: bool = Field(False, alias="ObservationTypeExclude")
    value_as_number: Optional[NumericRange] = Field(None, alias="ValueAsNumber")
    value_as_string: Optional[TextFilter] = Field(None, alias="ValueAsString")
    value_as_concept: Optional[List[Concept]] = Field(None, alias="ValueAsConcept")
    value_as_concept_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ValueAsConceptCS"
    )
    qualifier: Optional[List[Concept]] = Field(None, alias="Qualifier")
    qualifier_cs: Optional[ConceptSetSelection] = Field(None, alias="QualifierCS")
    unit: Optional[List[Concept]] = Field(None, alias="Unit")
    unit_cs: Optional[ConceptSetSelection] = Field(None, alias="UnitCS")
    observation_source_concept: Optional[int] = Field(
        None, alias="ObservationSourceConcept"
    )
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    provider_specialty: Optional[List[Concept]] = Field(None, alias="ProviderSpecialty")
    provider_specialty_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProviderSpecialtyCS"
    )
    visit_type: Optional[List[Concept]] = Field(None, alias="VisitType")
    visit_type_cs: Optional[ConceptSetSelection] = Field(None, alias="VisitTypeCS")


class Measurement(Criteria):
    """Measurement criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    measurement_type: Optional[List[Concept]] = Field(None, alias="MeasurementType")
    measurement_type_cs: Optional[ConceptSetSelection] = Field(
        None, alias="MeasurementTypeCS"
    )
    measurement_type_exclude: bool = Field(False, alias="MeasurementTypeExclude")
    operator: Optional[List[Concept]] = Field(None, alias="Operator")
    operator_cs: Optional[ConceptSetSelection] = Field(None, alias="OperatorCS")
    value_as_number: Optional[NumericRange] = Field(None, alias="ValueAsNumber")
    value_as_concept: Optional[List[Concept]] = Field(None, alias="ValueAsConcept")
    value_as_concept_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ValueAsConceptCS"
    )
    unit: Optional[List[Concept]] = Field(None, alias="Unit")
    unit_cs: Optional[ConceptSetSelection] = Field(None, alias="UnitCS")
    range_low: Optional[NumericRange] = Field(None, alias="RangeLow")
    range_high: Optional[NumericRange] = Field(None, alias="RangeHigh")
    range_low_ratio: Optional[NumericRange] = Field(None, alias="RangeLowRatio")
    range_high_ratio: Optional[NumericRange] = Field(None, alias="RangeHighRatio")
    abnormal: Optional[bool] = Field(None, alias="Abnormal")
    measurement_source_concept: Optional[int] = Field(
        None, alias="MeasurementSourceConcept"
    )
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    provider_specialty: Optional[List[Concept]] = Field(None, alias="ProviderSpecialty")
    provider_specialty_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProviderSpecialtyCS"
    )
    visit_type: Optional[List[Concept]] = Field(None, alias="VisitType")
    visit_type_cs: Optional[ConceptSetSelection] = Field(None, alias="VisitTypeCS")


class Death(Criteria):
    """Death criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    death_type: Optional[List[Concept]] = Field(None, alias="DeathType")
    death_type_cs: Optional[ConceptSetSelection] = Field(None, alias="DeathTypeCS")
    death_type_exclude: bool = Field(False, alias="DeathTypeExclude")
    death_source_concept: Optional[int] = Field(None, alias="DeathSourceConcept")
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")


class DeviceExposure(Criteria):
    """Device exposure criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    occurrence_end_date: Optional[DateRange] = Field(None, alias="OccurrenceEndDate")
    device_type: Optional[List[Concept]] = Field(None, alias="DeviceType")
    device_type_cs: Optional[ConceptSetSelection] = Field(None, alias="DeviceTypeCS")
    device_type_exclude: bool = Field(False, alias="DeviceTypeExclude")
    unique_device_id: Optional[TextFilter] = Field(None, alias="UniqueDeviceId")
    quantity: Optional[NumericRange] = Field(None, alias="Quantity")
    device_source_concept: Optional[int] = Field(None, alias="DeviceSourceConcept")
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    provider_specialty: Optional[List[Concept]] = Field(None, alias="ProviderSpecialty")
    provider_specialty_cs: Optional[ConceptSetSelection] = Field(
        None, alias="ProviderSpecialtyCS"
    )
    visit_type: Optional[List[Concept]] = Field(None, alias="VisitType")
    visit_type_cs: Optional[ConceptSetSelection] = Field(None, alias="VisitTypeCS")


class Specimen(Criteria):
    """Specimen criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    specimen_type: Optional[List[Concept]] = Field(None, alias="SpecimenType")
    specimen_type_cs: Optional[ConceptSetSelection] = Field(
        None, alias="SpecimenTypeCS"
    )
    specimen_type_exclude: bool = Field(False, alias="SpecimenTypeExclude")
    quantity: Optional[NumericRange] = Field(None, alias="Quantity")
    unit: Optional[List[Concept]] = Field(None, alias="Unit")
    unit_cs: Optional[ConceptSetSelection] = Field(None, alias="UnitCS")
    anatomic_site: Optional[List[Concept]] = Field(None, alias="AnatomicSite")
    anatomic_site_cs: Optional[ConceptSetSelection] = Field(
        None, alias="AnatomicSiteCS"
    )
    disease_status: Optional[List[Concept]] = Field(None, alias="DiseaseStatus")
    disease_status_cs: Optional[ConceptSetSelection] = Field(
        None, alias="DiseaseStatusCS"
    )
    source_id: Optional[TextFilter] = Field(None, alias="SourceId")
    specimen_source_concept: Optional[int] = Field(None, alias="SpecimenSourceConcept")
    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")


class PayerPlanPeriod(Criteria):
    """Payer plan period criteria."""

    first: Optional[bool] = Field(None, alias="First")
    period_start_date: Optional[DateRange] = Field(None, alias="PeriodStartDate")
    period_end_date: Optional[DateRange] = Field(None, alias="PeriodEndDate")
    user_defined_period: Optional[Period] = Field(None, alias="UserDefinedPeriod")
    period_length: Optional[NumericRange] = Field(None, alias="PeriodLength")
    age_at_start: Optional[NumericRange] = Field(None, alias="AgeAtStart")
    age_at_end: Optional[NumericRange] = Field(None, alias="AgeAtEnd")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    payer_concept: Optional[int] = Field(None, alias="PayerConcept")
    plan_concept: Optional[int] = Field(None, alias="PlanConcept")
    sponsor_concept: Optional[int] = Field(None, alias="SponsorConcept")
    stop_reason_concept: Optional[int] = Field(None, alias="StopReasonConcept")
    payer_source_concept: Optional[int] = Field(None, alias="PayerSourceConcept")
    plan_source_concept: Optional[int] = Field(None, alias="PlanSourceConcept")
    sponsor_source_concept: Optional[int] = Field(None, alias="SponsorSourceConcept")
    stop_reason_source_concept: Optional[int] = Field(
        None, alias="StopReasonSourceConcept"
    )


class ObservationPeriod(Criteria):
    """Observation period criteria."""

    first: Optional[bool] = Field(None, alias="First")
    period_start_date: Optional[DateRange] = Field(None, alias="PeriodStartDate")
    period_end_date: Optional[DateRange] = Field(None, alias="PeriodEndDate")
    user_defined_period: Optional[Period] = Field(None, alias="UserDefinedPeriod")
    period_type: Optional[List[Concept]] = Field(None, alias="PeriodType")
    period_type_cs: Optional[ConceptSetSelection] = Field(None, alias="PeriodTypeCS")
    period_length: Optional[NumericRange] = Field(None, alias="PeriodLength")
    age_at_start: Optional[NumericRange] = Field(None, alias="AgeAtStart")
    age_at_end: Optional[NumericRange] = Field(None, alias="AgeAtEnd")


class ConditionEra(Criteria):
    """Condition era criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    era_start_date: Optional[DateRange] = Field(None, alias="EraStartDate")
    era_end_date: Optional[DateRange] = Field(None, alias="EraEndDate")
    occurrence_count: Optional[NumericRange] = Field(None, alias="OccurrenceCount")
    era_length: Optional[NumericRange] = Field(None, alias="EraLength")
    age_at_start: Optional[NumericRange] = Field(None, alias="AgeAtStart")
    age_at_end: Optional[NumericRange] = Field(None, alias="AgeAtEnd")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")


class DrugEra(Criteria):
    """Drug era criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    era_start_date: Optional[DateRange] = Field(None, alias="EraStartDate")
    era_end_date: Optional[DateRange] = Field(None, alias="EraEndDate")
    occurrence_count: Optional[NumericRange] = Field(None, alias="OccurrenceCount")
    gap_days: Optional[NumericRange] = Field(None, alias="GapDays")
    era_length: Optional[NumericRange] = Field(None, alias="EraLength")
    age_at_start: Optional[NumericRange] = Field(None, alias="AgeAtStart")
    age_at_end: Optional[NumericRange] = Field(None, alias="AgeAtEnd")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")


class DoseEra(Criteria):
    """Dose era criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")
    first: Optional[bool] = Field(None, alias="First")
    era_start_date: Optional[DateRange] = Field(None, alias="EraStartDate")
    era_end_date: Optional[DateRange] = Field(None, alias="EraEndDate")
    unit: Optional[List[Concept]] = Field(None, alias="Unit")
    unit_cs: Optional[ConceptSetSelection] = Field(None, alias="UnitCS")
    dose_value: Optional[NumericRange] = Field(None, alias="DoseValue")
    era_length: Optional[NumericRange] = Field(None, alias="EraLength")
    age_at_start: Optional[NumericRange] = Field(None, alias="AgeAtStart")
    age_at_end: Optional[NumericRange] = Field(None, alias="AgeAtEnd")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")


class LocationRegion(GeoCriteria):
    """Location region criteria."""

    codeset_id: Optional[int] = Field(None, alias="CodesetId")


class DemographicCriteria(BaseModel):
    """Demographic criteria for filtering."""

    age: Optional[NumericRange] = Field(None, alias="Age")
    gender: Optional[List[Concept]] = Field(None, alias="Gender")
    gender_cs: Optional[ConceptSetSelection] = Field(None, alias="GenderCS")
    race: Optional[List[Concept]] = Field(None, alias="Race")
    race_cs: Optional[ConceptSetSelection] = Field(None, alias="RaceCS")
    ethnicity: Optional[List[Concept]] = Field(None, alias="Ethnicity")
    ethnicity_cs: Optional[ConceptSetSelection] = Field(None, alias="EthnicityCS")
    occurrence_start_date: Optional[DateRange] = Field(
        None, alias="OccurrenceStartDate"
    )
    occurrence_end_date: Optional[DateRange] = Field(None, alias="OccurrenceEndDate")


class WindowEndpoint(BaseModel):
    """Window endpoint configuration."""

    days: Optional[int] = Field(None, alias="Days")
    coeff: int = Field(alias="Coeff")


class Window(BaseModel):
    """Time window configuration."""

    start: Optional[WindowEndpoint] = Field(None, alias="Start")
    end: Optional[WindowEndpoint] = Field(None, alias="End")
    use_index_end: Optional[bool] = Field(None, alias="UseIndexEnd")
    use_event_end: Optional[bool] = Field(None, alias="UseEventEnd")


class Occurrence(BaseModel):
    """Occurrence configuration."""

    EXACTLY: ClassVar[int] = 0
    AT_MOST: ClassVar[int] = 1
    AT_LEAST: ClassVar[int] = 2

    type: int = Field(alias="Type")
    count: int = Field(alias="Count")
    is_distinct: bool = Field(False, alias="IsDistinct")
    count_column: Optional[str] = Field(None, alias="CountColumn")


class CorelatedCriteria(BaseModel):
    """Correlated criteria with occurrence rules."""

    criteria: Optional[Criteria] = Field(None, alias="Criteria")
    start_window: Optional[Window] = Field(None, alias="StartWindow")
    end_window: Optional[Window] = Field(None, alias="EndWindow")
    occurrence: Optional[Occurrence] = Field(None, alias="Occurrence")
    restrict_visit: bool = Field(False, alias="RestrictVisit")
    ignore_observation_period: bool = Field(False, alias="IgnoreObservationPeriod")


class WindowedCriteria(BaseModel):
    """Windowed criteria base class."""

    criteria: Optional[Criteria] = Field(None, alias="Criteria")
    start_window: Optional[Window] = Field(None, alias="StartWindow")
    end_window: Optional[Window] = Field(None, alias="EndWindow")
    restrict_visit: bool = Field(False, alias="RestrictVisit")
    ignore_observation_period: bool = Field(False, alias="IgnoreObservationPeriod")


class DateOffsetStrategy(BaseModel):
    """Date offset strategy for end events."""

    class DateField(BaseModel):
        START_DATE: ClassVar[str] = "StartDate"
        END_DATE: ClassVar[str] = "EndDate"

    date_field: str = Field("StartDate", alias="DateField")
    offset: int = Field(0, alias="Offset")


class CustomEraStrategy(BaseModel):
    """Custom era strategy for end events."""

    drug_codeset_id: Optional[int] = Field(None, alias="DrugCodesetId")
    gap_days: int = Field(0, alias="GapDays")
    offset: int = Field(0, alias="Offset")
    days_supply_override: Optional[int] = Field(None, alias="DaysSupplyOverride")


class EndStrategy(BaseModel):
    """Base class for end strategies."""

    pass


class CriteriaGroup(BaseModel):
    """Logical grouping of criteria."""

    type: Optional[str] = Field(None, alias="Type")
    count: Optional[int] = Field(None, alias="Count")
    criteria_list: List[CorelatedCriteria] = Field(
        default_factory=list, alias="CriteriaList"
    )
    demographic_criteria_list: List[DemographicCriteria] = Field(
        default_factory=list, alias="DemographicCriteriaList"
    )
    groups: List["CriteriaGroup"] = Field(default_factory=list, alias="Groups")

    @property
    def is_empty(self) -> bool:
        """Check if the criteria group is empty."""
        return not (self.criteria_list or self.demographic_criteria_list or self.groups)


# Update forward references
Criteria.model_rebuild()
CriteriaGroup.model_rebuild()
