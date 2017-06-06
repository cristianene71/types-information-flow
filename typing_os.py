""" Typechecking
    Follow the algorithmic rule of the paper
"""

import lat_types
import free_vars

def subst(gamma, alpha, Xo, o):
    assert(o in Xo)
    go = gamma[o]
    ao = alpha[o]
    new_gamma = gamma.copy()
    new_alpha = alpha.copy()
    for x in gamma:
        if x in Xo:
            continue
        new_gamma[x] = lat_types.subst(gamma[x], go, ao)
    for x in alpha:
        new_alpha[x] = lat_types.subst(alpha[x], go, ao)
    return new_gamma, new_alpha

def _compute_types_block(gamma, alpha, V, Z, Xo, b):
    assert(b[0] == 'BLOCK')
    for stm in b[1]:
        gamma, alpha, V, Z = _compute_types_stm(gamma, alpha, V, Z, Xo, stm)
    return gamma, alpha, V, Z

def _compute_types_stm(gamma, alpha, V, Z, Xo, s):
    tag = s[0]
    if tag == 'SKIP':
        res = gamma, alpha, V, Z
    elif tag == 'ASSIGN':
        var = s[1]
        expr = s[2]
        fv_expr = free_vars.free_vars_exp(expr)
        if not var in Xo:
            gamma_new = gamma.copy()
            ty = lat_types.join_list([gamma[x] for x in fv_expr])
            gamma_new[var] = ty
            res = gamma_new, alpha, V, Z.union({var})
        else:
            gamma1, alpha1 = subst(gamma, alpha, Xo, var)  

            if var in fv_expr:
                fv_expr_minus_var = fv_expr.difference({var})
                ty = lat_types.join_list([gamma1[x] for x in fv_expr_minus_var])
                ty = lat_types.join(ty, alpha[var])
            else:
                ty = lat_types.join_list([gamma1[x] for x in fv_expr])

            alpha1[var] = ty
            res = gamma1, alpha1, V.union({var}), Z
    else:
        print("don't know tag", tag, s)    
        assert(False)
    return res

    # if tag == 'WHILE':
    #     expr = s[1]
    #     code = s[2]
    #     gamma_pr = gamma 
    #     gamma_old = None
    #     while gamma_pr != gamma_old:
    #         gamma_old = gamma_pr
    #         t = _compute_expr_type(gamma_pr, expr)
    #         gamma_sd = _compute_types_block(gamma_pr, lat_types.join(p, t), code) 
    #         gamma_pr = lat_types.join_env(gamma_pr, gamma_sd)
    #     res = gamma_pr
    # elif tag == 'IF':
    #     t = _compute_expr_type(gamma, s[1])
    #     gamma1 = _compute_types_block(gamma, lat_types.join(p, t), s[2])
    #     gamma2 = _compute_types_block(gamma, lat_types.join(p, t), s[3])
    #     res = lat_types.join_env(gamma1, gamma2)

def _compute_types_prog(gamma, alpha, V, Z, Xo, prog):
    return _compute_types_block(gamma, alpha, V, Z, Xo, prog)

def typecheck(gamma, alpha, V, Z, Xo, prog):
    """Compute new type environment after execution of prog in env gamma.

    Args:
        gamma (dict): dict, initially map regular variables to corresponding
                      singleton. All other variables to `complement` singleton. 
        alpha (dict): dict, initially map all output variable to corresponding 
                      singleton
        V (set): over-approximation of assigned output variables (initially empty)
        Z (set):                    of assigned non-output variables (initially empty)
        prog (ast): Program to be typed 

    Returns:
        ...
    """
    assert(prog[0] == 'PROG')
    return _compute_types_prog(gamma, alpha, V, Z, Xo, prog[1])