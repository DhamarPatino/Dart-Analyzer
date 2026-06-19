import ply.yacc as yacc
from src.lexer.lexer import tokens

# -- Dhamar Patiño
def p_programa(p):
    '''
    programa : lista_sentencias
    '''
    pass

def p_lista_sentencias(p):
    '''
    lista_sentencias : sentencia
                     | lista_sentencias sentencia
    '''
    pass
    
def p_sentencia(p):
    '''
    sentencia : declaracion
              | asignacion
              | sentencia_if
              | impresion
              | declaracion_lista

    '''
    pass

def p_declaracion(p):
    '''
    declaracion : tipo IDENTIFIER ASSIGN expresion SEMICOLON
                | VAR IDENTIFIER ASSIGN expresion SEMICOLON
    '''
    pass

def p_error(p):
    if p:
        print(f"Error sintáctico en '{p.value}'")
    else:
        print("Error sintáctico al final del archivo")

def p_tipo(p):
    '''
    tipo : INT_TYPE
         | DOUBLE_TYPE
         | STRING_TYPE
         | BOOL_TYPE
    '''

def p_expresion(p):
    '''
    expresion : INTEGER_LITERAL
              | DOUBLE_LITERAL
              | STRING_LITERAL
              | TRUE
              | FALSE
              | IDENTIFIER
    '''

def p_asignacion(p):
    '''
    asignacion : IDENTIFIER ASSIGN expresion SEMICOLON
    '''


def p_comparacion(p):
    '''
    comparacion : expresion GREATER_THAN expresion
                | expresion LESS_THAN expresion
                | expresion GREATER_EQUAL expresion
                | expresion LESS_EQUAL expresion
                | expresion EQUALS expresion
                | expresion NOT_EQUALS expresion
    '''
    pass

def p_booleano(p):
    '''
    booleano : comparacion
             | booleano AND comparacion
             | booleano OR comparacion
             | NOT booleano
    '''
    pass

def p_bloque(p):
    '''
    bloque : LBRACE lista_sentencias RBRACE
    '''
    pass

def p_sentencia_if(p):
    '''
    sentencia_if : IF LPAREN booleano RPAREN bloque
                 | IF LPAREN booleano RPAREN bloque ELSE bloque
    '''
    pass

def p_impresion(p):
    '''
    impresion : IDENTIFIER LPAREN expresion RPAREN SEMICOLON
    '''
    pass

def p_elementos(p):
    '''
    elementos : expresion
              | expresion COMMA elementos
    '''
    pass

def p_lista(p):
    '''
    lista : LBRACKET elementos RBRACKET
    '''
    pass

def p_declaracion_lista(p):
    '''
    declaracion_lista : LIST_TYPE LESS_THAN tipo GREATER_THAN IDENTIFIER ASSIGN lista SEMICOLON
    '''
    pass

# -- Dhamar Patiño

parser = yacc.yacc()



