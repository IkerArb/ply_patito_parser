# -----------------------------------------------------------------------------
# patito.py
#
# Un simple parser para la clase de compiladores.
# Basado en el ejemplo de calc.py de la librería ply v 3.8
# -----------------------------------------------------------------------------

import sys

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'PROG','IF','THEN','ELSE','PROC','END','INT','FLOAT',
    'WHILE','READ','PRINT','VAR','NOTEQ','LTEQ','GTEQ',
    'CTES','COMMENT','ID','CTEED','CTEEB','CTEEH','CTEF',
    )

literals = ['=','+','-','*','/', '(',')','{','}',':',',',';','>','<']

# Tokens

t_PROG = r'PROG'
t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_PROC = r'PROC'
t_END = r'END'
t_INT = r'INT'
t_FLOAT = r'FLOAT'
t_WHILE = r'WHILE'
t_READ = r'READ'
t_PRINT = r'PRINT'
t_VAR = r'VAR'
t_NOTEQ = r'<>'
t_LTEQ = r'<='
t_GTEQ = r'>='

def t_CTES(t):
    r'\"[^\n"]*\"'
    return t

t_ignore = " \t\n"

def t_COMMENT(t):
    r'\/\*([^*]|\n|[*][^\/])*\*\/'
    return t

def t_ID(t):
    r'[A-Za-z]([_]?([a-zA-Z]|[0-9]))*'
    return t

def t_CTEED(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CTEEB(t):
    r'(0|1)+b'
    return t

def t_CTEEH(t):
    r'[0-9]+[a-fA-F0-9]*[hH]'
    return t

def t_CTEF(t):
    r'[0-9]+([eE]([+]|[-])?|[.][0-9]+[eE]([+]|[-])?|[.])[0-9]+'
    t.value = float(t.value)
    return t



def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
