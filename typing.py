""" Typechecking
    Follow the algorithmic rule of the paper
    Types are elements of the lattice of finite sets of variables 
    + a top element.
"""

bottom = set() 
top = None

def _meet(x,y):
    if x == top:
        return y
    if y == top:
        return x
    return x.intersection(y)  

def _join(x,y):
    if x == top or y == top:
        return top
    return x.union(y)

def _join_env(gamma1, gamma2):
    res = dict()
    for x in gamma1:
        if x in gamma2:
          res[x] = _join(gamma1[x], gamma2[x])
        else:
          res[x] = gamma1[x]
    for y in gamma2:
        if not y in gamma1:
          res[y] = gamma2[y]
    return res

def _compute_expr_type(gamma, e):
    tag = e[0]
    if tag == 'INT':
        return set()
    elif tag == 'IDENT':
        return gamma[e[1]] 
    elif tag == 'BINOP':
        return _compute_expr_type(gamma, e[2]).union(_compute_expr_type(gamma, e[3]))
    else:
        print("don't know tag", tag, e)
        assert(False)

def _compute_types_block(gamma, p, b):
    assert(b[0] == 'BLOCK')
    for stm in b[1]:
        gamma = _compute_types_stm(gamma, p, stm)
    return gamma 

def _compute_types_stm(gamma, p, s):
    tag = s[0]
    if tag == 'SKIP':
        res = gamma 
    elif tag == 'AFFECT':
        var = s[1]
        expr = s[2]
        t = _compute_expr_type(gamma, expr)
        res = gamma.copy()
        res[var] = _join(p, t)
    elif tag == 'WHILE':
        expr = s[1]
        code = s[2]
        gamma_pr = gamma 
        gamma_old = None
        while gamma_pr != gamma_old:
            gamma_old = gamma_pr
            t = _compute_expr_type(gamma_pr, expr)
            gamma_sd = _compute_types_block(gamma_pr, _join(p, t), code) 
            gamma_pr = _join_env(gamma_pr, gamma_sd)
        res = gamma_pr
    elif tag == 'IF':
        t = _compute_expr_type(gamma, s[1])
        gamma1 = _compute_types_block(gamma, _join(p, t), s[2])
        gamma2 = _compute_types_block(gamma, _join(p, t), s[3])
        res = _join_env(gamma1, gamma2)
    else:
        print("don't know tag", tag, s)
        assert(False)
    return res

def _compute_types_prog(gamma, p, prog):
    return _compute_types_block(gamma, p, prog)

def typecheck(gamma, prog):
    """Compute new type environment after execution of prog in env gamma.

    Args:
        gamma (dict): Initial env
        prog (ast): Program to be typed 

    Returns:
        dict: New type environment.
    """
    return _compute_types_prog(gamma, bottom, prog)