"""
Base Pydantic models for common data structures used in cohort definitions.
"""

from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class DateRange(BaseModel):
    """Date range filter with operator and optional extent."""

    value: Optional[str] = Field(None, description="Date value in YYYY-MM-DD format")
    op: Optional[str] = Field(
        None, alias="Op", description="Comparison operator (gt, lt, gte, lte, eq, bt)"
    )
    extent: Optional[str] = Field(None, description="Extent for between operations")


class NumericRange(BaseModel):
    """Numeric range filter with operator and optional extent."""

    value: Optional[Union[int, float]] = Field(None, description="Numeric value")
    op: Optional[str] = Field(
        None, alias="Op", description="Comparison operator (gt, lt, gte, lte, eq, bt)"
    )
    extent: Optional[Union[int, float]] = Field(
        None, description="Extent for between operations"
    )


class TextFilter(BaseModel):
    """Text filter with operator."""

    text: Optional[str] = Field(None, description="Text value to filter")
    op: Optional[str] = Field(
        None, description="Text operator (contains, startsWith, endsWith, eq)"
    )


class ResultLimit(BaseModel):
    """Result limiting configuration."""

    type: str = Field(default="First", description="Limit type (First, All)")


class Period(BaseModel):
    """Time period with start and end dates."""

    start_date: Optional[str] = Field(
        None, alias="StartDate", description="Start date in YYYY-MM-DD format"
    )
    end_date: Optional[str] = Field(
        None, alias="EndDate", description="End date in YYYY-MM-DD format"
    )


class CollapseType(str, Enum):
    """Collapse type enumeration."""

    ERA = "ERA"


class CollapseSettings(BaseModel):
    """Collapse settings for cohort definition."""

    collapse_type: CollapseType = Field(default=CollapseType.ERA, alias="CollapseType")
    era_pad: int = Field(default=0, alias="EraPad")


class DateAdjustment(BaseModel):
    """Date adjustment configuration."""

    # This will be expanded based on the actual Java implementation
    pass


class ObservationFilter(BaseModel):
    """Observation window filter."""

    prior_days: Optional[int] = Field(
        None, alias="PriorDays", description="Days prior to event"
    )
    post_days: Optional[int] = Field(
        None, alias="PostDays", description="Days post event"
    )
