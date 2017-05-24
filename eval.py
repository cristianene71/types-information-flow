#!/usr/bin/python3
"""eval.

Intepreter for a simple imperative language.

Parsing the program
Typecheck (TODO)
Eval

"""
import sys
import os
import parser
import evaluation
import typing

def _usage():
    print('usage: ./eval.py file')
    exit(1)

def main():
    """ entry point to the interpreter """
    if len(sys.argv) != 2:
        _usage()

    filename = sys.argv[1]

    with open(filename, 'r') as myfile:
        input_program = myfile.read()

    print("--- parsing " + filename)
    prog = parser.parser().parse(input_program)
    exit(0)

    print('--- typechecking')
    print('todo')
    typing.typecheck(prog)

    print('--- evaluate ' + prog)
    evaluation.evaluate(prog)

if __name__ == "__main__":
    main()
