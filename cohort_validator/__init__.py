"""
Cohort Validator - Python Interface to OHDSI CIRCE Cohort Validation

This package provides a Python interface to the OHDSI CIRCE (Cohort Inclusion Rule and
Cohort Expression) library for validating cohort definitions.

The main functionality is provided through the CohortValidator class, which allows
you to validate cohort expressions and receive detailed warnings and errors.
"""

from .cohort_validator import CohortValidator

__version__ = "1.0.0"
__author__ = "EPAM Systems"
__email__ = "cohort-validator@epam.com"

__all__ = ["CohortValidator"]
