""" Solve liveness equations.
"""

def _live_out_var(x):
  """ Generate variable name from node name 
  Only used for display purpose.
  """
  return 'LIVE_' + x + '_out'

def print_sol(sol):
  print('--- solution')
  for x in sol:
    print(_live_out_var(x), '=', sol[x] if sol[x] else '{}') 

def _apply_liveness_equations(graph, current_sol):
  """ apply liveness equations (from the graph) to a current solution """
  for node in graph:
    res = set()
    for succ in node.succ:
      res = res.union(set(succ.uses).union(current_sol[succ.name]).difference(succ.defs))
    current_sol[node.name] = res

def compute_liveness(g):
  """ apply liveness equations until a fixpoint is reached """
  current_sol = { n.name : set() for n in g }
  while True:
    old_sol = current_sol.copy()
    _apply_liveness_equations(g, current_sol)
    if old_sol == current_sol:
       break
  return current_sol

def check_var_not_used(g, sol):
  """ generate warning for variables defined at a node that are not 'live-out'
  """
  for n in g:
    live_out = sol[n.name]
    for i in n.defs:
      if i not in live_out:
        print('WARNING variable', i, 'in block', n.name, 'defined but not used')

