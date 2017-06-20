""" Typechecking "output-sensitive"
    Generalization of Hunt-Sands typechecker (ongoing work).
"""

import lat_types
import free_vars

def _subst(gamma, alpha, Xo, x):
    """ (Gamma, Alpha) <| x in the paper
        x is an output variable
        substitutes all occurences of compl(x) in gamma and alpha with content of alpha[x]
        (except in x -> {compl{x}} in Gamma that remains constant)
        this is to update former dependencies to output variables in type environment
        For instance in:
          o = y; (1)
          x = o; (2)
          o = 1; (3)
        After o is updated in 3, x no longer depends on final value of o, although 
        it still depends on 'y' 
    """
    assert(x in Xo)
    go = gamma[x]
    assert(go == {lat_types.compl(x)}) # TODO(phil) why keep x -> {compl(x)} in Gamma if it's constant anyway?
    ao = alpha[x]
    new_gamma = { y : lat_types.subst(gamma[y], go, ao) if y not in Xo else gamma[y] for y in gamma}
    new_alpha = { y : lat_types.subst(alpha[y], go, ao) for y in alpha}
    return new_gamma, new_alpha

def _subst_if_aux(ty, gamma, alpha, Xo, U):
    for x in U:
        assert(x in Xo) 
        go = gamma[x]
        ao = alpha[x]
        assert(go == {lat_types.compl(x)}) # TODO(Phil) why keep x -> {compl(x)} in Gamma if it's constant anyway?
        ty = lat_types.subst(ty, go, ao)
    return ty

def _subst_if(ty, gamma, alpha, Xo, U):
    """ (ty, Gamma, Alpha) <| U) in the paper, used in If rule.
        U is a set of variables.

        if (h) {
          l = 1; 
        } else {
          l = 2;
        }
        ... TODO(phil) complete this comment
    """
    new_ty = ty
    while True:
        ty = new_ty
        new_ty = _subst_if_aux(new_ty, gamma, alpha, Xo, U)
        if new_ty == ty:
            break
    return ty

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
            ty = lat_types.join_list([gamma[y] for y in fv_expr])
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
        expr = s[1]
        if_block = s[2]
        else_block = s[3]

        gamma1, alpha1, U1, W1 = _compute_types_block(gamma, alpha, set(), set(), Xo, if_block)
        gamma2, alpha2, U2, W2 = _compute_types_block(gamma, alpha, set(), set(), Xo, else_block)

        gamma0 = lat_types.join_env(gamma1, gamma2) 
        alpha0 = lat_types.join_env(alpha1, alpha2) 

        U0 = U1.union(U2)
        W0 = W1.union(W2)

        fv_expr = free_vars.free_vars_exp(expr)
        ty = lat_types.join_list([gamma[y] for y in fv_expr])
        p = _subst_if(ty, gamma, alpha, Xo, U0)

        # print('DEBUG IF p =', p)
        new_alpha = { y : lat_types.join(alpha0[y], p) if y in U0 else alpha0[y] for y in alpha0}
        new_gamma = { y : lat_types.join(gamma0[y], p) if y in W0 else gamma0[y] for y in gamma0}

        res = new_gamma, new_alpha, V.union(U0), Z.union(W0)
    elif tag == 'WHILE':
        expr = s[1]
        block = s[2]

        gamma_init = gamma
        alpha_init = alpha

        new_alpha = alpha
        new_gamma = gamma

        while True:
            alpha = new_alpha
            gamma = new_gamma

            gamma0, alpha0, U0, W0 = _compute_types_block(gamma, alpha, set(), set(), Xo, block)

            fv_expr = free_vars.free_vars_exp(expr)
            ty = lat_types.join_list([gamma_init[y] for y in fv_expr])
            p = _subst_if(ty, gamma_init, alpha_init, Xo, U0)

            # print('DEBUG WHILE p =', p)
            new_alpha = { y : lat_types.join(alpha0[y], p) if y in U0 else alpha0[y] for y in alpha0}
            new_gamma = { y : lat_types.join(gamma0[y], p) if y in W0 else gamma0[y] for y in gamma0}

            new_alpha = lat_types.join_env(new_alpha, alpha)
            new_gamma = lat_types.join_env(new_gamma, gamma)

            if new_alpha == alpha and new_gamma == gamma:
                break

        res = new_gamma, new_alpha, V.union(U0), Z.union(W0)
    else:
        print("don't know tag", tag, s)    
        assert(False)
    return res


def _compute_types_prog(gamma, alpha, V, Z, Xo, prog):
    return _compute_types_block(gamma, alpha, V, Z, Xo, prog)

def typecheck(gamma, alpha, V, Z, Xo, prog):
    """

    Args: 

    gamma (dict): typing environment. See lat_typing.py for more
    information. Gamma maps `regular` variables to their types. Types keep
    track of dependencies with initial values of variables, and final values
    of leaked variables. 

    Output variables are mapped to the `complement` singleton. 

    alpha (dict): typing environment for output variables. 

    V (set): set of output variables. 

    Z (set): set of regular variables 

    Xo: set of output or 'leaked' variables. 

    prog (ast, see parser.py): Program to be typed 

    Returns: (gamma', alpha', V', Z'). 
    gamma, alpha, V, Z, define new typing environment after the execution of
    prog. V' is V extended with regular variables (potentially) assigned in prog.
    Z' is Z extended with leaked variables (potentially) assigned in prog.
    """
    assert(prog[0] == 'PROG')
    return _compute_types_prog(gamma, alpha, V, Z, Xo, prog[1])