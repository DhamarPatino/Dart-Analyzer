import ply.yacc as yacc

from src.lexer.lexer import tokens

from src.semantic.semantic import (
    registrar_variable,
    verificar_variable,
    obtener_tipo,
    obtener_tipo_elemento,
    verificar_asignacion,
    verificar_asignacion_tipos,
    verificar_operacion,
    crear_resultado_tipo,
    iniciar_funcion,
    finalizar_funcion,
    verificar_retorno
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


# TIPOS DE DATOS

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
    p[0] = f"List<{p[3]}>"
#-- Dhamar Patiño


#-- Cristina Pihuave
def p_tipo_mapa(p):
    """
    tipo : MAP_TYPE LESS_THAN tipo COMA tipo GREATER_THAN
    """
    p[0] = f"Map<{p[3]},{p[5]}>"


def p_tipo_opcional(p):
    """
    tipo_opcional : tipo
                  | vacio
    """
    p[0] = p[1]
#-- Cristina Pihuave


# DECLARACIÓN DE VARIABLES

#-- Dhamar Patiño
def p_declaracion_tipo_explicito(p):
    """
    declaracion : tipo IDENTIFIER ASSIGN expresion SEMICOLON
    """

    registrar_variable(
        p[2],
        p[1]
    )

    tipo_valor = obtener_tipo(
        p[4]
    )

    verificar_asignacion(
        p[2],
        tipo_valor
    )
#-- Dhamar Patiño


#-- Cristina Pihuave
def p_declaracion_inferencia_inmutable(p):
    """
    declaracion : VAR IDENTIFIER ASSIGN expresion SEMICOLON
                | FINAL tipo_opcional IDENTIFIER ASSIGN expresion SEMICOLON
                | CONST tipo_opcional IDENTIFIER ASSIGN expresion SEMICOLON
    """

    # var toma el tipo del valor
    if p.slice[1].type == "VAR":

        tipo = obtener_tipo(
            p[4]
        )

        registrar_variable(
            p[2],
            tipo
        )

        return

    tipo_valor = obtener_tipo(
        p[5]
    )

    # final o const sin tipo explícito
    if p[2] is None:

        registrar_variable(
            p[3],
            tipo_valor
        )

    # final o const con tipo explícito
    else:

        registrar_variable(
            p[3],
            p[2]
        )

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

    es_acceso = (
        p.slice[1].type == "acceso_indice"
    )

    if not es_acceso:
        verificar_variable(
            p[1]
        )

    # Regla 2: asignación normal
    if p.slice[2].type == "ASSIGN":

        tipo_valor = obtener_tipo(
            p[3]
        )

        if es_acceso:

            verificar_asignacion_tipos(
                obtener_tipo(p[1]),
                tipo_valor
            )

        else:

            verificar_asignacion(
                p[1],
                tipo_valor
            )

        return

    operadores_compuestos = {
        "PLUS_ASSIGN": "+",
        "MINUS_ASSIGN": "-",
        "TIMES_ASSIGN": "*",
        "DIVIDE_ASSIGN": "/"
    }

    operador = operadores_compuestos[
        p.slice[2].type
    ]

    # Regla 3: revisar la operación
    resultado = verificar_operacion(
        p[1],
        operador,
        p[3]
    )

    # Regla 2: revisar el resultado asignado
    if es_acceso:

        verificar_asignacion_tipos(
            obtener_tipo(p[1]),
            obtener_tipo(resultado)
        )

    else:

        verificar_asignacion(
            p[1],
            obtener_tipo(resultado)
        )
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

        p[0] = p[1]

    else:

        # Regla 3: probando suma o resta
        p[0] = verificar_operacion(
            p[1],
            p[2],
            p[3]
        )


def p_expresion_multiplicativa(p):
    """
    expresion_multiplicativa : expresion_multiplicativa MULTIPLY expresion_unaria
                             | expresion_multiplicativa DIVIDE expresion_unaria
                             | expresion_multiplicativa MODULO expresion_unaria
                             | expresion_unaria
    """

    if len(p) == 2:

        p[0] = p[1]

    else:

        # Regla 3: probando *, / o %
        p[0] = verificar_operacion(
            p[1],
            p[2],
            p[3]
        )
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

    if len(p) == 2:

        p[0] = p[1]

    else:

        p[0] = crear_resultado_tipo(
            "bool"
        )


def p_expresion_and(p):
    """
    expresion_and : expresion_and AND expresion_igualdad
                  | expresion_igualdad
    """

    if len(p) == 2:

        p[0] = p[1]

    else:

        p[0] = crear_resultado_tipo(
            "bool"
        )


def p_expresion_igualdad(p):
    """
    expresion_igualdad : expresion_relacional
                       | expresion_relacional EQUALS expresion_relacional
                       | expresion_relacional NOT_EQUALS expresion_relacional
    """

    if len(p) == 2:

        p[0] = p[1]

    else:

        p[0] = crear_resultado_tipo(
            "bool"
        )


def p_expresion_relacional(p):
    """
    expresion_relacional : expresion_aditiva
                         | expresion_aditiva GREATER_THAN expresion_aditiva
                         | expresion_aditiva LESS_THAN expresion_aditiva
                         | expresion_aditiva GREATER_EQUAL expresion_aditiva
                         | expresion_aditiva LESS_EQUAL expresion_aditiva
    """

    if len(p) == 2:

        p[0] = p[1]

    else:

        p[0] = crear_resultado_tipo(
            "bool"
        )


def p_expresion_unaria(p):
    """
    expresion_unaria : NOT expresion_unaria
                     | MINUS expresion_unaria
                     | factor
    """

    if len(p) == 2:

        p[0] = p[1]

    else:

        # Solo conserva el tipo del valor
        p[0] = p[2]


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

        # Regla 1
        verificar_variable(
            p[1]
        )

        p[0] = p[1]

    elif p.slice[1].type == "TRUE":

        p[0] = True

    elif p.slice[1].type == "FALSE":

        p[0] = False

    elif p.slice[1].type == "LPAREN":

        p[0] = p[2]

    else:

        p[0] = p[1]
#-- Dhamar Patiño


# ESTRUCTURAS DE CONTROL

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

    # Variable ya declarada
    if p.slice[1].type == "IDENTIFIER":

        verificar_variable(
            p[1]
        )

        verificar_asignacion(
            p[1],
            obtener_tipo(p[3])
        )

    # Declaración con var
    elif p.slice[1].type == "VAR":

        registrar_variable(
            p[2],
            obtener_tipo(p[4])
        )

    # Declaración con tipo
    else:

        registrar_variable(
            p[2],
            p[1]
        )

        verificar_asignacion(
            p[2],
            obtener_tipo(p[4])
        )


def p_actualizacion_for(p):
    """
    actualizacion_for : IDENTIFIER INCREMENT
                      | IDENTIFIER PLUS_ASSIGN expresion
                      | IDENTIFIER MINUS_ASSIGN expresion
                      | IDENTIFIER TIMES_ASSIGN expresion
                      | IDENTIFIER DIVIDE_ASSIGN expresion
    """

    # Regla 1
    verificar_variable(
        p[1]
    )

    # ++ solo se reconoce sintácticamente
    if p.slice[2].type == "INCREMENT":
        return

    operadores_compuestos = {
        "PLUS_ASSIGN": "+",
        "MINUS_ASSIGN": "-",
        "TIMES_ASSIGN": "*",
        "DIVIDE_ASSIGN": "/"
    }

    operador = operadores_compuestos[
        p.slice[2].type
    ]

    # Regla 3
    resultado = verificar_operacion(
        p[1],
        operador,
        p[3]
    )

    # Regla 2
    verificar_asignacion(
        p[1],
        obtener_tipo(resultado)
    )
#-- Cristina Pihuave


# LISTAS

#-- Dhamar Patiño
def p_lista(p):
    """
    lista : LCORCHETE elementos_lista_opcionales RCORCHETE
    """
    p[0] = []


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


# MAPAS

#-- Cristina Pihuave
def p_mapa(p):
    """
    mapa : LLLAVE pares_mapa_opcionales RLLAVE
    """
    p[0] = {}


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

    # Regla 1
    verificar_variable(
        p[1]
    )

    p[0] = crear_resultado_tipo(
        obtener_tipo_elemento(p[1])
    )
#-- Cristina Pihuave


# FUNCIONES CLÁSICAS

#-- Dhamar Patiño
def p_encabezado_funcion_clasica(p):
    """
    encabezado_funcion_clasica : tipo IDENTIFIER LPAREN parametros_opcionales RPAREN LLLAVE
                               | VOID IDENTIFIER LPAREN parametros_opcionales RPAREN LLLAVE
    """

    # Regla 4 de Cristina:
    # guardar el tipo antes de revisar el cuerpo
    iniciar_funcion(
        p[2],
        p[1]
    )


def p_funcion_clasica(p):
    """
    funcion_clasica : encabezado_funcion_clasica lista_sentencias_opcional RLLAVE
    """

    finalizar_funcion()


def p_retorno(p):
    """
    retorno : RETURN expresion SEMICOLON
            | RETURN SEMICOLON
    """

    # Regla 4: return con valor
    if len(p) == 4:

        verificar_retorno(
            valor=p[2],
            tiene_valor=True
        )

    # Regla 4: return sin valor
    else:

        verificar_retorno(
            tiene_valor=False
        )
#-- Dhamar Patiño


# FUNCIÓN FLECHA

#-- Cristina Pihuave
def p_encabezado_funcion_flecha(p):
    """
    encabezado_funcion_flecha : tipo IDENTIFIER LPAREN parametros_opcionales RPAREN ARROW
    """

    # Regla 4: guardar el tipo de retorno
    iniciar_funcion(
        p[2],
        p[1]
    )


def p_funcion_flecha(p):
    """
    funcion_flecha : encabezado_funcion_flecha expresion SEMICOLON
    """

    # Regla 4: la expresión es el retorno
    verificar_retorno(
        valor=p[2],
        tiene_valor=True
    )

    finalizar_funcion()
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


# LLAMADAS DE FUNCIONES

#-- Dhamar Patiño
def p_llamada_funcion(p):
    """
    llamada_funcion : IDENTIFIER LPAREN argumentos_opcionales RPAREN
    """

    # Regla 1
    verificar_variable(
        p[1]
    )

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

    # Regla 1
    verificar_variable(
        p[1]
    )

    p[0] = crear_resultado_tipo(
        None
    )
#-- Cristina Pihuave


# IMPRESIÓN Y ENTRADA DE DATOS

#-- Dhamar Patiño
def p_impresion(p):
    """
    impresion : PRINT LPAREN expresion RPAREN SEMICOLON
    """
    pass


def p_ingreso_datos(p):
    """
    ingreso_datos : STDIN PUNTO READ_LINE_SYNC LPAREN RPAREN
                  | STDIN PUNTO READ_LINE_SYNC LPAREN RPAREN NOT
    """

    p[0] = crear_resultado_tipo(
        "String"
    )
#-- Dhamar Patiño


# IMPORTACIONES

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
    p[0] = None
#-- Cristina Pihuave


# ERRORES SINTÁCTICOS

#-- Cristina Pihuave
def calcular_columna(
    lexdata,
    lexpos
):

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

    errores_sintacticos.append(
        mensaje
    )
#-- Cristina Pihuave


# CONSTRUCCIÓN DEL PARSER

#-- Dhamar Patiño
parser = yacc.yacc(
    start="programa"
)
#-- Dhamar Patiño