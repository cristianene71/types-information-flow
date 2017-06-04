""" Types and type environments

An environment is a dictionary that maps identifiers to types. The lattice of
types is the powerset of identifiers, extened with a 'top'  element. In other
words, a type is either 'top' or a set of identifiers.  To make things simple,
the initial typing environment is created from the (free) variables of
the program. Each variable is mapped to its associated singleton.

This package could implement another lattice and the rest of the program
wouldn't be affected since typechecking is parameterized by a lattice.
The parser/AST may need be extended to allow the user to declare custom types.
"""

bottom = set() 
top = None

def type_from_var(v):
    return set([v])

def create_init_env(fv):
    """ Initial typing environnment maps each variable to the corresponding
    singleton.
    """ 
    return dict([(x, type_from_var(x)) for x in fv])

def meet(x,y):
    if x == top:
        return y
    if y == top:
        return x
    return x.intersection(y)  

def join(x,y):
    if x == top or y == top:
        return top
    return x.union(y)

def join_env(gamma1, gamma2):
    res = dict()
    for x in gamma1:
        if x in gamma2:
          res[x] = join(gamma1[x], gamma2[x])
        else:
          res[x] = gamma1[x]
    for y in gamma2:
        if not y in gamma1:
          res[y] = gamma2[y]
    return res