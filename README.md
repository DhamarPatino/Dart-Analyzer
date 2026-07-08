# Analizador Dart con PLY

Proyecto parcial de Compiladores.

Integrantes:
- Dhamar Patiño
- Cristina Pihuave

Tecnologías:
- Python 3
- PLY
- GitHub
- Tkinter

Estado:
- ✅ Analizador Léxico
- ✅ Analizador Sintáctico
- ✅ Analizador Semántico
- ✅ Interfaz Gráfica

## Requisitos

- Python 3.10 o superior.
- [PLY](https://ply.readthedocs.io/en/latest/) 3.11 (analizador léxico y sintáctico).
- Tkinter para la interfaz gráfica. Viene incluido con Python en Windows y macOS.
  En Linux (Ubuntu/Debian) puede requerir instalarlo aparte:
  ```bash
  sudo apt install python3-tk
  ```

## Instalación

Clonar el repositorio e instalar las dependencias listadas en `requirements.txt`:

```bash
git clone https://github.com/DhamarPatino/Dart-Analyzer.git
cd Dart-Analyzer
pip install -r requirements.txt
```

## Ejecución

Interfaz gráfica (recomendado):

```bash
python -m src.gui.app
```

Desde la interfaz se puede escribir o pegar código Dart en el editor, o cargar
uno de los algoritmos de prueba de la carpeta `tests/`, y ejecutar el análisis
léxico, sintáctico y semántico. Los resultados se muestran en el panel derecho:
tokens, árbol sintáctico, errores (léxicos y sintácticos con línea y columna;
semánticos con línea) y logs.

Modo consola (interactivo, recorre los archivos de `tests/`):

```bash
python -m src.main
```

## Estructura del proyecto

```
src/
  lexer/      Analizador léxico (tokens, palabras reservadas, errores léxicos)
  parser/     Analizador sintáctico (gramática y recuperación de errores)
  semantic/   Analizador semántico (tabla de símbolos y reglas semánticas)
  gui/        Interfaz gráfica de usuario (Tkinter)
tests/        Algoritmos de prueba en Dart de cada integrante
logs/         Logs generados por cada análisis (léxico, sintáctico, semántico)
```
