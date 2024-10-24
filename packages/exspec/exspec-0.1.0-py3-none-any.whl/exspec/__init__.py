"""
ExSpec Package
--------------

The **ExSpec** package provides tools to parse, manipulate, and analyze **experiment specifications (exspecs)** defined
by a custom grammar. It includes functionality for:

- Parsing exspecs from text which defines a formula on dictionaries.
- Performing operations like **MERGE** and **ALTERNATE** on exspecs.
- Resolving composed exspecs into a set of constituent atomic exspecs.
- Pretty-printing atomic exspecs.
- Flattening exspecs into flat dictionaries suitable for metadata storage (e.g., in InfluxDB).
- De-flattening flattened exspecs with no information loss. *
- Comparing exspecs to determine if one specializes another.
- Comparing exspecs to determine if one is a subset of another.
- Handling ranges, units, and physical quantities in exspecs.


## Installation

To install the `exspec` package, use `pip`:

```bash
pip install exspec
```

## ExSpec Language

ExSpecs are organized as packages represented by files with the '.exspec' extension. It is assumed that all these
files/packages are available in the same directory in order to resolve references to exspecs in-between packages.


### Basic Syntax

An **exspec** is a set of dictionaries.
Each dictionary in the ExSpec represents an alternate experiment specification within
the composed experiment specification.
A dictionary defines the parameters and configurations for experiments in a structured, hierarchical format.
The syntax resembles a combination of JSON and custom constructs.

**Example:**

```plaintext
my_exspec = {
  prop1 = 'value1' ;
  prop2 = 42 ;
  nested = {
    prop3 = 3.14 ;
  };
}
```

ExSpecs can be specified as a formulation of different dictionaries:

**Example:**

```plaintext
my_exspec = {
  prop1 = 'value1' ;
  prop2 = 42 ;
} MERGE {
  nested = {
    prop3 = 3.14 ;
  };
}
```

### Propositions

A **proposition**  is a key-value pair within an exspec's dictionaries.
Propositions can be nested to create hierarchical structures.

**Syntax:**

```plaintext
property_name = property_value ;
```

**Example:**

```plaintext
simulation = {
    duration = 100 ;
    solver = 'DASSL' ;
    settings = {
        tolerance = 1e-6 ;
    } ;
}
```

### Types

You can optionally specify the types of the value/s in a proposition.
Properties can have explicit types specified, including basic types (`str`, `int`, `float`), composed types (e.g.,
`list[int]`, `list[list[ ... ]]`).

**Syntax:**

```plaintext
property_name : type = value ;
```

**Example:**

```plaintext
simulation.solver : str = 'DASSL' ;
```

**Physical Dimensions:**

You can also specify dimensions of physical quantities as a dimensional formula.

Dimensions are specified using SI base units:

- `M` (mass)
- `L` (length)
- `T` (time)
- `I` (current)
- `K` (temperature)
- `N` (substance amount)
- `J` (luminous intensity)

**Example:**

```plaintext
force : MLT-2 = 9.8 ;
```

### Units

You can optionally specify units of the value/s in a proposition.
Units can be any string representing a unit (e.g., `m`, `s`, `g`, `N`)
There is no inbuilt library for conversion of units for comparison,
so be careful to use only one standard system of units.

You can also optionally specify the prefix of the unit.

**Prefixes:**
- `n-` (nano)
- `u-` (micro)
- `m-` (milli)
- `k-` (kilo)
- `M-` (mega)
- `G-` (giga)
- `T-` (tera)

**Syntax:**

```plaintext
property_name = value prefix-unit ;
```

**Example:**

```plaintext
length = 10 n-m ;
time = 5 k-s ;
```

The prefix is taken into account when comparing propositions.
So `1e9 n-m == 1 m` will evaluate to True.

### Multi-Values

You can use the multivalued propositions to compactly describe a composed experiment specification, where the
multivalued properties are chosen combinatorially.

There are 2 types of constructs to specify multiple values for a property.
You can even specify the types and units of multivalued properties with no problems.

**Range Syntax:**

```plaintext
property_name = RANGE(start, stop, step) ;
```

**Example:**

```plaintext
temperature = RANGE(300, 350, 10) K ;
```

**Set Syntax:**

```plaintext
property_name = { value1; value2; value3 } ;
```

**Example:**

```plaintext
modes : str = { 'mode1'; 'mode2'; 'mode3' } ;
```

### Composed Values

There may arise the need to specify a property that is a composition of multiple basic values.
In such a case, you can use a List.
The items of a list are not interpreted as leading to a composition of experiments.

**Set Syntax:**

```plaintext
property_name = [ value1, value2, value3 ] ;
```

**Example:**

```plaintext
modes : str = [ 'mode1', 'mode2', 'mode3' ] ;
```

### Operations

ExSpecs can be defined as formulas (over dictionaries) by composing two operations:

- **MERGE** : Combines two exspecs into one, ensuring no conflicting propositions.

- **ALTERNATE** : Creates an exspec representing all combinations of the input exspecs.

**Syntax:**

```plaintext
exspec1 MERGE exspec2
exspec1 ALTERNATE exspec2
```
### External References

ExSpecs can reference exspecs from other packages in formulas:

**Syntax:**

```plaintext
exspec1 OPERATION package_name::exspec_name
```

## Getting Started

This project is licensed under the MIT License. See the [LICENSE](#https://gitlab.rakshitmittal.net/mde/msdl/exspec/-/blob/main/LICENSE)  file for details.

**Step 1:**  Install the package using `pip`.

```bash
pip install exspec
```

**Step 2:**  Import the necessary modules in your Python script.

```python
from exspec.parser import parse_exspec
from exspec.deflattener import flatten_exspec
from exspec.models import ExSpec
from exspec.operations import merge, alternate
```

**Step 3:**  Define your exspecs as strings and parse them. You can also use exspecs defined in files instead.

```python
input_text = "simulation = {duration = 100 s; solver = 'DASSL';}"
exspecs = parse_exspec(input_text)
simulation_exspec = exspecs[0]
```

**Step 4:**  Use the exspec as needed.

- **Flattening:**

```python
if simulation_exspec.is_atomic():
    flat_dicts = flatten_exspec(simulation_exspec)
    flat_dict = flat_dicts[0]
    # Use flat_dict as metadata
```

- **Operations:**

```python
merged_exspec = ExSpec('merged', merge(exspec1.dictionaries, exspec2.dictionaries))
alternated_exspec = ExSpec('alternated', alternate(exspec1.dictionaries, exspec2.dictionaries))
```

- **Comparison:**

```python
if exspec1.is_subset_of(exspec2):
    print(f"{exspec1.name} is a subset of {exspec2.name}")
elif exspec1.is_subset_of(exspec2) is None:
    print("Exspecs cannot be compared")
else:
    print(f"{exspec1.name} is not a subset of {exspec2.name}")
```

### Example Script

An example script demonstrating how to use the package is included in `exspec/example.py`.

**Running the Example:**

```bash
python -m exspec.example
```

## How to Invoke the Tests

**Prerequisites:**

- Ensure you have the `exspec` package code and the `tests/` directory in your project.

**Steps:**
1. Navigate to the root directory of your project (where `setup.py` is located).

2. Run the following command:

```bash
python -m unittest discover -s tests
```

**Notes:**

- The tests use Python's built-in `unittest` framework.

- The `discover` command automatically finds and runs all test modules in the `tests/` directory.

## Documentation

The **ExSpec**  package provides a flexible way to define and manipulate experiment specifications.
With support for units, ranges, and complex operations, it can be a valuable tool for managing experimental
configurations and metadata.

Full documentation is available in the `docs/` directory. This documentation was
generated with `pdoc`, a Python documentation generator that automatically extracts
docstrings and generates HTML documentation.

You can access the generated documentation by navigating to the `docs/` folder. You may need to download the directory
and view `index.html` with a web-browser.

## Modules
- grammar.py: Contains the Lark grammar for parsing exspecs.
- parser.py: Implements the parser and transformer to build ASTs from exspecs.
- models.py: Defines data structures for exspecs, dictionaries, propositions, etc.
- operations.py: Exposes merge and alternate functions for programmatic use.
- utils.py: Provides utility functions for unit handling and comparisons.
- deflattener.py: Contains utilities to deflatten a dictionary.
- example.py: Demonstrates how to use the package with an example exspec.
"""

__version__ = '1.0.0'
