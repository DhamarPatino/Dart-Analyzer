tabla_simbolos = {}
errores_semanticos = []

# ---------------------------
# Reglas semánticas
# ---------------------------

# -- Dhamar Patiño

# Regla 1: Variable no declarada

def registrar_variable(nombre, tipo):

    tabla_simbolos[nombre] = tipo

def verificar_variable(nombre):
    if nombre not in tabla_simbolos:
        errores_semanticos.append(
            f"Error semántico: Variable '{nombre}' no declarada."
        )

# Regla 2: ipo incompatible

def obtener_tipo(valor):

    if isinstance(valor, int):
        return "int"

    if isinstance(valor, float):
        return "double"

    if isinstance(valor, str):
        return "String"

    if isinstance(valor, bool):
        return "bool"

    if valor in tabla_simbolos:
        return tabla_simbolos[valor]

    return None


def verificar_asignacion(nombre, tipo_valor):

    if nombre not in tabla_simbolos:
        return

    tipo_variable = tabla_simbolos[nombre]

    if tipo_variable != tipo_valor:
        errores_semanticos.append(
            f"Error semántico: No se puede asignar un {tipo_valor} a una variable {tipo_variable}."
        )

# -- Dhamar Patiño