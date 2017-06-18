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
import pretty_print
import free_vars
import lat_types
import argparse
import cfg

def main():
    """ entry point to the interpreter.

    Check arguments and run the different steps.
    parsing, printing, free variables calculation and typechecking.
    """
    arg_parser = argparse.ArgumentParser(description = 
        'Information-flow typechecker for a simple imperative language.')
    arg_parser.add_argument("file", metavar="FILE", help="file to be processed", 
      nargs=1)
    arg_parser.add_argument("-v", dest='verbose', action='store_true', 
      help='verbose mode. Print debug information')
    arg_parser.add_argument("-g", dest='graph', action='store_true', 
      help='Control flow graph. Generate control flow graph')
    args = arg_parser.parse_args()
    verbose = args.verbose
    graph = args.graph

    filename = args.file[0]

    # TODO(Phil) handle exception
    with open(filename, 'r') as myfile:
        input_program = myfile.read()
    if verbose:
        print("--- parsing", filename)

    prog = parser.parser().parse(input_program)

    if graph:
        print("--- control flow graph")
        g = cfg.make_cfg(prog)
        print(g)
        exit(0)

    fv = free_vars.free_vars_prog(prog)

    if verbose:
        print("--- pretty print")
        pretty_print.print_prog(prog)

    if verbose:
        print('--- typechecking')

    gamma = lat_types.create_init_env(fv)

    if verbose:
        print('initial environment:', gamma)

    new_gamma = typing.typecheck(gamma, prog)

    print('final environment:', new_gamma)

if __name__ == "__main__":
    main()
