# Typing for information flow 

Implementation of the type system defined in "On Flow-Sensitive Security Types" (S.Hunt and D.Sands) in python3.

### Usage

You need to install the `ply` [package](http://www.dabeaz.com/ply/) using python package manager (`pip`):
    
    pip3 install ply
  
Then:

    python3 main.py file

or (you may need to change the path to python3 on the fisrt line): 

    ./main.py file

To run all tests:

    ./run-tests.sh

### Langage

Simple imperative language with C-like syntax. No variable declarations. All values are integers. See parser.py for concrete and abstract syntax.

### Types

We use the lattice of finite sets of variables extended with a 'top' element. The initial context is deduced from the (free) variables of the program. Each variable is mapped to its associated singleton.

### Examples

    > ./main.py tests/if_then.w 
    --- parsing tests/if_then.w
    --- pretty print
    x = 1;
    if ((x==1)) {
      y = 2;
    } else {
      skip;
    }
    --- free variable
    {'y', 'x'}
    --- typechecking
    initial environment: {'y': {'y'}, 'x': {'x'}}
    final environment: {'y': {'y'}, 'x': set()}

### TODO

* enforce python coding guidelines
* typecheck while 
* add precedence/associativity rules in the grammar
* expand this README 
* add more tests



