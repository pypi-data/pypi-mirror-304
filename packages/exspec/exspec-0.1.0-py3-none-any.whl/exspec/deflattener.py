"""
Deflattener Module
------------------

This module provides utility functions to "deflatten" metadata that has been
flattened (e.g., by the ExSpec package). It handles the conversion of certain
special keys back into their corresponding complex data types, such as lists,
type-unit values, and dimension formulas, ensuring the complete recovery of the
original structure.

Functions:
----------
- `deflatten_dict(d: dict, name: str) -> ExSpec`: Converts a flattened dictionary back into
  an atomic ExSpec object.
"""

import json

from src.exspec.models import ExSpec
from src.exspec.operations import merge_two_dicts
from src.exspec.utils import TypeUnitValue, ListValue, DimensionFormula


def deflatten_dict(d: dict, name: str) -> ExSpec:
    """
    De-flattens a dictionary, reconstructing complex data types such as ListValue,
    TypeUnitValue, and DimensionFormula from a flattened form. This is particularly
    useful for converting metadata back into its original format after being stored
    in a flattened structure.

    Parameters:
    -----------
    - d (dict): The flattened dictionary to deflatten. Keys with specific patterns
      will be converted back into their original data types.
    - name (str): Name of the resulting atomic ExSpec.

    Returns:
    --------
    - ExSpec: The resulting atomic ExSpec, with all flattened structures restored
      to their original form.
    """

    def _deserialize_dimension_formula(dimension_formula_json):
        """
        Converts a serialized dictionary back into a DimensionFormula object.

        Parameters:
        -----------
        - dimension_formula_json (dict): A dictionary representing a serialized
          DimensionFormula.

        Returns:
        --------
        - DimensionFormula: The deserialized DimensionFormula object.
        """
        dims = dimension_formula_json
        items = []
        for dim, exp in dims.items():
            if exp != 0:
                items.append(dim)
                items.append(exp)
        return DimensionFormula(items)

    def _deserialize_value(value):
        """
        Deserializes a value, handling both atomic values and complex nested
        structures (lists, dictionaries).

        Parameters:
        -----------
        - value: The value to deserialize, which may be a string, JSON object,
          or serialized structure.

        Returns:
        --------
        - The deserialized value, either as an atomic value or a complex structure.
        """
        try:
            # Attempt to parse value as JSON
            loaded_value = json.loads(value)

            # Recursively deserialize lists and dictionaries
            if isinstance(loaded_value, list):
                return [_deserialize_value(item) for item in loaded_value]
            elif isinstance(loaded_value, dict):
                # Handle DimensionFormula deserialization
                if "__DimensionFormula__" in loaded_value:
                    return _deserialize_dimension_formula(loaded_value["__DimensionFormula__"])
                # Recursively deserialize nested dictionaries
                return {k: _deserialize_value(v) for k, v in loaded_value.items()}
            elif value in ('str', 'int', 'float'):
                type_map = {
                    "int": int,
                    "float": float,
                    "str": str
                }
                return type_map.get(value)
            else:
                return loaded_value  # Base case: Return atomic values
        except (TypeError, ValueError):
            # Return the original value if it cannot be parsed as JSON
            return value

    def _deflatten(sub_d):
        """
        A helper function to deflatten a dictionary by reconstructing complex
        types such as TypeUnitValue and ListValue.

        Parameters:
        -----------
        - sub_d (dict): The dictionary to deflatten.

        Returns:
        --------
        - dict: The deflattened dictionary.
        """
        deflattened_dict = {}
        for k, v in list(sub_d.items()):
            if k in sub_d.keys():
                if '._TypeUnitValue.' in k:
                    # Convert back to TypeUnitValue
                    base_key = k.rsplit('._TypeUnitValue._value', 1)[0]
                    if sub_d.get(f"{base_key}._TypeUnitValue._value._ListValue"):
                        value = ListValue(items=json.loads(sub_d.pop(f"{base_key}._TypeUnitValue._value._ListValue")))
                    else:
                        value = sub_d.pop(f"{base_key}._TypeUnitValue._value")
                    unit = sub_d.pop(f"{base_key}._TypeUnitValue._unit", None)
                    prefix = sub_d.pop(f"{base_key}._TypeUnitValue._prefix", None)
                    prop_type = None
                    if sub_d.get(f"{base_key}._TypeUnitValue._type._DimensionFormula"):
                        prop_type = _deserialize_dimension_formula(
                            sub_d.pop(f"{base_key}._TypeUnitValue._type._DimensionFormula"))
                    elif sub_d.get(f"{base_key}._TypeUnitValue._type"):
                        prop_type = _deserialize_value(sub_d.pop(f"{base_key}._TypeUnitValue._type"))
                    deflattened_dict = merge_two_dicts(deflattened_dict,
                                                       {base_key: TypeUnitValue(value, prefix, unit, prop_type)})
                elif '._ListValue' in k:
                    # Convert back to ListValue
                    original_key = k.replace('._ListValue', '')
                    deflattened_dict = merge_two_dicts(deflattened_dict,
                                                       {original_key: ListValue(items=_deserialize_value(v))})
                    sub_d.pop(k)
                else:
                    deflattened_dict = merge_two_dicts(deflattened_dict, {k: v})
                    sub_d.pop(k)

        return deflattened_dict

    return ExSpec(name, [_deflatten(d)])
