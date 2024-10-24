"""
Parser Module
-------------

Implements the parser and transformer for the exspec language using Lark.
Transforms the parse tree into the data structures defined in models.py.
Handles dictionary references by loading referenced exspecs from files and
detects recursive references to prevent infinite recursion.
"""

import os
from typing import Union

from lark import Lark, Transformer
from lark.exceptions import VisitError

from src.exspec.grammar import exspec_grammar
from src.exspec.models import ExSpec
from src.exspec.operations import merge, alternate
from src.exspec.utils import TypeUnitValue, SetValue, RangeValue, ListValue, DimensionFormula


def parse_exspec(input_data: str, base_dir: str = '.', is_file: bool = False) -> list:
    """
    Parses exspec input from either a text or a file and returns a list of ExSpec objects.

    Parameters:
    -----------
    - input_data (str): The exspec input text or filename.
    - base_dir (str): Base directory for resolving file paths of referenced exspecs.
    - is_file (bool): If True, treats input_data as a filename to read from.

    Returns:
    --------
    - list: List of ExSpec objects.
    """
    if is_file:
        with open(input_data, 'r') as f:
            input_text = f.read()
    else:
        input_text = input_data

    parser = Lark(exspec_grammar, parser="earley")
    parse_tree = parser.parse(input_text)

    # Manually apply the transformer to the parse tree
    transformer = ExSpecTransformer(base_dir=base_dir)
    try:
        exspecs = transformer.transform(parse_tree)
    except RecursionError as e:
        # Handle the recursion error here
        raise e

    return exspecs


