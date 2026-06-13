import ply.lex as lex

tokens = (
#-- Dhamar Patiño
    'IDENTIFIER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MODULO',

    'EQUALS',
    'NOT_EQUALS',

    'GREATER_THAN',
    'LESS_THAN',
    'GREATER_EQUAL',
    'LESS_EQUAL',

    'AND',
    'OR',
    'NOT',

    'ASSIGN',

    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'TIMES_ASSIGN',
    'DIVIDE_ASSIGN',

    'COMMENT_SINGLE',
    'COMMENT_MULTI'
#-- Dhamar Patiño
)

#-- Dhamar Patiño
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'

t_EQUALS = r'=='
t_NOT_EQUALS = r'!='

t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='

t_GREATER_THAN = r'>'
t_LESS_THAN = r'<'

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

t_ASSIGN = r'='

t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='

# Variables
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Ignorar espacios
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)

def t_COMMENT_SINGLE(t):
    r'//.*'

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#-- Dhamar Patiño

lexer = lex.lex()




