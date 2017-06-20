import ast
import free_vars

def gen_name():
    for x in "abcdefghijklmnopqrstuvwxyz":
      yield x

    i = 0
    while True:
        yield 'node_' + str(i)
        i = i + 1

gen_name = gen_name()

nodes = []   # initially empty set of nodes, put in a static field of nodes ?

class Node:
  # TODO(phil) see how (and why) to use annotations like at_property

  def __init__(self):
    # TODO(Phil) check if there is a better way to define a static field
    global nodes
    self.name = next(gen_name)
    self.code = None
    self.succ = []
    self.defs = []
    self.uses = []
    nodes = nodes + [self]

  def set_code(self, code):
    self.code = code 
    if ast.is_expr(code):
      self.uses = list(free_vars.free_vars_exp(code))
    elif code[0] == 'ASSIGN':
      self.defs = [code[1]]
      self.uses = list(free_vars.free_vars_exp(code[2]))
    else:
      assert(code[0] == 'SKIP')

  def add_succ(self, n):
    self.succ = self.succ + [n]

def make_cfg_block(b, initial_node, exit_node):
  assert(b[0] == 'BLOCK')
  for i in b[1]:
    if i[0] in {'SKIP', 'ASSIGN'}:
      simple_instr_node = Node()
      simple_instr_node.set_code(i)
      initial_node.add_succ(simple_instr_node)
      initial_node = simple_instr_node
    elif i[0] == 'IF':
      expr = i[1]
      left = i[2]
      right = i[3]
      cond_node = Node()
      cond_node.set_code(expr)
      initial_node.add_succ(cond_node)
      exit_if = Node()
      make_cfg_block(left, cond_node, exit_if)
      make_cfg_block(right, cond_node, exit_if)
      initial_node = exit_if
    elif i[0] == 'WHILE':
      expr = i[1]
      block = i[2]
      cond_node = Node()
      cond_node.set_code(expr)
      initial_node.add_succ(cond_node)
      exit_while = Node()
      make_cfg_block(block, cond_node, cond_node)
      cond_node.add_succ(exit_while)
      initial_node = exit_while
    else:
      print("don't know tag", tag, p)
      assert(False)
  initial_node.add_succ(exit_node)

def make_cfg(p):
  initial_node = Node() 
  exit_node = Node() 
  make_cfg_block(p[1], initial_node, exit_node)
  return nodes

def print_dot(nodes, os):
  os.write('digraph cfg {\n')
  for n in nodes:
    if n.code:
      name = n.name
      defs = str(n.defs)
      uses = str(n.uses) 
      code = ast.simple_stm_or_expr_to_string(n.code)
      os.write('\t' + name + '[ label = "' + code + '\n def = ' + defs + '\n use = ' + uses + '\n"' + "]\n")
  for n in nodes:
      for s in n.succ:
        os.write('\t' + n.name + '->' + s.name + ';\n')
  os.write('}\n')
