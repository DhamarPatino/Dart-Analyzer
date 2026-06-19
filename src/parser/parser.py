import ply.yacc as yacc
from src.lexer.lexer import tokens

errores_sintacticos = []
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
              | funcion_retorno
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
        mensaje = f"Error sintáctico en '{p.value}' línea {p.lineno}"
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
              | llamada_funcion
    '''

def p_expresion_operaciones(p):
    '''
    expresion : expresion PLUS expresion
              | expresion MINUS expresion
              | expresion MULTIPLY expresion
              | expresion DIVIDE expresion
              | expresion MODULO expresion
    '''
    pass

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

def p_parametro(p):
    '''
    parametro : tipo IDENTIFIER
    '''
    pass

def p_parametros(p):
    '''
    parametros : parametro
               | parametro COMMA parametros
    '''
    pass

def p_retorno(p):
    '''
    retorno : RETURN expresion SEMICOLON
    '''
    pass

def p_funcion_retorno(p):
    '''
    funcion_retorno : tipo IDENTIFIER LPAREN parametros RPAREN LBRACE retorno RBRACE
    '''
    pass

def p_argumentos(p):
    '''
    argumentos : expresion
               | expresion COMMA argumentos
    '''
    pass

def p_llamada_funcion(p):
    '''
    llamada_funcion : IDENTIFIER LPAREN argumentos RPAREN
    '''
    pass


# -- Dhamar Patiño

parser = yacc.yacc()



