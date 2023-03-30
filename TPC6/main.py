import sys
from ply.lex import lex

tokens = [
    'LB', 'RB', 'LC', 'RC', 'LP', 'RP', 
    'SUM', 'SUB', 'MUL', 'DIV', 'ASSIGN', 'RANGE', 'MOD',
    'EQUAL', 'DIF', 'NOT', 'LESS', 'GREATER', 'LESS_EQ', 'GREATER_EQ', 'IN',
    'VAR', 'NUMBER', 'SEMICOLON', 'COMMA', 'COMMENT',
    'IF', 'ELSE', 'ELIF',
    'WHILE', 'FOR', 'FOREACH',
    'TYPE',
    'FUNCTION', 'PROGRAM', 'PRINT'
]

t_ignore = f'\t\r'

#parêntesis
t_LB = r'\['
t_RB = r'\]'
t_LC = r'{'
t_RC = r'}'
t_LP = r'\('
t_RP = r'\)'

#ops
t_SUM = r'\+'
t_SUB = r'-'
t_MUL = r'\*' 
t_DIV = r'/'

def t_ASSIGN(t):
    r'='
    return t 

t_RANGE = r'\.\.(?=\d+)'

t_MOD = r'%'

#cond 
t_EQUAL = r'=='
t_DIF = r'!='
t_NOT = r'!'
t_LESS = r'<'
t_GREATER = r'>'
t_LESS_EQ = r'<='
t_GREATER_EQ = r'>='
t_IN = r'in'

#conditionals
def t_IF(t):
    r'if '
    return t

def t_ELSE(t):
    r'else'
    return t

def t_ELIF(t):
    r'elif'
    return t
    

#loops
def t_WHILE(t):
    r'while'
    return t 
    
def t_FOR(t):
    r'for'
    return t
    
def t_FOREACH(t):
    r'foreach'
    return t

#types
def t_TYPE(t):
    r'int|double|string|char|float'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_PROGRAM(t):
    r'program'
    return t

def t_PRINT(t):
    r'print'
    return t

#id
def t_VAR(t):
    r'[a-z_]\w*'
    return t 

#number
def t_NUMBER(t):
    r'-?\d+'
    return t

t_SEMICOLON = r';'
t_COMMA = r','


#comments
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)' 
    return t

def t_comment(t):
    r'//.*'

def t_ANY_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_ANY_space(t):
    r'\s'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


fileName = sys.argv[1]
print("Opening " + fileName)
file = open(fileName).read()
lexer = lex()
lexer.input(file)
toks = []
for tok in lexer:
    toks.append(tok)
print("Tamanho da lista: " + str(len(toks))) 
print("Tokens: ")
for t in toks:
    print(t)