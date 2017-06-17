""" Lexer and parser for the language.

Concrete syntax is given by the following grammar.

    prog ::= block opt_return
    opt_return ::= epsilon
               |   RETURN SCOL 
               |   RETURN indents SCOL
    idents :: IDENT
           |  IDENT, idents
    block ::= stm block
    block ::= stm
    stm ::= IDENT ASSIGN exp SCOL
    stm ::= WHILE LPAREN exp RPAREN LBRACE block RBRACE
    stm ::= IF LPAREN exp RPAREN LBRACE block RBRACE ELSE LBRACE block RBRACE
    stm ::= SKIP SCOL
    exp ::= INT
    exp ::= IDENT
    exp ::= exp PLUS exp
        |   exp TIMES exp
        |   exp EQUAL exp
    exp ::= LPAREN exp RPAREN

Abstract syntax is defined as:

PROG ::= ('PROG', BLOCK, RETURNED_VARS) 
RETURNED_VARS :: = [ IDENT, ..., IDENT ]
BLOCK ::= [ STM, ..., STM ]
STM ::= ('IF', EXP, BLOCK, BLOCK)
     |  ('WHILE', EXP, EXP)
     |  ('ASSIGN', IDENT, EXP)
     |  ('SKIP' , None)
EXP ::= ('INT', INT)
     |  ('IDENT', IDENT)
     |  ('BINOP', BINOP, EXP, EXP)
BINOP ::= 'PLUS' | 'TIMES' | 'EQUAl'

"""

import struct
import sys

reserved = {'while':'WHILE', 'if':'IF', 'else':'ELSE', 'skip' :'SKIP',
            'return': 'RETURN' } 

tokens = ['INT', 'EQUAL', 'PLUS', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
          'ASSIGN', 'IDENT', 'COMMA', 'SCOL', 'TIMES'] + list(reserved.values())

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_SCOL = r'\;'
t_COMMA = r'\,'

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
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    exit(1)

t_ignore = " \t\n\r"
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (('left', 'EQUAL'), ('left', 'PLUS'), ('left', 'TIMES'))
names = {}

def p_prog(p):
    'prog : block opt_return'
    p[0] = ('PROG', p[1], p[2])

def p_opt_return_empty(p):
    'opt_return :'
    p[0] = []

def p_opt_return_void(p):
    'opt_return : RETURN SCOL'
    p[0] = []

def p_opt_return_idents(p):
    'opt_return : RETURN idents SCOL'
    p[0] = p[2] 

def p_idents_one(p):
    'idents : IDENT'
    p[0] = [p[1]]

def p_idents_seq(p):
    'idents : IDENT COMMA idents'
    p[0] = [p[1]] + p[3]

def p_block_seq(p):
    'block : stm block'
    p[0] = ('BLOCK', [p[1]] + p[2][1])

def p_block_base(p):
    'block : stm'
    p[0] = ('BLOCK', [p[1]]) 

def p_stm_assign(p):
    'stm : IDENT ASSIGN exp SCOL'
    p[0] = ('ASSIGN', p[1], p[3])

def p_stm_while(p):
    'stm : WHILE LPAREN exp RPAREN LBRACE block RBRACE'
    p[0] = ('WHILE', p[3], p[6])

def p_stm_ite(p):
    'stm : IF LPAREN exp RPAREN LBRACE block RBRACE ELSE LBRACE block RBRACE'
    p[0] = ('IF', p[3], p[6], p[10]) 

def p_stm_skip(p):
    'stm : SKIP SCOL'
    p[0] = ('SKIP', None) # tuples must have at least 2 elements

def p_exp_int(p):
    'exp : INT'
    p[0] = ('INT', p[1])

def p_exp_id(p):
    'exp : IDENT'
    p[0] = ('IDENT', p[1])

def p_exp_binop(p):
    '''exp : exp PLUS exp
           | exp TIMES exp
           | exp EQUAL exp'''
    p[0] = ('BINOP', p[2], p[1], p[3])

def p_exp_paren(p):
    'exp : LPAREN exp RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input near token", p)
    exit(1)

import ply.yacc as yacc

def parser():
    return yacc.yacc()
