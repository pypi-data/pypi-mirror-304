"""
Example Usage Module
--------------------

Demonstrates how to use the exspec package to parse, manipulate, and flatten exspecs.
"""
from src.exspec.deflattener import deflatten_dict
from src.exspec.parser import parse_exspec

if __name__ == '__main__':
    input_text = """
    modelica_simulation =
    '''This is an experiment conducted with Modelica with DASSL solver'''
    {
        workflow = {
            atomic = {
                record.resolution: str = '1.8' ;
                stabilisation_time: T = RANGE(1, 2, 1) s ;
                actor = {
                    solver = {
                        name: str = 'DASSL' ;
                        tolerance: float = 1e-9 ;
                    } ;
                    python = {
                        version: str = '3.11.3' ;
                        ompython.version: str = '3.4.0' ;
                    } ;
                    modelica.version = '1.22.0' ;
                } ;
                initial = {
                    environment.output: ML2T-3I-1 = 0 V ;
                    system.charge: TI1 = 0 C ;
                } ;
            } ;
        } ;
    }
    """

    exspecs = parse_exspec(input_text)
    exspec = exspecs[0]

    print("Original ExSpec:")
    print(exspec.pretty_print())

    print(f"\nIs '{exspec.name}' atomic? {exspec.is_atomic()}")

    if exspec.is_atomic():
        # Flatten the exspec
        flat_dict = exspec.flatten()

        print("\nFlattened ExSpec Dictionary:")
        for k, v in flat_dict.items():
            print(f"{k}: {v}")

        deflattened = deflatten_dict(flat_dict, name = "modelica_simulation")
        print("\nDeflattened ExSpec:")
        print(deflattened.pretty_print())
    else:
        print("ExSpec is not atomic and cannot be flattened.")
