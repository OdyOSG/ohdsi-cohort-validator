"""
Concept and concept set related Pydantic models.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class Concept(BaseModel):
    """Vocabulary concept with metadata."""

    concept_id: Optional[int] = Field(
        None, alias="CONCEPT_ID", description="Unique concept identifier"
    )
    concept_name: Optional[str] = Field(
        None, alias="CONCEPT_NAME", description="Human readable concept name"
    )
    standard_concept: Optional[str] = Field(
        None, alias="STANDARD_CONCEPT", description="Standard concept flag (S, C, N)"
    )
    invalid_reason: Optional[str] = Field(
        None, alias="INVALID_REASON", description="Invalid reason (V, D, U)"
    )
    concept_code: Optional[str] = Field(
        None, alias="CONCEPT_CODE", description="Concept code in source vocabulary"
    )
    domain_id: Optional[str] = Field(
        None, alias="DOMAIN_ID", description="Domain identifier"
    )
    vocabulary_id: Optional[str] = Field(
        None, alias="VOCABULARY_ID", description="Source vocabulary identifier"
    )
    concept_class_id: Optional[str] = Field(
        None, alias="CONCEPT_CLASS_ID", description="Concept class identifier"
    )

    @property
    def standard_concept_caption(self) -> str:
        """Get human readable standard concept caption."""
        if self.standard_concept is None:
            return "Unknown"

        mapping = {"N": "Non-Standard", "S": "Standard", "C": "Classification"}
        return mapping.get(self.standard_concept, "Unknown")

    @property
    def invalid_reason_caption(self) -> str:
        """Get human readable invalid reason caption."""
        if self.invalid_reason is None:
            return "Unknown"

        mapping = {"V": "Valid", "D": "Invalid", "U": "Invalid"}
        return mapping.get(self.invalid_reason, "Unknown")


class ConceptSetItem(BaseModel):
    """Individual concept within a concept set."""

    concept: Optional[Concept] = Field(None, description="The concept")
    is_excluded: bool = Field(False, description="Whether this concept is excluded")
    include_descendants: bool = Field(
        False, description="Whether to include descendant concepts"
    )
    include_mapped: bool = Field(
        False, description="Whether to include mapped concepts"
    )


class ConceptSetExpression(BaseModel):
    """Collection of concepts with inclusion/exclusion rules."""

    items: List[ConceptSetItem] = Field(
        default_factory=list, description="List of concept set items"
    )


class ConceptSet(BaseModel):
    """Named collection of concepts."""

    id: int = Field(description="Unique identifier for the concept set")
    name: str = Field(description="Human readable name for the concept set")
    expression: Optional[ConceptSetExpression] = Field(
        None, description="Concept set expression"
    )


class ConceptSetSelection(BaseModel):
    """Reference to a concept set with optional exclusion flag."""

    codeset_id: Optional[int] = Field(
        None, alias="CodesetId", description="ID of the referenced concept set"
    )
    is_exclusion: bool = Field(
        False, alias="IsExclusion", description="Whether this is an exclusion"
    )

