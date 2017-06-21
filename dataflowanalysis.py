""" Generate, print and solve dataflow equations. To each node 'n'
 we associate a variable 'Xn_out' that represents the set of variables
 used after exiting this node.
"""

def in_var(x):
  return x + '_in'

def out_var(x):
  return 'X' + x + '_out'

def print_equations(equations):
  print('--- equations')
  for var in equations:
    use, succ = equations[var]
    succ_names = " U ".join(succ)
    if succ_names:
      if use:
        print(var, '=', set(use), 'U', succ_names)
      else:
        print(var, '=', succ_names)
    else:
      if use:
        print(var, '=', set(use))
      else:
        print(var, '= {}')

def print_sol(sol):
  print('--- solution')
  for x in sol:
    print(x, '=', sol[x] if sol[x] else '{}') 

def gen_equations(nodes):
  res = {}
  for n in nodes:
    succ_names = [out_var(x.name) for x in n.succ]
    res[out_var(n.name)] = (n.uses, succ_names)
  return res

def apply_equations(equations, current_sol):
  for x in current_sol:
    use, succs = equations[x]
    cur_x = current_sol[x]
    cur_x = cur_x.union(use)
    for y in succs:
      cur_x = cur_x.union(current_sol[y])
    current_sol[x] = cur_x

def solve_equations(equations):
  current_sol = { x : set() for x in equations }
  while True:
    old_sol = current_sol.copy()
    apply_equations(equations, current_sol)
    if (old_sol == current_sol):
      break
  return current_sol