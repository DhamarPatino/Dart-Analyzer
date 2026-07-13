tabla_simbolos = {}
errores_semanticos = []
tabla_funciones = {}
pila_funciones = []

# Registra variables final o const para impedir su reasignación.
variables_inmutables = set()


# Agrega el número de línea al mensaje, cuando el parser lo envía.
def _registrar_error_semantico(mensaje, linea=None):
    if linea is not None:
        errores_semanticos.append(
            f"Error semántico en la línea {linea}: {mensaje}"
        )
    else:
        errores_semanticos.append(f"Error semántico: {mensaje}")


# Guarda el tipo resultante de una expresión
class ResultadoExpresion:

    def __init__(self, tipo):
        self.tipo = tipo


def crear_resultado_tipo(tipo):
    return ResultadoExpresion(tipo)


# REGLAS SEMÁNTICAS

# -- Dhamar Patiño
# Regla 1: variable no declarada

def registrar_variable(nombre, tipo, inmutable=False):
    tabla_simbolos[nombre] = tipo

    if inmutable:
        variables_inmutables.add(nombre)
    else:
        variables_inmutables.discard(nombre)


def registrar_funcion(nombre, tipo_retorno):
    tabla_funciones[nombre] = tipo_retorno


def verificar_variable(nombre, linea=None):

    if (
        nombre not in tabla_simbolos
        and nombre not in tabla_funciones
    ):
        _registrar_error_semantico(
            f"Variable o función '{nombre}' no declarada.",
            linea,
        )


def verificar_reasignacion(nombre, linea=None):

    if nombre in variables_inmutables:
        _registrar_error_semantico(
            f"No se puede reasignar '{nombre}' porque se "
            "declaró como final o const.",
            linea,
        )


def verificar_condicion_booleana(tipo, linea=None):

    if tipo is None:
        return

    if tipo != "bool":
        _registrar_error_semantico(
            f"La condición debe ser de tipo bool, pero es de tipo "
            f"'{tipo}'.",
            linea,
        )


def obtener_tipo(valor):

    if isinstance(
        valor,
        ResultadoExpresion
    ):
        return valor.tipo

    if isinstance(valor, bool):
        return "bool"

    if isinstance(valor, int):
        return "int"

    if isinstance(valor, float):
        return "double"

    if isinstance(valor, str):

        if valor in tabla_funciones:
            return tabla_funciones[valor]

        if valor in tabla_simbolos:
            return tabla_simbolos[valor]

        if (
            valor.startswith('"')
            or valor.startswith("'")
        ):
            return "String"

        return None

    if isinstance(valor, list):
        return "List"

    if isinstance(valor, dict):
        return "Map"

    return None


# Separa los tipos de un Map, esto se relaciona a la estructura de datos Map<K, V> en Dart, 
# donde K es el tipo de la clave y V es el tipo del valor
def separar_tipos_mapa(contenido):

    nivel = 0

    for posicion, caracter in enumerate(
        contenido
    ):

        if caracter == "<":
            nivel += 1

        elif caracter == ">":
            nivel -= 1

        elif (
            caracter == ","
            and nivel == 0
        ):
            return (
                contenido[:posicion].strip(),
                contenido[posicion + 1:].strip()
            )

    return None, None


# Obtiene el tipo guardado dentro de List o Map
def obtener_tipo_elemento(nombre):

    tipo = tabla_simbolos.get(nombre)

    if not isinstance(tipo, str):
        return None

    if (
        tipo.startswith("List<")
        and tipo.endswith(">")
    ):
        return tipo[5:-1].strip()

    if (
        tipo.startswith("Map<")
        and tipo.endswith(">")
    ):
        contenido = tipo[4:-1]

        _, tipo_valor = separar_tipos_mapa(
            contenido
        )

        return tipo_valor

    return None


# -- Dhamar Patiño
# Regla 2: asignación de tipo incompatible

def tipos_compatibles(
    tipo_destino,
    tipo_origen
):

    if tipo_destino == tipo_origen:
        return True

    # Un int puede guardarse en un double
    if (
        tipo_destino == "double"
        and tipo_origen == "int"
    ):
        return True

    # Permite asignar un literal de lista
    if (
        isinstance(tipo_destino, str)
        and tipo_destino.startswith("List<")
        and tipo_origen == "List"
    ):
        return True

    # Permite asignar un literal de mapa
    if (
        isinstance(tipo_destino, str)
        and tipo_destino.startswith("Map<")
        and tipo_origen == "Map"
    ):
        return True

    return False


