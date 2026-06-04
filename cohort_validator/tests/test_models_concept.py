"""
Comprehensive unit tests for models/concept.py
"""

import pytest
from cohort_validator.models.concept import (
    Concept,
    ConceptSet,
    ConceptSetExpression,
    ConceptSetItem,
    ConceptSetSelection,
)


class TestConcept:
    """Tests for Concept model."""

    def test_concept_creation_full(self):
        """Test creating a Concept with all fields."""
        concept = Concept(
            concept_id=201820,
            concept_name="Diabetes mellitus",
            domain_id="Condition",
            vocabulary_id="SNOMED",
            concept_code="73211009",
            concept_class_id="Clinical Finding",
            standard_concept="S",
            invalid_reason="V",
        )
        assert concept.concept_id == 201820
        assert concept.concept_name == "Diabetes mellitus"
        assert concept.domain_id == "Condition"
        assert concept.vocabulary_id == "SNOMED"
        assert concept.concept_code == "73211009"
        assert concept.standard_concept == "S"
        assert concept.invalid_reason == "V"

    def test_concept_with_aliases(self):
        """Test Concept with alias fields."""
        concept = Concept(
            CONCEPT_ID=201820,
            CONCEPT_NAME="Diabetes mellitus",
            DOMAIN_ID="Condition",
            VOCABULARY_ID="SNOMED",
        )
        assert concept.concept_id == 201820
        assert concept.concept_name == "Diabetes mellitus"
        assert concept.domain_id == "Condition"
        assert concept.vocabulary_id == "SNOMED"

    def test_concept_minimal(self):
        """Test Concept with minimal fields."""
        concept = Concept(concept_id=201820)
        assert concept.concept_id == 201820
        assert concept.concept_name is None

    def test_standard_concept_caption(self):
        """Test standard_concept_caption property."""
        concept_s = Concept(standard_concept="S")
        assert concept_s.standard_concept_caption == "Standard"

        concept_n = Concept(standard_concept="N")
        assert concept_n.standard_concept_caption == "Non-Standard"

        concept_c = Concept(standard_concept="C")
        assert concept_c.standard_concept_caption == "Classification"

        concept_none = Concept(standard_concept=None)
        assert concept_none.standard_concept_caption == "Unknown"

        concept_invalid = Concept(standard_concept="X")
        assert concept_invalid.standard_concept_caption == "Unknown"

    def test_invalid_reason_caption(self):
        """Test invalid_reason_caption property."""
        concept_v = Concept(invalid_reason="V")
        assert concept_v.invalid_reason_caption == "Valid"

        concept_d = Concept(invalid_reason="D")
        assert concept_d.invalid_reason_caption == "Invalid"

        concept_u = Concept(invalid_reason="U")
        assert concept_u.invalid_reason_caption == "Invalid"

        concept_none = Concept(invalid_reason=None)
        assert concept_none.invalid_reason_caption == "Unknown"

        concept_invalid = Concept(invalid_reason="X")
        assert concept_invalid.invalid_reason_caption == "Unknown"


class TestConceptSetItem:
    """Tests for ConceptSetItem model."""

    def test_concept_set_item_creation(self):
        """Test creating a ConceptSetItem."""
        concept = Concept(concept_id=201820, concept_name="Diabetes")
        item = ConceptSetItem(
            concept=concept, is_excluded=False, include_descendants=True, include_mapped=False
        )
        assert item.concept == concept
        assert item.is_excluded is False
        assert item.include_descendants is True
        assert item.include_mapped is False

    def test_concept_set_item_defaults(self):
        """Test ConceptSetItem with default values."""
        item = ConceptSetItem()
        assert item.concept is None
        assert item.is_excluded is False
        assert item.include_descendants is False
        assert item.include_mapped is False

    def test_concept_set_item_from_dict(self):
        """Test ConceptSetItem can be created from dict."""
        item_data = {
            "concept": {
                "CONCEPT_ID": 201820,
                "CONCEPT_NAME": "Diabetes",
            },
            "includeDescendants": True,
        }
        item = ConceptSetItem(**item_data)
        assert item.concept is not None
        assert item.include_descendants is True

    def test_concept_set_item_atlas_aliases(self):
        """Test ConceptSetItem accepts Atlas JSON field names."""
        item = ConceptSetItem(
            concept={"CONCEPT_ID": 201820},
            isExcluded=True,
            includeDescendants=True,
            includeMapped=True,
        )

        assert item.is_excluded is True
        assert item.include_descendants is True
        assert item.include_mapped is True

    def test_concept_set_item_missing_flags_default_to_false(self):
        """Test concept set item flags are optional."""
        item = ConceptSetItem(concept={"CONCEPT_ID": 201820})

        assert item.is_excluded is False
        assert item.include_descendants is False
        assert item.include_mapped is False


