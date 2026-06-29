from pathlib import Path
from datetime import datetime

from src.lexer.lexer import lexer
from src.parser.parser import parser, errores_sintacticos
from src.semantic.semantic import (tabla_simbolos, tabla_funciones, errores_semanticos,
pila_funciones, verificar_variable, verificar_asignacion, verificar_retorno, crear_resultado_tipo)


#-- Dhamar Patiño
BASE_DIR = Path(__file__).resolve().parent.parent
#-- Dhamar Patiño

#-- Cristina Pihuave
ruta_tests = BASE_DIR / "tests"

archivos_dart = sorted(
    ruta_tests.glob("*.dart")
)

if not archivos_dart:
    print(
        "No se encontraron archivos .dart "
        "dentro de la carpeta tests."
    )
    exit()

print(
    "\nAlgoritmos disponibles "
    "en la carpeta tests:\n"
)

for i, archivo in enumerate(
    archivos_dart,
    start=1
):
    print(
        f"{i}. {archivo.name}"
    )

try:
    opcion = int(
        input(
            "\nSeleccione el número del "
            "algoritmo a ejecutar: "
        ).strip()
    )

    if (
        opcion < 1
        or opcion > len(archivos_dart)
    ):
        print("Opción inválida.")
        exit()

except ValueError:
    print(
        "Debe ingresar un número válido."
    )
    exit()

nombre_archivo = (
    archivos_dart[opcion - 1].name
)
#-- Cristina Pihuave


#-- Dhamar Patiño
usuario_git = input(
    "Ingrese su usuario de GitHub "
    "para nombrar el log: "
).strip().replace(" ", "")

if not usuario_git:
    print(
        "Debe ingresar un usuario de GitHub."
    )
    exit()

ruta_archivo = (
    BASE_DIR
    / "tests"
    / nombre_archivo
)

print(
    f"\nArchivo seleccionado: "
    f"{nombre_archivo}"
)

print(
    f"Buscando archivo: "
    f"{ruta_archivo}"
)

try:
    with open(
        ruta_archivo,
        "r",
        encoding="utf-8"
    ) as archivo:
        contenido = archivo.read()

except FileNotFoundError:
    print("Archivo no encontrado.")
    exit()


fecha = datetime.now().strftime(
    "%d%m%Y-%Hh%M"
)
#-- Dhamar Patiño

#-- Cristina Pihuave
ruta_logs = BASE_DIR / "logs"

ruta_logs.mkdir(
    parents=True,
    exist_ok=True
)
#-- Cristina Pihuave


# ANÁLISIS LÉXICO
#-- Cristina Pihuave
lexer.lineno = 1
lexer.pending_errors.clear()
lexer.input(contenido)

ruta_log_lexico = (
    ruta_logs
    / f"lexico-{usuario_git}-{fecha}.txt"
)

with open(
    ruta_log_lexico,
    "w",
    encoding="utf-8"
) as log:

    while True:
        token = lexer.token()
        while lexer.pending_errors:
            error = (
                lexer.pending_errors.pop(0)
            )

            print(error)
            log.write(error + "\n")

        if not token:
            break

        print(token)
        log.write(
            str(token) + "\n"
        )

    while lexer.pending_errors:
        error = (
            lexer.pending_errors.pop(0)
        )

        print(error)
        log.write(error + "\n")

print(
    "\nAnálisis léxico completado."
)

print(
    f"Log léxico generado: "
    f"{ruta_log_lexico}"
)
#-- Cristina Pihuave

# ANÁLISIS SINTÁCTICO

#-- Dhamar Patiño
errores_sintacticos.clear()

lexer.lineno = 1
lexer.pending_errors.clear()

print(
    "\n--- INICIO DEL ANÁLISIS "
    "SINTÁCTICO ---"
)

parser.parse(
    contenido,
    lexer=lexer,
    tracking=True,
    debug=False
)

print(
    "--- FIN DEL ANÁLISIS "
    "SINTÁCTICO ---\n"
)

ruta_log_sintactico = (
    ruta_logs
    / f"sintactico-{usuario_git}-{fecha}.txt"
)

with open(
    ruta_log_sintactico,
    "w",
    encoding="utf-8"
) as log:

    if errores_sintacticos:
        for error in errores_sintacticos:
            log.write(
                error + "\n"
            )

    else:
        log.write(
            "No se encontraron errores "
            "sintácticos.\n"
        )

print(
    "Análisis sintáctico completado."
)

print(
    f"Log sintáctico generado: "
    f"{ruta_log_sintactico}"
)
#-- Dhamar Patiño

# ANÁLISIS SEMÁNTICO

tabla_simbolos.clear()
tabla_funciones.clear()
pila_funciones.clear()
errores_semanticos.clear()

lexer.lineno = 1
lexer.pending_errors.clear()
lexer.input(contenido)

parser.parse(
    contenido,
    lexer=lexer,
    tracking=True,
    debug=False
)

ruta_log_semantico = (
    ruta_logs
    / f"semantico-{usuario_git}-{fecha}.txt"
)

with open(
    ruta_log_semantico,
    "w",
    encoding="utf-8"
) as log:

    if errores_semanticos:

        print("\nErrores semánticos encontrados:")

        for error in errores_semanticos:
            print(error)
            log.write(error + "\n")

    else:

        print("No se encontraron errores semánticos.")

        log.write(
            "No se encontraron errores semánticos.\n"
        )

print(
    "\nAnálisis semántico completado."
)

print(
    f"Log semántico generado: "
    f"{ruta_log_semantico}"
)
# -- Dhamar Patiño