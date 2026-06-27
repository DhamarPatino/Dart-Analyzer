import ply.yacc as yacc
from src.lexer.lexer import tokens
from src.semantic.semantic import (tabla_simbolos, errores_semanticos,
    registrar_variable, verificar_variable, obtener_tipo, verificar_asignacion
)

errores_sintacticos = []


# REGLAS GENERALES DEL PROGRAMA

#-- Dhamar Patiño
def p_programa(p):
    """
    programa : lista_importaciones lista_elementos_programa
             | lista_importaciones
             | lista_elementos_programa
             | vacio
    """
    pass


def p_lista_importaciones(p):
    """
    lista_importaciones : importacion
                        | lista_importaciones importacion
    """
    pass


def p_lista_elementos_programa(p):
    """
    lista_elementos_programa : elemento_programa
                             | lista_elementos_programa elemento_programa
    """
    pass


def p_elemento_programa(p):
    """
    elemento_programa : declaracion
                      | funcion_clasica
                      | funcion_flecha
    """
    pass


def p_lista_sentencias_opcional(p):
    """
    lista_sentencias_opcional : lista_sentencias
                              | vacio
    """
    pass


def p_lista_sentencias(p):
    """
    lista_sentencias : sentencia
                     | lista_sentencias sentencia
    """
    pass


def p_sentencia(p):
    """
    sentencia : declaracion
              | asignacion
              | impresion
              | sentencia_if
              | sentencia_for
              | retorno
              | llamada_funcion SEMICOLON
              | llamada_metodo SEMICOLON
    """
    pass
#-- Dhamar Patiño
#--Cristina Pihuave
# RECUPERACIÓN DE ERRORES SINTÁCTICOS

#-- Cristina Pihuave
def p_elemento_programa_error(p):
    """
    elemento_programa : error SEMICOLON
    """
    pass


def p_sentencia_error(p):
    """
    sentencia : error SEMICOLON
    """
    pass
#-- Cristina Pihuave


# DECLARACIÓN DE VARIABLES


# TIPOS DE DATOS PRIMITIVOS Y LIST

#-- Dhamar Patiño
def p_tipo_primitivo(p):
    """
    tipo : INT_TYPE
         | DOUBLE_TYPE
         | STRING_TYPE
         | BOOL_TYPE
    """
    p[0] = p[1]


def p_tipo_lista(p):
    """
    tipo : LIST_TYPE LESS_THAN tipo GREATER_THAN
    """
    p[0] = "List"
#-- Dhamar Patiño


# TIPO DE DATO MAP Y TIPO OPCIONAL

#-- Cristina Pihuave
def p_tipo_mapa(p):
    """
    tipo : MAP_TYPE LESS_THAN tipo COMA tipo GREATER_THAN
    """
    p[0] = "Map"


def p_tipo_opcional(p):
    """
    tipo_opcional : tipo
                  | vacio
    """
    if len(p)==2:
        p[0]=p[1]
#-- Cristina Pihuave


# DECLARACIÓN CON TIPO EXPLÍCITO

#-- Dhamar Patiño
def p_declaracion_tipo_explicito(p):
    """
    declaracion : tipo IDENTIFIER ASSIGN expresion SEMICOLON
    """
    tabla_simbolos[p[2]] = p[1]
    registrar_variable(
        p[2],
        p[1]
    )

    tipo_valor = obtener_tipo(p[4])

    verificar_asignacion(p[2], tipo_valor)
#-- Dhamar Patiño


# DECLARACIÓN CON VAR, FINAL Y CONST

#-- Cristina Pihuave
def p_declaracion_inferencia_inmutable(p):
    """
    declaracion : VAR IDENTIFIER ASSIGN expresion SEMICOLON
                | FINAL tipo_opcional IDENTIFIER ASSIGN expresion SEMICOLON
                | CONST tipo_opcional IDENTIFIER ASSIGN expresion SEMICOLON
    """
    if p.slice[1].type == "VAR":

        tipo = obtener_tipo(p[4])

        registrar_variable(
            p[2],
            tipo
        )

    else:

        registrar_variable(
            p[3],
            p[2]
        )

        tipo_valor = obtener_tipo(p[5])

        verificar_asignacion(
            p[3],
            tipo_valor
        )
