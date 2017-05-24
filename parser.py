""" Lexer and parser for the language.

This code serves as a reference for the language syntax and datatype
used in other modules.

ASML program (non-terminal fundefs)
{'data' : data, 'funs' : funs , 'main' : fun}

data is a list of (label, const) where const is an int or a float

funs is a list of functions of the form
{'label' : label, 'args' : args, 'code' : code}

args are lists of string

code and main are list of instructions (non-terminal exp)

('LET', id, expr)
('ANS', expr)

Expression are of the form
('NEW', ...)
('CALL', ...)
...

TODO(phil): pylint returns a lot of errors on this module... can be fixed 
without breaking ply conventions.
"""
import struct

reserved = {'while':'WHILE', 'if':'IF', 'then':'THEN', 'else':'ELSE' } 

tokens = ['INT', 'EQUAL', 'PLUS', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
          'ASSIGN', 'LE', 'GE', 'IDENT', 'SCOL'] + list(reserved.values())

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_EQUAL = r'='
t_LE = r'<='
t_ASSIGN = r'<-'
t_SCOL = r';'

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large ", t.value)
        t.value = 0
    return t

def t_IDENT(t):
    r'%?[a-z][a-zA-Z0-9_\.]*'
    t.type = reserved.get(t.value, 'IDENT') 
    print(t)
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    exit(1)

t_ignore = " \t\n\r"
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (('right', 'WHILE'), ('right', 'IF'))
names = {}
# def p_new(p):
#     'exp : NEW ident_or_imm'
#     p[0] = ('NEW', p[2])

# # TODO(phil) see if we really need this rule. I think ASML contains only idents
# # Although immediate could be propagated as an optimization in the backend.
# def p_ident_or_imm(p):
#     '''ident_or_imm : INT 
#                     | IDENT'''
#     p[0] = p[1]

# def p_neg(p):
#     'exp : NEG IDENT'
#     p[0] = ('NEG', p[2])

# def p_exp_call_closure(p):
#     'exp : CALL_CLOSURE IDENT formal_args'
#     p[0] = ('CALLCLOSURE', p[2], p[3])

def p_exp_int(p):
    'exp : INT'

def p_stm_affect(p):
    'stm : IDENT EQUAL exp SCOL'

def p_stm_while(p):
    'stm : WHILE LBRACE exp RBRACE'

def p_error(p):
    print("Syntax error in input near token", p)
    exit(1)

import ply.yacc as yacc

def parser():
    return yacc.yacc()