def verificar_asignacion_tipos(
    tipo_destino,
    tipo_valor,
    linea=None
):

    if (
        tipo_destino is None
        or tipo_valor is None
    ):
        return

    if not tipos_compatibles(
        tipo_destino,
        tipo_valor
    ):
        _registrar_error_semantico(
            f"No se puede asignar un {tipo_valor} "
            f"a una variable {tipo_destino}.",
            linea,
        )


def verificar_asignacion(
    nombre,
    tipo_valor,
    linea=None
):

    if nombre not in tabla_simbolos:
        return

    verificar_asignacion_tipos(
        tabla_simbolos[nombre],
        tipo_valor,
        linea
    )


# -- Cristina Pihuave
# Regla 3: operaciones con tipos incompatibles no se pueden realizar

def es_tipo_numerico(tipo):

    return tipo in {
        "int",
        "double"
    }


def verificar_operacion(
    valor_izquierdo,
    operador,
    valor_derecho,
    linea=None
):

    tipo_izquierdo = obtener_tipo(
        valor_izquierdo
    )

    tipo_derecho = obtener_tipo(
        valor_derecho
    )

    # Evita errores repetidos
    if (
        tipo_izquierdo is None
        or tipo_derecho is None
    ):
        return crear_resultado_tipo(
            None
        )

    # String + String
    if (
        operador == "+"
        and tipo_izquierdo == "String"
        and tipo_derecho == "String"
    ):
        return crear_resultado_tipo(
            "String"
        )

    # Operaciones entre numeros
    if (
        es_tipo_numerico(tipo_izquierdo)
        and es_tipo_numerico(tipo_derecho)
    ):

        # La divisió¿on da como resultado double
        if operador == "/":
            return crear_resultado_tipo(
                "double"
            )

        # Si uno es double, el resultado es double
        if (
            tipo_izquierdo == "double"
            or tipo_derecho == "double"
        ):
            return crear_resultado_tipo(
                "double"
            )

        # int con int da int
        return crear_resultado_tipo(
            "int"
        )

    _registrar_error_semantico(
        f"Operación incompatible. No se puede aplicar el "
        f"operador '{operador}' entre un valor de tipo "
        f"'{tipo_izquierdo}' y un valor de tipo '{tipo_derecho}'.",
        linea,
    )

    return crear_resultado_tipo(
        None
    )


# El menos unario solo se aplica a valores numéricos
def verificar_menos_unario(valor, linea=None):

    tipo = obtener_tipo(valor)

    # Evita errores repetidos
    if tipo is None:
        return crear_resultado_tipo(None)

    if not es_tipo_numerico(tipo):

        _registrar_error_semantico(
            f"El operador '-' unario solo se puede aplicar "
            f"a valores numéricos, no a un valor de tipo "
            f"'{tipo}'.",
            linea,
        )

        return crear_resultado_tipo(None)

    return crear_resultado_tipo(tipo)


# -- Cristina Pihuave
# Regla 4: retorno incorrecto de funciones

def iniciar_funcion(
    nombre,
    tipo_retorno
):

    registrar_funcion(
        nombre,
        tipo_retorno
    )

    pila_funciones.append(
        {
            "nombre": nombre,
            "tipo_retorno": tipo_retorno
        }
    )


def finalizar_funcion():

    if pila_funciones:
        pila_funciones.pop()


def verificar_retorno(
    valor=None,
    tiene_valor=False,
    linea=None
):

    # Un return fuera de una función
    if not pila_funciones:
        return

    funcion_actual = pila_funciones[-1]

    nombre_funcion = (
        funcion_actual["nombre"]
    )

    tipo_declarado = (
        funcion_actual["tipo_retorno"]
    )

    # Una funcion void no retorna valores
    if tipo_declarado == "void":

        if tiene_valor:
            _registrar_error_semantico(
                f"La función '{nombre_funcion}' es de tipo "
                "void y no puede retornar un valor.",
                linea,
            )

        return

    # Una función con tipo debe retornar un valor
    if not tiene_valor:
        _registrar_error_semantico(
            f"La función '{nombre_funcion}' declara un "
            f"retorno de tipo '{tipo_declarado}' y no puede "
            "usar 'return;' sin un valor.",
            linea,
        )

        return

    tipo_retornado = obtener_tipo(
        valor
    )

    # Evita errores repetidos
    if tipo_retornado is None:
        return

    if not tipos_compatibles(
        tipo_declarado,
        tipo_retornado
    ):
        _registrar_error_semantico(
            f"La función '{nombre_funcion}' declara un "
            f"retorno de tipo '{tipo_declarado}', pero "
            f"retorna un valor de tipo '{tipo_retornado}'.",
            linea,
        )