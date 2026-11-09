"""A small decimal calculator with a stable command-line interface."""

from .core import CalculationError, calculate

__version__ = "1.0.0"
__all__ = ["CalculationError", "calculate"]
