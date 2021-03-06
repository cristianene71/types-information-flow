""" Typechecking
    Follow the algorithmic rule of the paper
"""

import lat_types

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
    elif tag == 'ASSIGN':
        var = s[1]
        expr = s[2]
        t = _compute_expr_type(gamma, expr)
        res = gamma.copy()
        res[var] = lat_types.join(p, t)
    elif tag == 'WHILE':
        expr = s[1]
        code = s[2]
        gamma_pr = gamma 
        gamma_old = None
        while gamma_pr != gamma_old:
            gamma_old = gamma_pr
            t = _compute_expr_type(gamma_pr, expr)
            gamma_sd = _compute_types_block(gamma_pr, lat_types.join(p, t), code) 
            gamma_pr = lat_types.join_env(gamma_pr, gamma_sd)
        res = gamma_pr
    elif tag == 'IF':
        t = _compute_expr_type(gamma, s[1])
        gamma1 = _compute_types_block(gamma, lat_types.join(p, t), s[2])
        gamma2 = _compute_types_block(gamma, lat_types.join(p, t), s[3])
        res = lat_types.join_env(gamma1, gamma2)
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
    return _compute_types_prog(gamma, lat_types.bottom, prog)