#-- Cristina Pihuave


# ASIGNACIONES

#-- Dhamar Patiño
def p_asignacion(p):
    """
    asignacion : IDENTIFIER ASSIGN expresion SEMICOLON
               | IDENTIFIER PLUS_ASSIGN expresion SEMICOLON
               | IDENTIFIER MINUS_ASSIGN expresion SEMICOLON
               | IDENTIFIER TIMES_ASSIGN expresion SEMICOLON
               | IDENTIFIER DIVIDE_ASSIGN expresion SEMICOLON
               | acceso_indice ASSIGN expresion SEMICOLON
               | acceso_indice PLUS_ASSIGN expresion SEMICOLON
               | acceso_indice MINUS_ASSIGN expresion SEMICOLON
               | acceso_indice TIMES_ASSIGN expresion SEMICOLON
               | acceso_indice DIVIDE_ASSIGN expresion SEMICOLON
    """
    
    verificar_variable(p[1])
    tipo_valor = obtener_tipo(p[3])
    verificar_asignacion(p[1], tipo_valor)
#-- Dhamar Patiño


# EXPRESIONES ARITMÉTICAS

#-- Cristina Pihuave
def p_expresion_aditiva(p):
    """
    expresion_aditiva : expresion_aditiva PLUS expresion_multiplicativa
                      | expresion_aditiva MINUS expresion_multiplicativa
                      | expresion_multiplicativa
    """
    if len(p) == 2:
        p[0]=p[1]

    else:
        p[0]=p[1]


def p_expresion_multiplicativa(p):
    """
    expresion_multiplicativa : expresion_multiplicativa MULTIPLY expresion_unaria
                             | expresion_multiplicativa DIVIDE expresion_unaria
                             | expresion_multiplicativa MODULO expresion_unaria
                             | expresion_unaria
    """
    if len(p)==2:
        p[0]=p[1]

    else:
        p[0]=p[1]
#-- Cristina Pihuave


# EXPRESIONES BOOLEANAS

#-- Dhamar Patiño
def p_expresion(p):
    """
    expresion : expresion_or
    """
    p[0] = p[1]


def p_expresion_or(p):
    """
    expresion_or : expresion_or OR expresion_and
                 | expresion_and
    """
    if len(p)==2:
        p[0]=p[1]

    else:
        p[0]=p[1]


def p_expresion_and(p):
    """
    expresion_and : expresion_and AND expresion_igualdad
                  | expresion_igualdad
    """
    if len(p)==2:
        p[0]=p[1]

    else:
        p[0]=p[1]


def p_expresion_igualdad(p):
    """
    expresion_igualdad : expresion_relacional
                       | expresion_relacional EQUALS expresion_relacional
                       | expresion_relacional NOT_EQUALS expresion_relacional
    """
    if len(p)==2:
        p[0]=p[1]

    else:
        p[0]=p[1]


def p_expresion_relacional(p):
    """
    expresion_relacional : expresion_aditiva
                         | expresion_aditiva GREATER_THAN expresion_aditiva
                         | expresion_aditiva LESS_THAN expresion_aditiva
                         | expresion_aditiva GREATER_EQUAL expresion_aditiva
                         | expresion_aditiva LESS_EQUAL expresion_aditiva
    """
    if len(p)==2:
        p[0]=p[1]

    else:
        p[0]=p[1]


def p_expresion_unaria(p):
    """
    expresion_unaria : NOT expresion_unaria
                     | MINUS expresion_unaria
                     | factor
    """
    if len(p)==2:
        p[0]=p[1]

    else:
        p[0]=p[1]


def p_factor(p):
    """
    factor : INTEGER_LITERAL
           | DOUBLE_LITERAL
           | STRING_LITERAL
           | TRUE
           | FALSE
           | IDENTIFIER
           | llamada_funcion
           | llamada_metodo
           | ingreso_datos
           | acceso_indice
           | lista
           | mapa
           | LPAREN expresion RPAREN
    """
    
    
    if p.slice[1].type == "IDENTIFIER":
        verificar_variable(p[1])

    if p.slice[1].type == "TRUE":
        p[0] = True

    elif p.slice[1].type == "FALSE":
        p[0] = False

    else:
        p[0] = p[1]
