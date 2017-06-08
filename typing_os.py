""" Typechecking
    Follow the algorithmic rule of the paper
"""

import lat_types
import free_vars

def _subst(gamma, alpha, Xo, x):
    assert(x in Xo)
    go = gamma[x]
    ao = alpha[x]
    new_gamma = { y : lat_types.subst(gamma[y], go, ao) if y not in Xo else gamma[y] for y in gamma}
    new_alpha = { y : lat_types.subst(alpha[y], go, ao) for y in alpha}
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
        # x := expr
        x = s[1]
        expr = s[2]
        fv_expr = free_vars.free_vars_exp(expr)
        if not x in Xo:
            # Rule As1
            gamma_new = gamma.copy()
            ty = lat_types.join_list([gamma[x] for x in fv_expr])
            gamma_new[x] = ty
            res = gamma_new, alpha, V, Z.union({x})
        else:
            gamma1, alpha1 = _subst(gamma, alpha, Xo, x)  

            if x in fv_expr:
                # Rule As3 
                ty = lat_types.join_list([gamma1[y] for y in fv_expr if y != x])
                ty = lat_types.join(ty, alpha[x])
            else:
                # Rule As2
                ty = lat_types.join_list([gamma1[y] for y in fv_expr])

            alpha1[x] = ty
            res = gamma1, alpha1, V.union({x}), Z
    elif tag == 'IF':
        if_block = s[2]
        else_block = s[3]
        gamma1, alpha1, U1, W1 = _compute_types_block(gamma, alpha, set(), set(), Xo, if_block)
        gamma2, alpha2, U2, W2 = _compute_types_block(gamma, alpha, set(), set(), Xo, else_block)
        gamma0 = lat_types.join_env(gamma1, gamma2) 
        alpha0 = lat_types.join_env(alpha1, alpha2) 
        U0 = U1.union(U2)
        W0 = W1.union(W2)
        res = gamma0, alpha0, U0, W0
    elif tag == 'WHILE':
        expr = s[1]
        code = s[2]
        print("not yet implemented")
        assert(False)
    else:
        print("don't know tag", tag, s)    
        assert(False)
    return res


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