class ExSpecTransformer(Transformer):
    """
    Transformer class to convert the parse tree into ExSpec data structures.
    Resolves dictionary references by loading referenced exspecs from files.
    Detects recursive references to prevent infinite recursion.
    """

    def __init__(self, base_dir: str = '.', loaded_exspecs: dict = None, loading_stack: list = None):
        """
        Initializes the transformer with a base directory for resolving file paths
        and dictionaries to track loaded exspecs and detect recursive references.

        Parameters:
        -----------
        - base_dir (str): Base directory for resolving file paths.
        - loaded_exspecs (dict): Dictionary of already loaded exspecs (default: {}).
        - loading_stack (list): Stack to track loading exspecs to detect recursion.
        """
        super().__init__()
        self.exspecs = {}
        self.base_dir = base_dir  # Base directory for resolving file paths
        self.loaded_exspecs = loaded_exspecs if loaded_exspecs is not None else {}
        self.loading_stack = loading_stack if loading_stack is not None else []

    @staticmethod
    def start(specs: list) -> list:
        """
        Returns the list of parsed specifications.

        Parameters:
        -----------
        - specs (list): List of ExSpec objects.

        Returns:
        --------
        - list: List of ExSpec objects.
        """
        return specs

    def specification(self, items: list) -> ExSpec:
        """
        Creates an ExSpec object from a specification.

        Parameters:
        -----------
        - items (list): List containing the ExSpec name and formula.

        Returns:
        --------
        - ExSpec: The resulting ExSpec object.
        """
        name, formula = items
        exspec = ExSpec(name, formula)
        self.exspecs[name] = exspec
        return exspec

    @staticmethod
    def EXSPEC_NAME(token) -> str:
        """
        Converts a token into an ExSpec name.

        Parameters:
        -----------
        - token: The token representing the ExSpec name.

        Returns:
        --------
        - str: The name of the ExSpec.
        """
        return str(token)

    @staticmethod
    def formula(items: list) -> list:
        """
        Processes a formula by applying operations like ALTERNATE or MERGE.

        Parameters:
        -----------
        - items (list): List of dictionaries and operations.

        Returns:
        --------
        - list: The result of applying the operations to the dictionaries.
        """
        result = items[0]
        i = 1
        while i < len(items):
            op = items[i]
            next_dict = items[i + 1]
            if op == 'ALTERNATE':
                result = alternate(result, next_dict)
            elif op == 'MERGE':
                result = merge(result, next_dict)
            i += 2
        return result

    @staticmethod
    def OPERATION(token) -> str:
        """
        Converts an operation token (e.g., 'ALTERNATE', 'MERGE') to a string.

        Parameters:
        -----------
        - token: The token representing the operation.

        Returns:
        --------
        - str: The string representation of the operation.
        """
        return str(token)

    @staticmethod
    def dictionary(items: list) -> dict:
        """
        Returns a single dictionary from the list of items.

        Parameters:
        -----------
        - items (list): List of dictionaries.

        Returns:
        --------
        - dict: The single dictionary.
        """
        return items[0]

    @staticmethod
    def dictionary_def(items: list) -> dict:
        """
        Merges a list of dictionaries into one, handling overlaps in keys by merging
        nested dictionaries recursively.

        Parameters:
        -----------
        - items (list): List of dictionaries to be merged.

        Returns:
        --------
        - dict: The merged dictionary.
        """

        def _merge_dicts(dict1: dict, dict2: dict) -> dict:
            """
            Recursively merges dict2 into dict1.

            Parameters:
            -----------
            - dict1 (dict): The first dictionary to merge into.
            - dict2 (dict): The second dictionary to merge.

            Returns:
            --------
            - dict: The merged dictionary.
            """
            for key, value in dict2.items():
                if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                    _merge_dicts(dict1[key], value)  # Recursive merge of sub-dictionaries
                else:
                    dict1[key] = value  # Overwrite or add the value from dict2
            return dict1

        # Start with an empty dictionary and merge each prop into it
        merged_dict = {}
        for prop in items:
            merged_dict = _merge_dicts(merged_dict, prop)

        return merged_dict

    @staticmethod
    def proposition(items: list) -> dict:
        """
        Parses a proposition and creates a dictionary from it, optionally handling
        types, values, and units.

        Parameters:
        -----------
        - items (list): List containing the proposition name, type, value, and unit.

        Returns:
        --------
        - dict: The parsed proposition as a dictionary.
        """
        prop_name = items[0]
        prop_type = None
        value = None
        unit = None

        # Handle propositions with optional type, value, unit
        index = 1
        if len(items) > index and (isinstance(items[index], (DimensionFormula, type)) or (
                isinstance(items[index], dict) and "list" in items[index])):
            prop_type = items[index]
            index += 1

        if len(items) > index:
            value = items[index]
            index += 1

        if len(items) > index and isinstance(items[index], dict) and 'unit' in items[index]:
            unit = items[index]
            index += 1

        if unit and prop_type:
            value = TypeUnitValue(value, prefix=unit['prefix'], unit=unit['unit'], prop_type=prop_type)
        elif unit:
            value = TypeUnitValue(value, prefix=unit['prefix'], unit=unit['unit'])
        elif prop_type:
            value = TypeUnitValue(value, prop_type=prop_type)

        # Handle the specification of properties with the . notation
        props = prop_name.split('.')
        if len(props) > 1:
            nested_dict = value
            for prop in reversed(props):
                nested_dict = {prop: nested_dict}
            return nested_dict

        return {prop_name: value}

    @staticmethod
    def PROPERTY_NAME(token) -> str:
        """
        Converts a property name token into a string.

        Parameters:
        -----------
        - token: The token representing the property name.

        Returns:
        --------
        - str: The string representation of the property name.
        """
        return str(token)

    @staticmethod
    def property_value(items: list) -> any:
        """
        Returns the first item in the list as the property value.

        Parameters:
        -----------
        - items (list): List of property values.

        Returns:
        --------
        - any: The first value in the list.
        """
        return items[0]

    @staticmethod
    def basic_property_value(items: list) -> any:
        """
        Returns the first item in the list as the basic property value.

        Parameters:
        -----------
        - items (list): List of basic property values.

        Returns:
        --------
        - any: The first basic value in the list.
        """
        return items[0]

    @staticmethod
    def number(token) -> float:
        """
        Converts a token into a floating-point number.

        Parameters:
        -----------
        - token: The token representing the number.

        Returns:
        --------
        - float: The number as a float.
        """
        return float(token[0])

    @staticmethod
    def string(token) -> str:
        """
        Converts a string token into a Python string.

        Parameters:
        -----------
        - token: The token representing the string.

        Returns:
        --------
        - str: The string value.
        """
        return str(token[0])[1:-1]

    @staticmethod
    def unit(items: list) -> dict:
        """
        Parses a unit with an optional prefix.

        Parameters:
        -----------
        - items (list): List containing unit prefix (optional) and unit word.

        Returns:
        --------
        - dict: A dictionary containing 'prefix' and 'unit' keys.
        """
        if len(items) == 2:
            prefix = items[0]
            unit = items[1]
        else:
            prefix = None
            unit = items[0]
        return {'prefix': prefix, 'unit': unit}

    @staticmethod
    def unit_prefix(token) -> str:
        """
        Converts a unit prefix token into a string.

        Parameters:
        -----------
        - token: The token representing the unit prefix.

        Returns:
        --------
        - str: The string representation of the unit prefix.
        """
        return str(token[0])

    @staticmethod
    def WORD(token) -> str:
        """
        Converts a word token into a string.

        Parameters:
        -----------
        - token: The token representing the word.

        Returns:
        --------
        - str: The string representation of the word.
        """
        return str(token)

    @staticmethod
    def LETTER(token) -> str:
        """
        Converts a letter token into a string.

        Parameters:
        -----------
        - token: The token representing the letter.

        Returns:
        --------
        - str: The string representation of the letter.
        """
        return str(token)

    @staticmethod
    def physical_type(items: list) -> DimensionFormula:
        """
        Converts a list of items into a DimensionFormula.

        Parameters:
        -----------
        - items (list): List of dimension tokens.

        Returns:
        --------
        - DimensionFormula: The resulting DimensionFormula object.
        """
        return DimensionFormula(items)

    @staticmethod
    def dimension(token) -> str:
        """
        Converts a dimension token into a string.

        Parameters:
        -----------
        - token: The token representing the dimension.

        Returns:
        --------
        - str: The string representation of the dimension.
        """
        return str(token)

    @staticmethod
    def composed_type(items: list) -> dict:
        """
        Converts a list of items into a composed type, represented as a list.

        Parameters:
        -----------
        - items (list): List of items representing the composed type.

        Returns:
        --------
        - dict: A dictionary representing the composed type (e.g., 'list').
        """
        return {'list': items[0]}

    @staticmethod
    def property_type(items: list) -> any:
        """
        Returns the first item in the list as the property type.

        Parameters:
        -----------
        - items (list): List of property types.

        Returns:
        --------
        - any: The first property type in the list.
        """
        return items[0]

    @staticmethod
    def BASIC_TYPE(token) -> type:
        """
        Returns the corresponding Python class for basic types like 'int', 'float', etc.

        Parameters:
        -----------
        - token: The token representing the basic type.

        Returns:
        --------
        - type: The Python class corresponding to the basic type.
        """
        type_map = {
            "int": int,
            "float": float,
            "str": str
        }
        return type_map.get(str(token), str)  # Default to str if the type is not found

    @staticmethod
    def set(items: list) -> Union[SetValue, object]:
        """
        Converts a list of items into a SetValue if there are multiple items.

        Parameters:
        -----------
        - items (list): List of items representing the set.

        Returns:
        --------
        - SetValue: A SetValue if there are multiple items.
         - object: The first item if only one item is present.
        """
        if len(items) > 1:
            return SetValue(items)
        return items[0]

    @staticmethod
    def list(items: list) -> Union[ListValue, object]:
        """
        Converts a list of items into a ListValue if there are multiple items.

        Parameters:
        -----------
        - items (list): List of items representing the list.

        Returns:
        --------
        - ListValue: A ListValue if there are multiple items.
        - object: The first item if only one item is present.
        """
        if len(items) > 1:
            return ListValue(items)
        return items[0]

    @staticmethod
    def range(items: list) -> RangeValue | int:
        """
        Converts a list of items into a RangeValue if there is more than one item in the range.

        Parameters:
        -----------
        - items (list): List of start, stop, and step values for the range.

        Returns:
        --------
        - RangeValue: A RangeValue object if there is more than one item in the range.
        - int: The start value if the range has only one item.
        """
        if len(range(int(items[0]), int(items[1]), int(items[2]))) > 1:
            return RangeValue(start=int(items[0]), stop=int(items[1]), step=int(items[2]))
        return int(items[0])

    @staticmethod
    def SIGNED_NUMBER(token) -> float:
        """
        Converts a signed number token into a float.

        Parameters:
        -----------
        - token: The token representing the signed number.

        Returns:
        --------
        - float: The signed number as a float.
        """
        return float(token)

    def dictionary_ref(self, items: list, local_exspecs: dict = None) -> dict:
        """
        Handles dictionary references by loading the referenced exspec from a file or resolving
        it from local definitions. Detects recursive references and handles them properly.

        Parameters:
        -----------
        - items (list): List containing package name and exspec name.
        - local_exspecs (dict): Dictionary of locally defined exspecs.

        Returns:
        --------
        - dict: The dictionary representing the referenced exspec.

        Raises:
        -------
        - VisitError: If a recursive reference is detected, wraps RecursionError.
        """
        if len(items) == 2:
            package_name = items[0]
            exspec_name = items[1]
            filename = f"{package_name}.exspec"
        else:
            exspec_name = items[0]
            filename = f"{exspec_name}.exspec"

        filepath = os.path.join(self.base_dir, filename)

        # Check for recursion
        cache_key = (filepath, exspec_name)
        if cache_key in self.loading_stack:
            loading_chain = ' -> '.join(f"{name}@{path}" for path, name in self.loading_stack + [cache_key])
            raise VisitError('dictionary_ref', None,
                             RecursionError(f"Recursive exspec reference detected: {loading_chain}"))

        # Check if already loaded
        if cache_key in self.loaded_exspecs:
            return self.loaded_exspecs[cache_key]

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Referenced exspec file not found: {filepath}")

        # Add to loading stack
        self.loading_stack.append(cache_key)

        try:
            # Read and parse the referenced exspec
            with open(filepath, 'r') as f:
                content = f.read()

            parser = Lark(exspec_grammar, parser='earley')
            parse_tree = parser.parse(content)
            transformer = ExSpecTransformer(
                base_dir=self.base_dir,
                loaded_exspecs=self.loaded_exspecs,
                loading_stack=self.loading_stack.copy()
            )
            exspecs = transformer.transform(parse_tree)

            # Find the specific exspec
            for exspec in exspecs:
                if exspec.name == exspec_name:
                    self.loaded_exspecs[cache_key] = exspec.dictionaries
                    return exspec.dictionaries

            raise ValueError(f"ExSpec '{exspec_name}' not found in file '{filepath}'")
        except RecursionError as e:
            # Wrap the RecursionError inside a VisitError so Lark can handle it properly
            raise VisitError('dictionary_ref', None, e)
        finally:
            # Ensure the cache_key is removed from the loading stack
            if cache_key in self.loading_stack:
                self.loading_stack.remove(cache_key)

    @staticmethod
    def PACKAGE_NAME(token) -> str:
        """
        Converts a package name token into a string.

        Parameters:
        -----------
        - token: The token representing the package name.

        Returns:
        --------
        - str: The string representation of the package name.
        """
        return str(token)

    @staticmethod
    def __default__(data, children, meta):
        """
        Default method to handle any unmatched parse trees.

        Parameters:
        -----------
        - data: The data node in the parse tree.
        - children: The children nodes of the data node.
        - meta: Metadata of the node.

        Returns:
        --------
        - The children or data node.
        """
        return children or data
