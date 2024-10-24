"""
Grammar Module
-------------------------

This module defines the grammar for the exspec language using Lark's EBNF syntax.
The grammar is responsible for parsing experiment specification definitions,
allowing for structured configurations in the exspec language.

The grammar supports:
- Definitions of specifications, dictionaries, and properties.
- References to other dictionaries or packages.
- Composed and physical types, such as lists and dimension-based units.
- Basic data types (e.g., strings, integers, floats) as well as ranges, sets, and units.

Grammar structure:
------------------
- The `start` rule serves as the entry point for the grammar, representing a list of specifications.
- Specifications define key-value mappings that can reference other dictionaries or define new ones.
- Operations, such as `ALTERNATE` and `MERGE`, are used to combine dictionaries.
- Properties within dictionaries can have types, values, and optional units, including physical units like mass (M), length (L), and time (T).

Lark's extended Backus-Naur Form (EBNF) is used to express the grammar.
"""

exspec_grammar = r"""
    start: specification+

    specification: EXSPEC_NAME "=" formula

    EXSPEC_NAME: CNAME

    %import common.CNAME

    formula: (dictionary OPERATION)* dictionary

    OPERATION: "ALTERNATE"
             | "MERGE"

    dictionary: dictionary_ref
              | dictionary_def
              | "(" formula ")"

    dictionary_ref: (PACKAGE_NAME "::")? EXSPEC_NAME

    PACKAGE_NAME: CNAME

    dictionary_def: "{" proposition+ "}"

    proposition: PROPERTY_NAME (":" property_type)? "=" property_value unit? ";"
               | PROPERTY_NAME "=" (dictionary_def | dictionary_ref) ";"

    PROPERTY_NAME: (CNAME".")* CNAME

    property_type: BASIC_TYPE | composed_type | physical_type

    BASIC_TYPE: "str" | "int" | "float"

    composed_type: "list[" property_type "]"

    physical_type: (dimension (INT | SIGNED_INT)?)+

    %import common.SIGNED_INT
    %import common.INT

    dimension: "M" -> mass
             | "L" -> length
             | "T" -> time
             | "I" -> current
             | "K" -> temperature
             | "N" -> substance
             | "J" -> luminosity

    property_value: "RANGE(" START "," END ("," STEP)? ")" -> range
                  | "{" (basic_property_value ";")* basic_property_value "}" -> set
                  | basic_property_value

    START: NUMBER | SIGNED_NUMBER

    END: NUMBER | SIGNED_NUMBER

    STEP: NUMBER | SIGNED_NUMBER

    basic_property_value: basic_value
                        | "[" (basic_value ("," basic_value)*)? "]" -> list

    basic_value: (NUMBER | SIGNED_NUMBER) -> number
               | /'.*?'/ -> string

    %import common.SIGNED_NUMBER
    %import common.NUMBER

    unit: unit_prefix? (LETTER | WORD)

    unit_prefix: "n-" -> nano
               | "u-" -> micro
               | "m-" -> milli
               | "k-" -> kilo
               | "M-" -> mega
               | "G-" -> giga
               | "T-" -> tera

    %import common.WORD
    %import common.LETTER
    
    COMMENT: /#.*/
    MULTI_LINE_COMMENT: /'''(.|\n)*?'''/

    %import common.WS
    %ignore WS
    %ignore COMMENT
    %ignore MULTI_LINE_COMMENT
"""
