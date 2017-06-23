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
import ast
import free_vars
import lat_types
import argparse
import cfg
import dataflowanalysis

def main():
    """ entry point to the interpreter.

    Check arguments and run the different steps.
    parsing, printing, free variables calculation and typechecking.
    """
    arg_parser = argparse.ArgumentParser(description = 
        'Information-flow typechecker for a simple imperative language.')
    arg_parser.add_argument("file", metavar="FILE", help="file to be processed", 
      nargs=1)
    arg_parser.add_argument("-o", dest='target', 
        help="specify target dot file. To be used with -g option", nargs=1)
    arg_parser.add_argument("-v", dest='verbose', action='store_true', 
      help='verbose mode. Print debug information')
    arg_parser.add_argument("-g", dest='graph', action='store_true', 
      help='Control flow graph. Generate control flow graph')
    args = arg_parser.parse_args()

    verbose = args.verbose
    graph = args.graph
    target = args.target

    if target and not graph:
        print('target file ignored, to be used with -g option')

    filename = args.file[0]

    # TODO(Phil) handle exception
    with open(filename, 'r') as myfile:
        input_program = myfile.read()

    if verbose:
        print("--- parsing", filename)

    prog = parser.parser().parse(input_program)

    if graph:
        g = cfg.make_cfg(prog)

        # TODO(phil) rewrite this and handle exception
        if not target:
            # no output specified, use stdout
            cfg.print_dot(g, sys.stdout)
        else:
            with open(target[0], 'w') as myfile:
                cfg.print_dot(g, myfile)
            myfile.close()

        sol = dataflowanalysis.compute_liveness(g)
        dataflowanalysis.print_sol(sol)
        dataflowanalysis.check_var_not_used(g, sol)

        exit(0)

    fv = free_vars.free_vars_prog(prog)
    Xo = free_vars.output_vars_prog(prog)

    if not set(Xo).issubset(set(fv)):
        print('ERROR: returned vars must be included in free vars')
        exit(1)

    if verbose:
        print("--- pretty print")
        ast.print_prog(prog)

        print("--- free and output variable")
        print('free', fv)
        print('output', Xo)

    gamma_init_hs = lat_types.create_singleton_env(fv)

    if verbose:
        print('--- typechecking (hunt-sand)')
        if Xo:
            print('WARNING: output variables are ignored')
            
        print('* initial environment:', gamma_init_hs)

    gamma_final_hs = typing.typecheck(gamma_init_hs, prog)

    if verbose:
        print('* final environment:', gamma_final_hs)
        print('--- typechecking (output-sensitive)')

    gamma_init_os = lat_types.create_singleton_env(fv)
    gamma_init_os.update(lat_types.create_complement_env(Xo))
    alpha_init_os = lat_types.create_singleton_env(Xo)
    if verbose:
        print('* initial gamma', gamma_init_os) 
        print('* initial alpha', alpha_init_os) 

    gamma_final_os, alpha_final_os  = typing_os.typecheck(gamma_init_os, alpha_init_os, Xo, prog)

    if verbose:
        print('* final gamma:', gamma_final_os)
        print('* final alpha:', alpha_final_os)

    print('--- sanity check')

    if Xo: 
        gamma_no_output, alpha_no_output = typing_os.subst_all_output(gamma_final_os, alpha_final_os, Xo)
        gamma_alpha_os_no_output = { x : gamma_no_output[x] for x in gamma_no_output if x not in Xo }
        gamma_alpha_os_no_output.update(alpha_no_output)
        print('leaked variables: gamma_alpha_os_no_ouput == gamma_hs')
        if gamma_alpha_os_no_output == gamma_final_hs:
            print('OK')
        else:
            print('NOT OK')
            print('gamma_alpha_os_no_output', gamma_alpha_os_no_output)
            print('gamma_final_hs', gamma_final_hs)
    else:
        print('no leaked variables: gamma_final_hs == gamma_final_os')
        if gamma_final_os == gamma_final_hs:
            print('OK') 
        else:
            print('NOT OK')
            print('gamma_final_hs', gamma_final_hs)
            print('gamma_final_os', gamma_final_os)

if __name__ == "__main__":
    main()
