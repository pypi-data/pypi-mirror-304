"""
Operations Module
-----------------

Exposes the `merge` and `alternate` functions for programmatic use, allowing users
to perform these operations on exspecs or dictionaries. These operations support
merging two dictionaries or lists of dictionaries, as well as combining them
alternately.
"""

import copy
from itertools import product

from src.exspec.utils import MultiValue, TypeUnitValue


def merge(exspec1: list | dict, exspec2: list | dict) -> list:
    """
    Merges two ExSpecs or dictionaries.

    This function takes two ExSpecs or lists of dictionaries and merges them into
    a new set of combined dictionaries. If either `exspec1` or `exspec2` is a
    single dictionary, it is treated as a list with one element.

    Parameters:
    -----------
    - exspec1 (list | dict): The first ExSpec or dictionary (or list of dictionaries).
    - exspec2 (list | dict): The second ExSpec or dictionary (or list of dictionaries).

    Returns:
    --------
    - list: A list of merged dictionaries.

    Raises:
    -------
    - ValueError: If a merge conflict is detected between the dictionaries.
    """
    dict1_list = exspec1 if isinstance(exspec1, list) else [exspec1]
    dict2_list = exspec2 if isinstance(exspec2, list) else [exspec2]

    merged_list = []
    for d1, d2 in product(dict1_list, dict2_list):
        merged = merge_two_dicts(d1, d2)
        if merged is not None:
            merged_list.append(merged)
        else:
            raise ValueError("Merge conflict detected")
    return merged_list


def merge_two_dicts(dict1: dict, dict2: dict) -> dict | None:
    """
    Helper function to recursively merge two dictionaries.

    This function merges two dictionaries by recursively merging nested dictionaries
    and resolving any MultiValue or TypeUnitValue conflicts. If a conflict cannot be
    resolved, it returns `None`.

    Parameters:
    -----------
    - dict1 (dict): The first dictionary to merge.
    - dict2 (dict): The second dictionary to merge.

    Returns:
    --------
    - dict: The merged dictionary if successful.
    - None: If a conflict is detected between the dictionaries.
    """
    merged = copy.deepcopy(dict1)
    for key, value in dict2.items():
        if key in merged:
            # If both values are dictionaries, merge them recursively
            if isinstance(merged[key], dict) and isinstance(value, dict):
                result = merge_two_dicts(merged[key], value)
                if result is None:
                    return None  # Conflict detected in nested dictionaries
                merged[key] = result
            # If they are not both dictionaries, check for conflict
            elif isinstance(value, MultiValue) and value.contains(merged[key]):
                merged[key] = value
            elif isinstance(value, TypeUnitValue) and isinstance(merged[key], TypeUnitValue):
                if all(x in value.resolve() for x in merged[key].resolve()):
                    merged[key] = value
            elif merged[key] != value:
                return None  # Conflict detected
        else:
            merged[key] = value
    return merged


def alternate(dict1: list | dict, dict2: list | dict) -> list:
    """
    Combines two ExSpecs or dictionaries into a composed ExSpec.

    This function alternately combines two ExSpecs or dictionaries into a single
    list of dictionaries, where any duplicate dictionaries are ignored. If either
    `dict1` or `dict2` is a single dictionary, it is treated as a list with one element.

    Parameters:
    -----------
    - dict1 (list | dict): The first dictionary or list of dictionaries.
    - dict2 (list | dict): The second dictionary or list of dictionaries.

    Returns:
    --------
    - list: A combined list of dictionaries, with duplicates removed.
    """
    list1 = dict1 if isinstance(dict1, list) else [dict1]
    list2 = dict2 if isinstance(dict2, list) else [dict2]
    returnlist = list1
    for elem2 in list2:
        if not any(elem1 == elem2 for elem1 in list1):
            returnlist.append(elem2)
    return returnlist
