"""Define user level functions."""
import collections.abc
import dataclasses
import enum
import typing

from .operations_module import add_numbers, multiply_numbers
from .utility_module import divide_numbers, subtract_numbers


@enum.unique
class ArithmeticOperator(enum.Enum):
    """Define supported arithmetic operators."""

    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"


@dataclasses.dataclass
class ArithmeticOperation:
    """Define arithmetic operation.

    Parameters
    ----------
    first_number : float
        value of first number
    operation : collections.abc.Callable[[float, float], float]
        type of arithmetic operation
    second_number : float
        value of second number
    """

    first_number: float
    operation: collections.abc.Callable[[float, float], float]
    second_number: float

    @property
    def result(self: "ArithmeticOperation") -> float:
        """Store result of arithmetic operation.

        Returns
        -------
        float
            result of arithmetic operation
        """
        return self.operation(self.first_number, self.second_number)


def validate_number_input(user_input: typing.Any) -> float:
    """Validate input is a number or attempt to convert.

    Parameters
    ----------
    user_input : typing.Any
        value of input

    Returns
    -------
    float
        number input

    Raises
    ------
    ValueError
        if input is not of number type
    """
    if isinstance(user_input, float):
        return user_input

    try:
        converted_user_input = float(user_input)
    except ValueError as error:
        raise ValueError("Supports only real numbers") from error

    return converted_user_input


def validate_operator_input(
    user_input: typing.Any,
) -> collections.abc.Callable[[float, float], float]:
    """Validate input is in {``+``, ``-``, ``*``, ``/``} and return corresponding operation.

    Parameters
    ----------
    user_input : typing.Any
        value of input

    Returns
    -------
    collections.abc.Callable[[float, float], float]
        operation function

    Raises
    ------
    ValueError
        if input is not a basic arithmetic operator
    """
    try:
        processed_user_input = ArithmeticOperator(user_input)
    except ValueError as error:
        raise ValueError("Supports only basic arithmetic") from error

    if processed_user_input == ArithmeticOperator.ADDITION:
        return add_numbers

    if processed_user_input == ArithmeticOperator.SUBTRACTION:
        return subtract_numbers

    if processed_user_input == ArithmeticOperator.MULTIPLICATION:
        return multiply_numbers

    if processed_user_input == ArithmeticOperator.DIVISION:
        return divide_numbers

    raise ValueError("Unexpected value of operation")  # pragma: no cover


def process_inputs(
    first_input: typing.Any, operator: typing.Any, second_input: typing.Any
) -> ArithmeticOperation:
    """Validate and convert user inputs.

    Parameters
    ----------
    first_input : typing.Any
        input for first number
    operator : typing.Any
        input for arithmetic operator
    second_input : typing.Any
        input for second number

    Returns
    -------
    ArithmeticOperation
        validated expression
    """
    first_number = validate_number_input(first_input)
    operator = validate_operator_input(operator)
    second_number = validate_number_input(second_input)

    return ArithmeticOperation(first_number, operator, second_number)


def calculate_results(
    first_input: typing.Any,
    operator: typing.Literal["+", "-", "*", "/"],
    second_input: typing.Any,
) -> float:
    """Perform basic arithmetic operations.

    Parameters
    ----------
    first_input : typing.Any
        value of first number
    operator : typing.Literal[ "+", "-", "*", "/" ]
        type of arithmetic operation
    second_input : typing.Any
        value of second number

    Returns
    -------
    float
        result of arithmetic operation

    Examples
    --------
    .. code-block:: pycon

        >>> from package_name_to_import_with import calculate_results
        >>> calculate_results(1, "+", 2)
        3.0
        >>> calculate_results(1, "-", 2)
        -1.0
        >>> calculate_results(1, "*", 2)
        2.0
        >>> calculate_results(1, "/", 2)
        0.5
    """
    arithmetic_expression = process_inputs(first_input, operator, second_input)

    return arithmetic_expression.result
