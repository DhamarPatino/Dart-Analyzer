from pathlib import Path
from datetime import datetime
from lexer.lexer import lexer

#-- Dhamar Patiño
BASE_DIR = Path(__file__).resolve().parent.parent

#-- Cristina Pihuave
ruta_tests = BASE_DIR / "tests"

archivos_dart = sorted(ruta_tests.glob("*.dart"))

if not archivos_dart:
    print("No se encontraron archivos .dart dentro de la carpeta tests.")
    exit()

print("\nAlgoritmos disponibles en la carpeta tests:\n")

for i, archivo in enumerate(archivos_dart, start=1):
    print(f"{i}. {archivo.name}")

try:
    opcion = int(input("\nSeleccione el número del algoritmo a ejecutar: ").strip())

    if opcion < 1 or opcion > len(archivos_dart):
        print("Opción inválida")
        exit()

except ValueError:
    print("Debe ingresar un número válido")
    exit()

nombre_archivo = archivos_dart[opcion - 1].name
#-- Cristina Pihuave

#-- Dhamar Patiño
nombre_autor = input("Ingrese su nombre y apellido para el log: ").strip().replace(" ", "")

ruta_archivo = BASE_DIR / "tests" / nombre_archivo

print(f"\nArchivo seleccionado: {nombre_archivo}")
print(f"Buscando archivo: {ruta_archivo}")

try:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

except FileNotFoundError:
    print("Archivo no encontrado")
    exit()

lexer.lineno = 1
lexer.pending_errors.clear()
lexer.input(contenido)

fecha = datetime.now().strftime("%d-%m-%Y-%Hh%M")
#-- Dhamar Patiño

#-- Cristina Pihuave
ruta_logs = BASE_DIR / "logs"
ruta_logs.mkdir(parents=True, exist_ok=True)

ruta_log = (
    ruta_logs /
    f"lexico-{nombre_autor}-{fecha}.txt"
)

with open(ruta_log, "w", encoding="utf-8") as log:

    while True:

        token = lexer.token()

        # Guardar los errores que se hayan detectado antes de retornar el siguiente token válido.
        while lexer.pending_errors:
            error = lexer.pending_errors.pop(0)
            print(error)
            log.write(error + "\n")

        if not token:
            break

        print(token)
        log.write(str(token) + "\n")

    # Guardar cualquier error pendiente al final.
    while lexer.pending_errors:
        error = lexer.pending_errors.pop(0)
        print(error)
        log.write(error + "\n")
#-- Cristina Pihuave
        
print("\nAnálisis léxico completado.")
print(f"Log generado: {ruta_log}")