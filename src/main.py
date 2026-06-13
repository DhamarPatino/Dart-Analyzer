from pathlib import Path
from datetime import datetime
from lexer.lexer import lexer

BASE_DIR = Path(__file__).resolve().parent.parent


nombre_archivo = input(
    "Ingrese el nombre del archivo Dart: "
)

ruta_archivo = BASE_DIR / "tests" / nombre_archivo

print(f"Buscando archivo: {ruta_archivo}")

try:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

except FileNotFoundError:
    print("Archivo no encontrado")
    exit()

lexer.input(contenido)

fecha = datetime.now().strftime("%d-%m-%Y-%Hh%M")

ruta_log = (
    BASE_DIR /
    "logs" /
    f"lexico-{Path(nombre_archivo).stem}-{fecha}.txt"
)

with open(ruta_log, "w", encoding="utf-8") as log:

    while True:

        token = lexer.token()

        if not token:
            break

        print(token)
        log.write(str(token) + "\n")

print("\nAnálisis léxico completado.")
print(f"Log generado: {ruta_log}")