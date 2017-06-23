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

def leq(x,y):
    return x.issubset(y)

def compl(v):
    """ returns a `complement` variable to be used by the typesystem
        to identify dependency with output variables
    """
    assert(v[0] != '_')
    return '_' + v

def is_compl(v):
    assert(len(v) == 1)
    for x in v:
        return x[0] == '_'

def subst(ty, x, y):
    """ substitutes variable x in type t with variables in y.
        x has to be a `complement` variable  """
    assert(is_compl(x))
    res = ty
    if leq(x, ty): 
        res = ty.difference(x).union(y)
    return res

def type_from_var(v):
    """ returns the singleton containing v """
    return {v}

def create_singleton_env(fv):
    """ Initial typing environnment maps each variable to the corresponding
    singleton.
    """ 
    return dict([(x, type_from_var(x)) for x in fv])

def create_complement_env(fv):
     """ Initial typing environnment maps each variable to the corresponding
     'complement' singleton.
     """ 
     return dict([(x, type_from_var(compl(x))) for x in fv])

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

def join_list(l):
    res = set()
    for x in l:
        res = res.union(x)
    return res

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