#-- Dhamar Patiño


# ESTRUCTURAS DE CONTROL


# ESTRUCTURA IF-ELSE

#-- Dhamar Patiño
def p_bloque(p):
    """
    bloque : LLLAVE lista_sentencias_opcional RLLAVE
    """
    pass


def p_sentencia_if(p):
    """
    sentencia_if : IF LPAREN expresion RPAREN bloque
                 | IF LPAREN expresion RPAREN bloque ELSE bloque
                 | IF LPAREN expresion RPAREN bloque ELSE sentencia_if
    """
    pass
#-- Dhamar Patiño


# ESTRUCTURA FOR

#-- Cristina Pihuave
def p_sentencia_for(p):
    """
    sentencia_for : FOR LPAREN inicializacion_for expresion SEMICOLON actualizacion_for RPAREN bloque
    """
    pass


def p_inicializacion_for(p):
    """
    inicializacion_for : tipo IDENTIFIER ASSIGN expresion SEMICOLON
                       | VAR IDENTIFIER ASSIGN expresion SEMICOLON
                       | IDENTIFIER ASSIGN expresion SEMICOLON
    """
    if p.slice[1].type == "IDENTIFIER":
        verificar_variable(p[1])

    else:
        registrar_variable(
            p[2],
            p[1]
        )


def p_actualizacion_for(p):
    """
    actualizacion_for : IDENTIFIER INCREMENT
                      | IDENTIFIER PLUS_ASSIGN expresion
                      | IDENTIFIER MINUS_ASSIGN expresion
                      | IDENTIFIER TIMES_ASSIGN expresion
                      | IDENTIFIER DIVIDE_ASSIGN expresion
    """
    pass
#-- Cristina Pihuave


# ESTRUCTURAS DE DATOS


# ESTRUCTURA DE DATOS LIST

#-- Dhamar Patiño
def p_lista(p):
    """
    lista : LCORCHETE elementos_lista_opcionales RCORCHETE
    """
    pass


def p_elementos_lista_opcionales(p):
    """
    elementos_lista_opcionales : elementos_lista
                               | elementos_lista COMA
                               | vacio
    """
    pass


def p_elementos_lista(p):
    """
    elementos_lista : expresion
                    | elementos_lista COMA expresion
    """
    pass
#-- Dhamar Patiño


# ESTRUCTURA DE DATOS MAP

#-- Cristina Pihuave
def p_mapa(p):
    """
    mapa : LLLAVE pares_mapa_opcionales RLLAVE
    """
    pass


def p_pares_mapa_opcionales(p):
    """
    pares_mapa_opcionales : pares_mapa
                          | pares_mapa COMA
                          | vacio
    """
    pass


def p_pares_mapa(p):
    """
    pares_mapa : par_mapa
               | pares_mapa COMA par_mapa
    """
    pass


def p_par_mapa(p):
    """
    par_mapa : expresion COLON expresion
    """
    pass


def p_acceso_indice(p):
    """
    acceso_indice : IDENTIFIER LCORCHETE expresion RCORCHETE
                | IDENTIFIER LCORCHETE expresion RCORCHETE NOT
    """
    p[0] = p[1]
#-- Cristina Pihuave


# DECLARACIONES DE FUNCIONES


# FUNCIÓN CLÁSICA CON RETORNO O VOID

#-- Dhamar Patiño
def p_funcion_clasica(p):
    """
    funcion_clasica : tipo IDENTIFIER LPAREN parametros_opcionales RPAREN bloque
                    | VOID IDENTIFIER LPAREN parametros_opcionales RPAREN bloque
    """
    pass


def p_retorno(p):
    """
    retorno : RETURN expresion SEMICOLON
            | RETURN SEMICOLON
    """
    pass
#-- Dhamar Patiño


# FUNCIÓN FLECHA

#-- Cristina Pihuave
def p_funcion_flecha(p):
    """
    funcion_flecha : tipo IDENTIFIER LPAREN parametros_opcionales RPAREN ARROW expresion SEMICOLON
    """
    pass
#-- Cristina Pihuave


# PARÁMETROS

