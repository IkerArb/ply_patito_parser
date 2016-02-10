# -----------------------------------------------------------------------------
# patito.py
#
# Un simple parser para la clase de compiladores.
# Basado en el ejemplo de calc.py de la libreria ply v 3.8
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

def t_IF(t):
    r'IF'
    return t

def t_THEN(t):
    r'THEN'
    return t

def t_ELSE(t):
    r'ELSE'
    return t

def t_PROC(t):
    r'PROC'
    return t

def t_END(t):
    r'END'
    return t

def t_INT(t):
    r'INT'
    return t

def t_FLOAT(t):
    r'FLOAT'
    return t

def t_WHILE(t):
    r'WHILE'
    return t

def t_READ(t):
    r'READ'
    return t

def t_PRINT(t):
    r'PRINT'
    return t

def t_VAR(t):
    r'VAR'
    return t

def t_NOTEQ(t):
    r'<>'
    return t

def t_LTEQ(t):
    r'<='
    return t

def t_GTEQ(t):
    r'>='
    return t

def t_PROG(t):
    r'PROG'
    return t

def t_CTEF(t):
    r'[0-9]+([eE]([+]|[-])?|[.][0-9]+[eE]([+]|[-])?|[.])[0-9]+'
    t.value = float(t.value)
    return t

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

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

def p_programa(p):
    'programa : PROG ID ";" v bloque'
    print('done with file!\n')
    pass

def p_v(p):
    ''' v : empty
          | vars'''
    pass

def p_vars(p):
    'vars : VAR a'
    pass

def p_a(p):
    'a : b ":" tipo ";" f'
    pass

def p_f(p):
    ''' f : empty
          | a'''
    pass

def p_b(p):
    'b : ID c'
    pass

def p_c(p):
    '''c : empty
         | "," b '''
    pass

def p_tipo(p):
    '''tipo : INT
            | FLOAT'''
    pass

def p_bloque(p):
    'bloque : "{" d "}"'
    print('bloque codificado exitosamente\n')
    pass

def p_d(p):
    '''d : empty
         | estatuto d'''
    pass

def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | escritura'''
    pass

def p_asignacion(p):
    'asignacion : ID "=" expresion ";"'
    print('se asigno la variable '+ p[1])
    pass

def p_expresion(p):
    'expresion : exp i'
    pass

def p_i(p):
    '''i : empty
         | ">" exp
         | "<" exp
         | NOTEQ exp'''
    pass

def p_escritura(p):
    'escritura : PRINT "(" g ")" ";"'
    pass

def p_g(p):
    '''g : expresion h
         | CTES h'''
    pass

def p_h(p):
    '''h : empty
        | "," g'''
    pass

def p_exp(p):
    'exp : termino k'
    pass

def p_k(p):
    '''k : empty
         | "+" exp
         | "-" exp'''
    pass

def p_factor(p):
    '''factor : "(" expresion ")"
              | m varcte'''
    pass

def p_m(p):
    '''m : empty
         | "+"
         | "-"'''
    pass

def p_condicion(p):
    'condicion : IF "(" expresion ")" bloque j ";"'
    pass

def p_j(p):
    '''j : empty
         | ELSE bloque'''
    pass

def p_termino(p):
    'termino : factor l'
    pass

def p_l(p):
    '''l : empty
         | "*" termino
         | "/" termino'''
    pass

def p_varcte(p):
    '''varcte : ID
              | CTEED
              | CTEF'''
    pass

def p_empty(t):
    'empty : '
    pass

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
