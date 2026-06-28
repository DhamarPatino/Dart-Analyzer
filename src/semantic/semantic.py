tabla_simbolos = {}
errores_semanticos = []
tabla_funciones = {}
pila_funciones = []


# Guarda el tipo resultante de una expresión
class ResultadoExpresion:

    def __init__(self, tipo):
        self.tipo = tipo


def crear_resultado_tipo(tipo):
    return ResultadoExpresion(tipo)


# REGLAS SEMÁNTICAS

# -- Dhamar Patiño
# Regla 1: variable no declarada

def registrar_variable(nombre, tipo):
    tabla_simbolos[nombre] = tipo


def registrar_funcion(nombre, tipo_retorno):
    tabla_funciones[nombre] = tipo_retorno


def verificar_variable(nombre):

    if (
        nombre not in tabla_simbolos
        and nombre not in tabla_funciones
    ):
        errores_semanticos.append(
            f"Error semántico: Variable o función "
            f"'{nombre}' no declarada."
        )


# Ayuda para obtener el tipo de un valor
def obtener_tipo(valor):

    if isinstance(
        valor,
        ResultadoExpresion
    ):
        return valor.tipo

    # bool se revisa antes de int
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


# Separa los tipos de un Map
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
    tipo_valor
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
        errores_semanticos.append(
            f"Error semántico: No se puede asignar "
            f"un {tipo_valor} a una variable "
            f"{tipo_destino}."
        )


def verificar_asignacion(
    nombre,
    tipo_valor
):

    if nombre not in tabla_simbolos:
        return

    verificar_asignacion_tipos(
        tabla_simbolos[nombre],
        tipo_valor
    )


# -- Cristina Pihuave
# Regla 3: operaciones con tipos incompatibles

def es_tipo_numerico(tipo):

    return tipo in {
        "int",
        "double"
    }


def verificar_operacion(
    valor_izquierdo,
    operador,
    valor_derecho
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

    # Operaciones entre números
    if (
        es_tipo_numerico(tipo_izquierdo)
        and es_tipo_numerico(tipo_derecho)
    ):

        # La división da como resultado double
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

    errores_semanticos.append(
        f"Error semántico: Operación incompatible. "
        f"No se puede aplicar el operador '{operador}' "
        f"entre un valor de tipo '{tipo_izquierdo}' "
        f"y un valor de tipo '{tipo_derecho}'."
    )

    return crear_resultado_tipo(
        None
    )


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
    tiene_valor=False
):

    # Un return fuera de una función
    # se revisa en el parser
    if not pila_funciones:
        return

    funcion_actual = pila_funciones[-1]

    nombre_funcion = (
        funcion_actual["nombre"]
    )

    tipo_declarado = (
        funcion_actual["tipo_retorno"]
    )

    # Una función void no retorna valores
    if tipo_declarado == "void":

        if tiene_valor:
            errores_semanticos.append(
                f"Error semántico: La función "
                f"'{nombre_funcion}' es de tipo void "
                "y no puede retornar un valor."
            )

        return

    # Una función con tipo debe retornar un valor
    if not tiene_valor:
        errores_semanticos.append(
            f"Error semántico: La función "
            f"'{nombre_funcion}' declara un retorno "
            f"de tipo '{tipo_declarado}' y no puede "
            "usar 'return;' sin un valor."
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
        errores_semanticos.append(
            f"Error semántico: La función "
            f"'{nombre_funcion}' declara un retorno "
            f"de tipo '{tipo_declarado}', pero retorna "
            f"un valor de tipo '{tipo_retornado}'."
        )