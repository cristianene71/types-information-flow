# Typing for information flow 

*Very preliminary* implementation of the type system defined in "On Flow-Sensitive Security Types" (S.Hunt and D.Sands) in python3. The code should be straighforward to understand, it follows the algorithmic typing rules from the paper.

### Usage

You need to install the `ply` [package](http://www.dabeaz.com/ply/) using python package manager (`pip`):
    
    pip3 install ply
  
Then:

    python3 main.py file

or (you may need to change the path to python3 on the first line): 

    ./main.py file

To run all tests:

    ./run-tests.sh

See options with `./main.py -h`

### Langage

Simple imperative language with C-like syntax. No variable declarations. All values are integers. See parser.py for concrete and abstract syntax.

### Types

We use the lattice of finite sets of variables extended with a 'top' element. The initial context is deduced from the (free) variables of the program. Each variable is mapped to its associated singleton.

### Examples

    > ./main.py -v tests/if_then2.w 
    --- parsing tests/if_then2.w
    --- pretty print
    if ((x==1)) {
      y = 2;
    } else {
      skip;
    }
    --- free variable
    {'y', 'x'}
    --- typechecking
    initial environment: {'y': {'y'}, 'x': {'x'}}
    final environment: {'y': {'y', 'x'}, 'x': {'x'}}

