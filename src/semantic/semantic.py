tabla_simbolos = {}
errores_semanticos = []
tabla_funciones = {}

# ---------------------------
# Reglas semánticas
# ---------------------------

# -- Dhamar Patiño

# Regla 1: Variable no declarada

def registrar_variable(nombre, tipo):
    tabla_simbolos[nombre] = tipo

def registrar_funcion(nombre, tipo_retorno):
    tabla_funciones[nombre] = tipo_retorno

def verificar_variable(nombre):
    # Si es una función conocida, no debería dar error de "variable no declarada"
    if nombre not in tabla_simbolos and nombre not in tabla_funciones and nombre != "stdin.readLineSync":
        errores_semanticos.append(
            f"Error semántico: Variable o función '{nombre}' no declarada."
        )

# Regla 2: ipo incompatible

def obtener_tipo(valor):
    if isinstance(valor, bool):
        return "bool"

    if isinstance(valor, int):
        return "int"

    if isinstance(valor, float):
        return "double"

    if isinstance(valor, str):
        # 1. ¿Es una función registrada dinámicamente?
        if valor in tabla_funciones:
            return tabla_funciones[valor]
        
        # Casos especiales de la librería estándar de Dart
        if "stdin.readLineSync" in valor:
            return "String"

        # 2. ¿Es una variable registrada en la tabla de símbolos?
        if valor in tabla_simbolos:
            if tabla_simbolos[valor] == "Map":
                return "int"  # Parche dinámico para accesos a mapas numéricos
            return tabla_simbolos[valor]
        
        # 3. Si no es variable ni función, y empieza con comillas, es un String literal
        if valor.startswith('"') or valor.startswith("'"):
            return "String"
            
        return "String"
    if isinstance(valor, list):
        return "List"

    if isinstance(valor, dict):
        return "Map"

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