#-- Dhamar Patiño
def p_parametro(p):
    """
    parametro : tipo IDENTIFIER
    """
    registrar_variable(
        p[2],
        p[1]
    )


def p_parametros(p):
    """
    parametros : parametro
               | parametros COMA parametro
    """
    pass


def p_parametros_opcionales(p):
    """
    parametros_opcionales : parametros
                          | vacio
    """
    pass
#-- Dhamar Patiño


# LLAMADAS DE FUNCIONES Y ARGUMENTOS

#-- Dhamar Patiño
def p_llamada_funcion(p):
    """
    llamada_funcion : IDENTIFIER LPAREN argumentos_opcionales RPAREN
    """
    p[0] = p[1]


def p_argumentos_opcionales(p):
    """
    argumentos_opcionales : argumentos
                          | vacio
    """
    pass


def p_argumentos(p):
    """
    argumentos : expresion
               | argumentos COMA expresion
    """
    pass
#-- Dhamar Patiño


# LLAMADAS DE MÉTODOS

#-- Cristina Pihuave
def p_llamada_metodo(p):
    """
    llamada_metodo : IDENTIFIER PUNTO IDENTIFIER LPAREN argumentos_opcionales RPAREN
    """
    p[0] = p[1]
#-- Cristina Pihuave


# IMPRESIÓN Y SOLICITUD DE DATOS


# IMPRESIÓN

#-- Dhamar Patiño
def p_impresion(p):
    """
    impresion : PRINT LPAREN expresion RPAREN SEMICOLON
    """
    pass
#-- Dhamar Patiño


# INGRESO DE DATOS

#-- Dhamar Patiño
def p_ingreso_datos(p):
    """
    ingreso_datos : STDIN PUNTO READ_LINE_SYNC LPAREN RPAREN
                  | STDIN PUNTO READ_LINE_SYNC LPAREN RPAREN NOT
    """
    p[0] = ""
#-- Dhamar Patiño


# IMPORTACIÓN DE LA BIBLIOTECA

#-- Dhamar Patiño
def p_importacion(p):
    """
    importacion : IMPORT STRING_LITERAL SEMICOLON
    """
    pass
#-- Dhamar Patiño


# PRODUCCIÓN VACÍA

#-- Cristina Pihuave
def p_vacio(p):
    """
    vacio :
    """
    pass
#-- Cristina Pihuave


# MANEJO DE ERRORES SINTÁCTICOS

#-- Cristina Pihuave
def calcular_columna(lexdata, lexpos):
    ultimo_salto = lexdata.rfind(
        "\n",
        0,
        lexpos
    )

    return lexpos - ultimo_salto


def p_error(p):
    if p:
        columna = calcular_columna(
            p.lexer.lexdata,
            p.lexpos
        )

        if p.type == "RLLAVE":
            sugerencia = (
                "Revise si falta un punto y coma antes de cerrar "
                "el bloque o si las llaves están balanceadas."
            )

        elif p.type == "SEMICOLON":
            sugerencia = (
                "Revise si falta una expresión o un valor antes "
                "del punto y coma."
            )

        elif p.type in {
            "RPAREN",
            "RCORCHETE"
        }:
            sugerencia = (
                "Revise los paréntesis, los corchetes y los "
                "elementos de la expresión."
            )

        elif p.type == "IMPORT":
            sugerencia = (
                "Las importaciones deben escribirse al inicio "
                "del archivo, antes de las declaraciones."
            )

        else:
            sugerencia = (
                "Revise la instrucción anterior y la posición "
                "de este token."
            )

        mensaje = (
            f"Error sintáctico en la línea {p.lineno}, "
            f"columna {columna}: se encontró "
            f"'{p.value}' ({p.type}). {sugerencia}"
        )

    else:
        mensaje = (
            "Error sintáctico al final del archivo: "
            "la última instrucción o bloque está incompleto. "
            "Revise los puntos y coma y los delimitadores."
        )

    print(mensaje)
    errores_sintacticos.append(mensaje)
#-- Cristina Pihuave


# CONSTRUCCIÓN DEL ANALIZADOR SINTÁCTICO

#-- Dhamar Patiño
parser = yacc.yacc(
    start="programa"
)
#-- Dhamar Patiño