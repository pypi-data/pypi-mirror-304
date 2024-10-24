"""
Utility Functions Module
------------------------

This module provides utility functions for handling units, prefixes, and comparisons
of physical quantities. It includes classes for handling multi-values, range values,
and unit-based comparisons for experiment specifications.
"""
from collections import Counter

from lark import Token

# Unit prefixes for conversion to base units
unit_prefixes = {
    'nano': ['n-', 1e-9],
    'micro': ['u-', 1e-6],
    'milli': ['m-', 1e-3],
    'kilo': ['k-', 1e3],
    'mega': ['M-', 1e6],
    'giga': ['G-', 1e9],
    'tera': ['T-', 1e12],
}

# Dimensions for physical quantities
dimensions = {
    'mass': 'M' ,
    'length': 'L',
    'time': 'T',
    'current': 'I',
    'temperature': 'K',
    'substance': 'N',
    'luminosity': 'J'
}

def compare_units(value1: 'TypeUnitValue', value2: 'TypeUnitValue') -> bool:
    """
    Compares two values with units, considering unit prefixes and dimensions.

    Parameters:
    -----------
    - value1 (TypeUnitValue): The first value with units.
    - value2 (TypeUnitValue): The second value with units.

    Returns:
    --------
    - bool: True if the two values are equivalent in base units and dimensions, False otherwise.
    """
    if isinstance(value1, TypeUnitValue) and isinstance(value2, TypeUnitValue):
        return (value1.value_in_base_units() == value2.value_in_base_units() and
                value1.unit == value2.unit and
                value1.prop_type == value2.prop_type)
    return False


def is_atomic_dictionary(d: any) -> bool:
    """
    Recursively checks if a dictionary or value is atomic (contains no MultiValues).

    Parameters:
    -----------
    - d: The dictionary or value to check.

    Returns:
    --------
    - bool: True if atomic, False otherwise.
    """
    if isinstance(d, dict):
        # Recursively checif self.mass > 1k if all values in the dictionary are atomic
        return all(is_atomic_dictionary(v) for v in d.values())
    elif isinstance(d, TypeUnitValue):
        return False if isinstance(d.value, MultiValue) else True
    elif isinstance(d, MultiValue):
        # If the value is a MultiValue, it is not atomic
        return False
    else:
        # Any other value is considered atomic
        return True


class TypeUnitValue:
    """
    Represents a value with an associated type, unit, and prefix.
    """

    def __init__(self, value: any, prefix: str = None, unit: str = None, prop_type: 'DimensionFormula' = None):
        self.value = value
        self.prefix = prefix
        self.unit = unit
        self.prop_type = prop_type  # Physical dimensions, if any

    def __eq__(self, other: 'TypeUnitValue') -> bool:
        if not isinstance(other, TypeUnitValue):
            return False
        return (self.value_in_base_units() == other.value_in_base_units() and
                self.unit == other.unit and
                self.prop_type == other.prop_type)

    def __str__(self) -> str:
        result_str = ''
        if self.prop_type:
            result_str += f": {str(self.prop_type)} "
        result_str += f"= {str(self.value)}"
        if self.prefix:
            result_str += f" {unit_prefixes[self.prefix][0]}{self.unit}"
        elif self.unit:
            result_str += f" {self.unit}"
        return result_str

    def value_in_base_units(self) -> any:
        """
        Converts the value to base units using the unit prefix.

        Returns:
        --------
        - The value in base units.
        """
        factor = 1
        for key, (prefix_symbol, value) in unit_prefixes.items():
            if prefix_symbol == self.prefix:
                factor = value
        if isinstance(self.value, MultiValue):
            return self.value.resolve() * factor
        if isinstance(self.value, ListValue):
            return list(self.value.items) * factor
        return self.value * factor

    def resolve(self) -> list:
        """
        Resolves the value into a list of TypeUnitValues.

        Returns:
        --------
        - list: A list of resolved TypeUnitValues.
        """
        if not isinstance(self.value, MultiValue):
            return [self]
        else:
            return [TypeUnitValue(value=resolved_value, prefix=self.prefix, unit=self.unit, prop_type=self.prop_type)
                    for resolved_value in self.value.resolve()]


