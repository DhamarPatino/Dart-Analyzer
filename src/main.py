from pathlib import Path
from datetime import datetime
from lexer.lexer import lexer

#-- Dhamar Patiño
BASE_DIR = Path(__file__).resolve().parent.parent
nombre_archivo = input("Ingrese el nombre del archivo Dart: ").strip()
nombre_autor = input("Ingrese su nombre y apellido para el log: ").strip().replace(" ", "")

ruta_archivo = BASE_DIR / "tests" / nombre_archivo

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
   
        
print("\nAnálisis léxico completado.")
print(f"Log generado: {ruta_log}")