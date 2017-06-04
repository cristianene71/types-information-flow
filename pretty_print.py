""" Pretty print a program
    Simple recursive functions following the abstract syntax grammar.
"""

import sys

def _exp_to_string(e):
    tag = e[0]
    if tag == 'INT':
        res = str(e[1])
    elif tag == 'IDENT':
        res = e[1]
    elif tag == 'BINOP':
        res = '(' + _exp_to_string(e[2]) + e[1] + _exp_to_string(e[3]) + ')'
    else:
        print("don't know tag", tag, e)
        assert(False)
    return res

def _stm_to_string(p, indent):
    tag = p[0]
    if tag == 'AFFECT':
        res = indent + p[1] + ' = ' + _exp_to_string(p[2]) + ';'
    elif tag == 'WHILE':
        res = indent + 'while (' + _exp_to_string(p[1])  + ') {\n' + _block_to_string(p[2], indent + '  ') + indent + '}'
    elif tag == 'IF':
        res = indent + 'if (' + _exp_to_string(p[1]) + ') {\n' + _block_to_string(p[2], indent + '  ') + indent + '} else {\n' + _block_to_string(p[3], indent + '  ') + indent + '}'
    elif tag == 'SKIP':
        res = indent + 'skip;'
    else:
        print("don't know tag", tag, p)
        assert(False)
    return res

def _block_to_string(b, indent):
    assert(b[0] == 'BLOCK')
    res = ""
    for s in b[1]:
        res = res + _stm_to_string(s, indent) + '\n'
    return res

def print_prog(p):
    assert(p[0] == 'PROG')
    sys.stdout.write(_block_to_string(p[1], ""))
    print('return ', ",".join(p[2]), ';', sep = "")