class MultiValue:
    """
    Superclass for multi-values, which are values that represent multiple options for atomic experiment specifications.
    """

    def resolve(self) -> list:
        """
        Resolves the multi-value into a list of atomic values.

        Returns:
        --------
        - list: A list of atomic values.
        """
        raise NotImplementedError("Subclasses must implement resolve method")

    def __eq__(self, other: 'MultiValue') -> bool:
        if isinstance(other, MultiValue):
            return Counter(self.resolve()) == Counter(other.resolve())
        return False

    def contains(self, other: any) -> bool:
        """
        Checks if the current multi-value contains another value or multi-value.

        Parameters:
        -----------
        - other: The value or multi-value to check.

        Returns:
        --------
        - bool: True if the current multi-value contains the other value, False otherwise.
        """
        if isinstance(other, MultiValue):
            return all(x in self.resolve() for x in other.resolve())
        else:
            return other in self.resolve()

class SetValue(MultiValue):
    """
    Represents a set value that is interpreted as a composition of experiment specifications.
    """

    def __init__(self, items: list):
        self.items = items

    def resolve(self) -> list:
        """
        Resolves the set value into a list of items.

        Returns:
        --------
        - list: The list of items in the set.
        """
        return self.items

    def __str__(self) -> str:
        return "{" + "; ".join(str(item) for item in self.items) + "}"


class RangeValue(MultiValue):
    """
    Represents a range value with an associated start, stop and step, that is interpreted as a composition of experiment specifications.
    """

    def __init__(self, start: int, stop: int, step: int):
        self.start = start
        self.stop = stop
        self.step = step

    def resolve(self) -> list:
        """
        Resolves the range value into a list of integers.

        Returns:
        --------
        - list: The list of values in the range.
        """
        return list(range(self.start, self.stop, self.step))

    def __str__(self) -> str:
        return f"RANGE({self.start}, {self.stop}, {self.step})"


class ListValue:
    """
    Represents a list value that is interpreted as a single value for a single experiment specifications.
    """

    def __init__(self, items: list):
        self.items = items

    def __eq__(self, other: 'ListValue') -> bool:
        if not isinstance(other, ListValue):
            return False
        return Counter(self.items) == Counter(other.items)

    def __str__(self) -> str:
        return "[" + ", ".join(str(item) for item in self.items) + "]"


class DimensionFormula:
    """
    Represents a dimensional formula, which defines the physical dimensions (mass, length, time, etc.) of a quantity.
    """

    def __init__(self, items: list):
        dims = {}
        for item in items:
            if not isinstance(item, (Token, int)):
                token_index = items.index(item) + 1
                if len(items) > token_index and isinstance(items[token_index], (Token, int)):
                    dim = item
                    exp = int(items[token_index])
                else:
                    dim = item
                    exp = 1
                dims[dim] = exp
        self.mass = dims['mass'] if 'mass' in dims else 0
        self.length = dims['length'] if 'length' in dims else 0
        self.time = dims['time'] if 'time' in dims else 0
        self.current = dims['current'] if 'current' in dims else 0
        self.temperature = dims['temperature'] if 'temperature' in dims else 0
        self.substance = dims['substance'] if 'substance' in dims else 0
        self.luminosity = dims['luminosity'] if 'luminosity' in dims else 0

    def __eq__(self, other: 'DimensionFormula') -> bool:
        if not isinstance(other, DimensionFormula):
            return False
        return (
                self.mass == other.mass and self.length == other.length and self.time == other.time and self.current == other.current
                and self.temperature == other.temperature and self.substance == other.substance and self.luminosity == other.luminosity)

    def __str__(self) -> str:
        return_str = ''
        for k, v in vars(self).items():
            if v != 0:
                return_str += f"{dimensions.get(k)}" if v == 1 else f"{dimensions.get(k)}{str(int(v))}"
        return return_str
