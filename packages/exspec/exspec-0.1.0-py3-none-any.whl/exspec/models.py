"""
Data Models Module
------------------

This module defines the core data structures for representing experiment specifications (exspecs).
It includes the `ExSpec` class, which supports:
- Storing dictionaries of properties and their values.
- Resolving and comparing exspecs.
- Handling atomic and specialized exspecs.
- Supporting operations like subset checks, flattening, and pretty-printing.

The module also manages the comparison of units, multi-values, and complex data types, ensuring that
exspecs can be flattened into a combinatorial set of atomic dictionaries when needed.

Key Classes:
------------
- `ExSpec`: Represents an experiment specification, capable of resolving itself into atomic dictionaries.
"""
import json
from functools import total_ordering

from src.exspec.utils import compare_units, MultiValue, TypeUnitValue, is_atomic_dictionary, DimensionFormula, ListValue


@total_ordering
class ExSpec:
    """
    Represents an experiment specification (exspec).

    An ExSpec stores one or more dictionaries representing the structure of an experiment,
    along with operations for resolving, flattening, and comparing these structures.
    Each exspec can hold references to nested dictionaries and supports combinatorial
    expansion of multi-values.

    Attributes:
    -----------
    - name (str): The name of the exspec.
    - dictionaries (list): A list of dictionaries that form the exspec.
    """

    def __init__(self, name: str, dictionaries: list):
        """
        Initializes an ExSpec with a name and dictionaries.

        Parameters:
        -----------
        - name (str): The name of the exspec.
        - dictionaries (list): The list of dictionaries representing the exspec.
          If a single dictionary is passed, it is wrapped in a list.
        """
        self.name = name
        self.dictionaries = dictionaries if isinstance(dictionaries, list) else [dictionaries]

    def __lt__(self, other: 'ExSpec') -> bool:
        """
        Compares the current ExSpec to another based on their names.

        Parameters:
        -----------
        - other (ExSpec): Another ExSpec to compare.

        Returns:
        --------
        - bool: True if the current ExSpec's name is lexicographically less than the other.
        """
        if not isinstance(other, ExSpec):
            return NotImplemented
        return self.name < other.name

    def __eq__(self, other: 'ExSpec') -> bool:
        """
        Checks if two ExSpec objects are equal by resolving their dictionaries and
        comparing them.

        Parameters:
        -----------
        - other (ExSpec): The ExSpec to compare against.

        Returns:
        --------
        - bool: True if both ExSpecs have the same resolved dictionaries, False otherwise.
        """
        if not isinstance(other, ExSpec):
            return NotImplemented
        self.resolve()
        other.resolve()
        return self._are_equal_resolved_exspecs(self.dictionaries, other.dictionaries)

    def _are_equal_resolved_exspecs(self, list_a: list, list_b: list) -> bool:
        """
        Compares two lists of resolved dictionaries for equality.

        Parameters:
        -----------
        - list_a (list): The first list of resolved dictionaries.
        - list_b (list): The second list of resolved dictionaries.

        Returns:
        --------
        - bool: True if both lists contain equal dictionaries, False otherwise.
        """
        if len(list_a) != len(list_b):
            return False
        return all(any(self._are_equal_dicts(d1, d2) for d2 in list_b) for d1 in list_a)

    def _are_equal_dicts(self, a: dict, b: dict) -> bool:
        """
        Recursively compares two dictionaries, considering unit equality.

        Parameters:
        -----------
        - a (dict): The first dictionary to compare.
        - b (dict): The second dictionary to compare.

        Returns:
        --------
        - bool: True if both dictionaries are equal, False otherwise.
        """
        if isinstance(a, dict) and isinstance(b, dict):
            if set(a.keys()) != set(b.keys()):
                return False
            return all(self._are_equal_dicts(a[k], b[k]) for k in a)
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                return False
            return all(self._are_equal_dicts(x, y) for x, y in zip(a, b))
        else:
            return a == b or compare_units(a, b)

    def is_resolved(self) -> bool:
        """
        Checks whether the ExSpec is fully resolved into atomic dictionaries.

        An ExSpec is considered resolved if all its dictionaries are atomic.

        Returns:
        --------
        - bool: True if the ExSpec is fully resolved, False otherwise.
        """
        return all(is_atomic_dictionary(d) for d in self.dictionaries)

    def resolve(self) -> None:
        """
        Resolves the ExSpec by expanding all MultiValues into their possible
        combinations, producing atomic dictionaries.
        """
        resolved_dicts = []
        for d in self.dictionaries:
            resolved_dicts.extend(self._resolve_combinations(d))
        self.dictionaries = resolved_dicts

    def _resolve_combinations(self, d: dict) -> list:
        """
        Recursively resolves combinations of MultiValues within a dictionary.

        Parameters:
        -----------
        - d (dict): The dictionary to resolve.

        Returns:
        --------
        - list: A list of atomic dictionaries representing all possible combinations.
        """
        # First, resolve any MultiValues at the current dictionary level.
        possible_values = {}
        for k, v in d.items():
            if isinstance(v, dict):
                # Recursively resolve nested dictionaries
                possible_values[k] = self._resolve_combinations(v)
            elif isinstance(v, MultiValue):
                # Expand MultiValues into their possible atomic choices
                possible_values[k] = v.resolve()
            elif isinstance(v, TypeUnitValue):
                possible_values[k] = v.resolve()
            else:
                # For atomic values, just wrap them in a list to allow combinations later
                possible_values[k] = [v]

        # Now generate all combinations across all the keys
        from itertools import product
        keys = list(possible_values.keys())
        value_combinations = list(product(*possible_values.values()))

        # Build the result as a list of fully resolved dictionaries
        resolved_combinations = []
        for combination in value_combinations:
            # Combine the current set of resolved values into a dictionary
            combination_dict = {key: value for key, value in zip(keys, combination)}
            resolved_combinations.append(combination_dict)

        return resolved_combinations

    def is_atomic(self) -> bool:
        """
        Checks if the ExSpec is atomic, meaning it resolves to a single dictionary
        without any MultiValues (e.g., ranges or sets).

        Returns:
        --------
        - bool: True if the ExSpec is atomic, False otherwise.
        """
        return len(self.dictionaries) == 1 and is_atomic_dictionary(self.dictionaries[0])

    def is_specialization_of(self, other: 'ExSpec') -> tuple[bool, dict]:
        """
        Determines whether the current ExSpec is a specialization of another ExSpec.

        A specialization is a more specific version of another ExSpec, meaning all
        of the current ExSpec's dictionaries are specializations of the other ExSpec's
        dictionaries.

        Parameters:
        -----------
        - other (ExSpec): The ExSpec to compare against.

        Returns:
        --------
        - tuple: A boolean indicating whether the current ExSpec is a specialization of the other,
                 and a dictionary mapping the specialized dictionaries.
        """
        from collections import defaultdict
        specialization_map = defaultdict(list)

        other_list = list(range(len(other.dictionaries)))
        # Step 1: For each dictionary in self, find a specialization in other.
        for idx_a, dict_a in enumerate(self.dictionaries):
            found_specialization = False
            for idx_b, dict_b in enumerate(other.dictionaries):
                if self._is_specialization(dict_a, dict_b):
                    specialization_map[idx_a].append(idx_b)
                    found_specialization = True
                    if idx_b in other_list:
                        other_list.pop(idx_b)
            if not found_specialization:
                return False, {}  # No specialization found for one of self's dictionaries
        if other_list:
            return False, {}

        return True, specialization_map

    def _is_specialization(self, specific: dict, general: dict) -> bool:
        """
        Recursively checks if a specific dictionary is a specialization of a general one.

        Parameters:
        -----------
        - specific (dict): The more specific dictionary.
        - general (dict): The more general dictionary.

        Returns:
        --------
        - bool: True if specific is a specialization of general, False otherwise.
        """
        if isinstance(specific, dict) and isinstance(general, dict):
            for key in general:  # Check that every key in general exists in specific and is more specific.
                if key not in specific:
                    return False
                if not self._is_specialization(specific[key], general[key]):
                    return False
            return True
        else:
            # Direct comparison or using unit comparison
            return specific == general or compare_units(specific, general)

    def is_subset_of(self, other: 'ExSpec') -> bool:
        """
        Checks if the current ExSpec is a subset of another ExSpec.

        A subset means that all dictionaries of the current ExSpec are contained
        in the dictionaries of the other ExSpec.

        Parameters:
        -----------
        - other (ExSpec): The ExSpec to compare against.

        Returns:
        --------
        - bool: True if the current ExSpec is a subset of the other, False otherwise.
        """
        self.resolve()
        other.resolve()

        # Check if every dictionary in self.dictionaries has a match in other.dictionaries
        for self_dict in self.dictionaries:
            if not any(self._are_equal_dicts(self_dict, other_dict) for other_dict in other.dictionaries):
                return False  # If no match is found for any self_dict, return False
        return True

    def pretty_print(self) -> str:
        """
        Pretty-prints the ExSpec in a human-readable format, with sorted propositions.

        Returns:
        --------
        - str: A formatted string representation of the ExSpec.
        """
        result = [f"{self.name} ="]

        for d in self.dictionaries:
            result.append(self._print_dict(d, indent=1))

        # Return the result as a joined string which is an ALTERNATE formula
        return result[0] + " ALTERNATE".join(result[1:])

    def _print_dict(self, d: dict, indent: int) -> str:
        """
        Recursively prints a dictionary with proper indentation for pretty-printing.

        Parameters:
        -----------
        - d (dict): The dictionary to print.
        - indent (int): The current level of indentation.

        Returns:
        --------
        - str: The formatted string representation of the dictionary.
        """
        result = []
        indent_str = '  ' * indent

        if isinstance(d, dict):
            result.append(" {")
            for k in sorted(d.keys()):
                if isinstance(d[k], TypeUnitValue):
                    result.append(indent_str + f"{k} " + self._print_dict(d[k], indent + 1))
                else:
                    result.append(indent_str + f"{k} = " + self._print_dict(d[k], indent + 1))
            if indent == 1:
                result.append('  ' * (indent-1) + "}") # No ; at the end of a top-level dictionary
            else:
                result.append('  ' * (indent - 1) + "}"+';')
        else:
            result.append(f"{d}" + ' ;')

        # Return the accumulated result as a joined string
        return "\n".join(result)

    def flatten(self) -> dict:
        """
        Flattens the ExSpec dictionary only if it is atomic. This function was developed to be used in tandem with tools
        like InfluxDB where a flattened atomic exspec can be used to store trace metadata.

        Returns:
        --------
        - dict: A flattened dictionary.

        Raises:
        -------
        - ValueError: If the ExSpec is not atomic.
        """
        if not self.is_atomic():
            raise ValueError("Flattening is only supported for atomic exspecs.")
        self.resolve()
        return self._flatten(dict(self.dictionaries[0]))

    @staticmethod
    def _serialize_value(value) -> str:
        """
        Serializes a value into a format suitable for flattening.

        Parameters:
        -----------
        - value: The value to serialize.

        Returns:
        --------
        - str: The serialized value (as a string, JSON, etc.).
        """
        if isinstance(value, list):
            # Serialize lists as JSON arrays
            return json.dumps(value)
        elif isinstance(value, dict) and 'list' in value.keys():
            # Serialize list type which could be nested with str or DimensionFormula type.
            return json.dumps({k: ExSpec._serialize_value(v) for k, v in value.items()})
        elif isinstance(value, DimensionFormula):
            # Serialize DimensionFormula as a JSON object
            return json.dumps({"__DimensionFormula__": {k: v for k, v in vars(value).items() if v is not None}})
        elif isinstance(value, type):
            return str(value.__name__)
        else:
            return value

    @staticmethod
    def _flatten(sub_d: dict, parent_key: str = '') -> dict:
        """
        Recursively flattens a dictionary into a single-level dictionary.

        Parameters:
        -----------
        - sub_d (dict): The dictionary to flatten.
        - parent_key (str): The base key for nested keys in the flattened structure.

        Returns:
        --------
        - dict: The flattened dictionary.
        """
        flattened = {}
        for k, v in sub_d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k

            if isinstance(v, dict):
                # Recurse for nested dictionaries
                flattened.update(ExSpec._flatten(v, new_key))
            elif isinstance(v, TypeUnitValue):
                # Flatten TypeUnitValue with the required key pattern
                if isinstance(v.value, ListValue):
                    # Serialize ListValue as JSON and mark with '_ListValue'
                    flattened[f"{new_key}._TypeUnitValue._value._ListValue"] = ExSpec._serialize_value(v.value.items)
                else:
                    flattened[f"{new_key}._TypeUnitValue._value"] = v.value
                if v.unit:
                    flattened[f"{new_key}._TypeUnitValue._unit"] = v.unit
                if v.prefix:
                    flattened[f"{new_key}._TypeUnitValue._prefix"] = v.prefix
                if v.prop_type:
                    flattened[f"{new_key}._TypeUnitValue._type"] = ExSpec._serialize_value(v.prop_type)

            elif isinstance(v, ListValue):
                # Serialize ListValue as JSON and mark with '_ListValue'
                flattened[f"{new_key}._ListValue"] = ExSpec._serialize_value(v.items)
            else:
                # For atomic values, just store them as-is
                flattened[new_key] = v
        return flattened

    def __str__(self) -> str:
        """
        Returns a string representation of the ExSpec.

        Returns:
        --------
        - str: The name of the ExSpec.
        """
        return f"ExSpec({self.name})"
