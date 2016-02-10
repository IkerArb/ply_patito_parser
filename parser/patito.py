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

def p_programa(p):
    'programa : PROG ID ";" v bloque'
    print('done with file!\n')

def p_v(p):
    ''' v : empty
          | vars'''

def p_vars(p):
    'vars : VAR a'

def p_a(p):
    'a : b ":" tipo ";" f'

def p_f(p):
    ''' f : empty
          | a'''

def p_b(p):
    'b : ID c'

def p_c(p):
    '''c : empty
         | "," b '''

def p_tipo(p):
    '''tipo : INT
            | FLOAT'''

def p_bloque(p):
    'bloque : "{" d "}"'
    print('bloque codificado exitosamente\n')

def p_d(p):
    '''d : empty
         | estatuto d'''

def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | escritura'''

def p_asignacion(p):
    'asignacion : ID "=" expresion ";"
    print('se asignó la variable '+ p[1])

def p_expresion(p):
    'expresion : exp i'

def p_i(p):
    '''i : empty
         | ">" exp
         | "<" exp
         | NOTEQ exp'''

def p_escritura(p):
    'escritura : PRINT "(" g ")" ";"'

def p_g(p):
    '''g : expresion h
         | CTES h'''

def p_h(p):
    '''h: empty
        | "," g'''

def p_exp(p):
    'exp : termino k'

def p_k(p):
    '''k : empty
         | "+" exp
         | "-" exp'''

def p_factor(p):
    '''factor : "(" expresion ")"
              | m varcte'''

def p_m(p):
    '''m : empty
         | "+"
         | "-"'''

def p_condicion(p):
    'condicion : IF "(" expresion ")" bloque j ";"'

def p_j(p):
    '''j : empty
         | ELSE bloque'''

def p_termino(p):
    'termino : factor l'

def p_l(p):
    '''l : empty
         | "*" termino
         | "/" termino'''

def p_varcte(p):
    '''varcte : ID
              | CTEED
              | CTEF'''

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
