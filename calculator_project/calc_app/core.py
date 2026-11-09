"""Arithmetic independent of argument parsing and terminal output."""

from decimal import Decimal, DecimalException, localcontext
import re


class CalculationError(ValueError):
    """An input or operation cannot produce a supported numeric result."""


OPERATIONS = ("add", "subtract", "multiply", "divide")
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")


def parse_number(text: str) -> Decimal:
    """Accept bounded, finite decimal literals with at most 200 characters."""
    if not isinstance(text, str) or len(text) > 200 or not NUMBER.fullmatch(text):
        raise CalculationError("Enter a valid decimal number (up to 200 characters).")
    try:
        number = Decimal(text)
        if (not number.is_finite() or number.copy_abs() > Decimal("1e100")
                or (number != 0 and number.copy_abs() < Decimal("1e-100"))):
            raise CalculationError("Nonzero numbers must have magnitude between 1e-100 and 1e100.")
        return number
    except DecimalException as exc:
        raise CalculationError("Enter a valid decimal number.") from exc


def format_number(value: Decimal) -> str:
    """Render fixed-point output without insignificant zeros or negative zero."""
    if value == 0:
        return "0"
    output = format(value, "f")
    return output.rstrip("0").rstrip(".") if "." in output else output


def calculate(operation: str, left: str, right: str) -> str:
    """Return arithmetic rounded to 28 significant decimal digits, half-even."""
    if operation not in OPERATIONS:
        raise CalculationError(f"Unsupported operation: {operation}")
    # Explicit precision prevents callers' decimal contexts changing app results.
    with localcontext() as context:
        context.prec = 28
        context.rounding = "ROUND_HALF_EVEN"
        a, b = parse_number(left), parse_number(right)
        if operation == "divide" and b == 0:
            raise CalculationError("Cannot divide by zero.")
        try:
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            else:
                result = a / b
            if not result.is_finite():
                raise CalculationError("The result must be finite.")
            return format_number(result)
        except DecimalException as exc:
            raise CalculationError("The calculation is outside supported numeric limits.") from exc