class TestConceptSetExpression:
    """Tests for ConceptSetExpression model."""

    def test_concept_set_expression_empty(self):
        """Test ConceptSetExpression with empty items."""
        expression = ConceptSetExpression(items=[])
        assert expression.items == []

    def test_concept_set_expression_with_items(self):
        """Test ConceptSetExpression with items."""
        concept = Concept(concept_id=201820)
        item = ConceptSetItem(concept=concept)
        expression = ConceptSetExpression(items=[item])
        assert len(expression.items) == 1
        assert expression.items[0] == item

    def test_concept_set_expression_from_dict(self):
        """Test ConceptSetExpression from dictionary."""
        expression_data = {
            "items": [
                {
                    "concept": {
                        "CONCEPT_ID": 201820,
                        "CONCEPT_NAME": "Diabetes",
                    },
                    "includeDescendants": True,
                }
            ]
        }
        expression = ConceptSetExpression(**expression_data)
        assert len(expression.items) == 1


class TestConceptSet:
    """Tests for ConceptSet model."""

    def test_concept_set_creation(self):
        """Test creating a ConceptSet."""
        expression = ConceptSetExpression(items=[])
        concept_set = ConceptSet(id=0, name="Test Set", expression=expression)
        assert concept_set.id == 0
        assert concept_set.name == "Test Set"
        assert concept_set.expression == expression

    def test_concept_set_minimal(self):
        """Test ConceptSet with minimal fields."""
        concept_set = ConceptSet(id=0, name="Test Set")
        assert concept_set.id == 0
        assert concept_set.name == "Test Set"
        assert concept_set.expression is None

    def test_concept_set_from_dict(self):
        """Test ConceptSet from dictionary."""
        concept_set_data = {
            "id": 0,
            "name": "Diabetes Concepts",
            "expression": {
                "items": [
                    {
                        "concept": {
                            "CONCEPT_ID": 201820,
                            "CONCEPT_NAME": "Diabetes mellitus",
                        },
                        "includeDescendants": True,
                    }
                ]
            },
        }
        concept_set = ConceptSet(**concept_set_data)
        assert concept_set.id == 0
        assert concept_set.name == "Diabetes Concepts"
        assert concept_set.expression is not None
        assert len(concept_set.expression.items) == 1


class TestConceptSetSelection:
    """Tests for ConceptSetSelection model."""

    def test_concept_set_selection_creation(self):
        """Test creating a ConceptSetSelection."""
        selection = ConceptSetSelection(codeset_id=0, is_exclusion=False)
        assert selection.codeset_id == 0
        assert selection.is_exclusion is False

    def test_concept_set_selection_with_aliases(self):
        """Test ConceptSetSelection with alias fields."""
        selection = ConceptSetSelection(CodesetId=1, IsExclusion=True)
        assert selection.codeset_id == 1
        assert selection.is_exclusion is True

    def test_concept_set_selection_defaults(self):
        """Test ConceptSetSelection with default values."""
        selection = ConceptSetSelection(codeset_id=0)
        assert selection.codeset_id == 0
        assert selection.is_exclusion is False

    def test_concept_set_selection_exclusion(self):
        """Test ConceptSetSelection as exclusion."""
        selection = ConceptSetSelection(codeset_id=0, is_exclusion=True)
        assert selection.is_exclusion is True
