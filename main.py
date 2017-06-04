#!/usr/local/bin/python3
"""main.

Typechecking non-interference.

Implementation of the type system defined in 
"On Flow-Sensitive Security Types" (S.Hunt and D.Sands):
"""

import os
import sys
import parser
import typing
import typing_os
import pretty_print
import free_vars
import lat_types

def _usage():
    print('usage: ./main.py file')
    exit(1)

def main():
    """ entry point to the interpreter.

    Check arguments and run the different steps.
    parsing, printing, free variables calculation and typechecking.
    """
    if len(sys.argv) != 2:
        _usage()

    filename = sys.argv[1]

    with open(filename, 'r') as myfile:
        input_program = myfile.read()

    print("--- parsing", filename)
    prog = parser.parser().parse(input_program)

    print("--- pretty print")
    pretty_print.print_prog(prog)

    print("--- free variable")
    fv = free_vars.free_vars_prog(prog)
    print(fv)

    gamma = lat_types.create_init_env(fv)
    print('initial environment:', gamma)

    print('--- typechecking (hunt-sand)')
    new_gamma = typing.typecheck(gamma, prog)
    print('final environment:', new_gamma)

    print('--- typechecking (output-sensitive)')
    new_gamma = typing_os.typecheck(gamma, prog)
    print('final environment:', new_gamma)

if __name__ == "__main__":
    main()
