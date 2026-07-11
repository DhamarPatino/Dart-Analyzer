import re
import subprocess
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from src.lexer.lexer import lexer
from src.parser.parser import (
    errores_sintacticos,
    obtener_arbol,
    parser,
    reiniciar_arbol,
)
from src.semantic.semantic import (
    errores_semanticos,
    pila_funciones,
    tabla_funciones,
    tabla_simbolos,
    variables_inmutables,
)


#-- Cristina Pihuave
# TEMA OSCURO

FONDO = "#12121a"
PANEL = "#1b1b27"
PANEL_CLARO = "#20202e"
BORDE = "#2c2c3a"
TEXTO = "#e4e4ef"
TEXTO_SECUNDARIO = "#8b8ba7"

COLOR_EXITO = "#22c55e"
COLOR_LEXICO = "#ef4444"
COLOR_SINTACTICO = "#f59e0b"
COLOR_SEMANTICO = "#8b5cf6"

COLOR_KEYWORD = "#60a5fa"
COLOR_TYPE = "#f59e0b"
COLOR_IDENT = "#4ade80"
COLOR_STRING = "#f472b6"
COLOR_NUMBER = "#22d3ee"
COLOR_OPERADOR = "#9ca3af"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RUTA_LOGS = BASE_DIR / "logs"
RUTA_TESTS = BASE_DIR / "tests"


# Palabras y tipos para clasificar tokens y colorear el editor.
PALABRAS_CLAVE = {
    "VAR", "FINAL", "CONST", "IF", "ELSE", "FOR", "RETURN",
    "VOID", "IMPORT", "TRUE", "FALSE", "PRINT", "STDIN", "READ_LINE_SYNC",
}

TIPOS_DATO = {
    "INT_TYPE", "DOUBLE_TYPE", "STRING_TYPE", "BOOL_TYPE", "LIST_TYPE", "MAP_TYPE",
}

PATRON_LINEA = re.compile(r"línea (\d+)")


def categoria_token(tipo):
    if tipo in PALABRAS_CLAVE:
        return "kw"
    if tipo in TIPOS_DATO:
        return "type"
    if tipo == "IDENTIFIER":
        return "ident"
    if tipo == "STRING_LITERAL":
        return "string"
    if tipo in ("INTEGER_LITERAL", "DOUBLE_LITERAL"):
        return "number"
    return "operador"


def extraer_linea(mensaje):
    coincidencia = PATRON_LINEA.search(mensaje)

    if coincidencia:
        return int(coincidencia.group(1))

    return None


def usuario_git_por_defecto():
    try:
        resultado = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        nombre = resultado.stdout.strip()

        return nombre.replace(" ", "") if nombre else "invitado"

    except Exception:
        return "invitado"


# ANÁLISIS
# -- Dhamar Patiño
def ejecutar_lexico(codigo):
    lexer.lineno = 1
    lexer.pending_errors.clear()
    lexer.input(codigo)

    tokens = []

    while True:
        token = lexer.token()

        if not token:
            break

        tokens.append(token)

    return tokens, list(lexer.pending_errors)


def ejecutar_sintactico(codigo):
    errores_sintacticos.clear()
    reiniciar_arbol()
    lexer.lineno = 1
    lexer.pending_errors.clear()

    parser.parse(
        codigo,
        lexer=lexer,
        tracking=True,
        debug=False,
    )

    return list(errores_sintacticos), obtener_arbol()


def ejecutar_semantico(codigo):
    tabla_simbolos.clear()
    tabla_funciones.clear()
    pila_funciones.clear()
    variables_inmutables.clear()
    errores_semanticos.clear()
    reiniciar_arbol()
    lexer.lineno = 1
    lexer.pending_errors.clear()

    parser.parse(
        codigo,
        lexer=lexer,
        tracking=True,
        debug=False,
    )

    return list(errores_semanticos)


# VENTANA PRINCIPAL

#-- Cristina Pihuave
class AplicacionAnalizador(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Analizador Dart — PLY")
        self.geometry("1200x760")
        self.configure(background=FONDO)

        self.usuario_git = tk.StringVar(value=usuario_git_por_defecto())

        self._construir_estilos()
        self._construir_toolbar()
        self._construir_cuerpo()
        self._construir_status_bar()

        self.texto_codigo.insert("1.0", self._codigo_de_ejemplo())
        self._actualizar_numeros_linea()
        self._resaltar_editor()

    # ESTILOS

    def _construir_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Toolbar.TButton",
            background=PANEL_CLARO,
            foreground=TEXTO,
            borderwidth=0,
            focusthickness=0,
            padding=(10, 6),
        )
        estilo.map(
            "Toolbar.TButton",
            background=[("active", BORDE)],
        )

        estilo.configure("TNotebook", background=PANEL, borderwidth=0)
        estilo.configure(
            "TNotebook.Tab",
            background=PANEL,
            foreground=TEXTO_SECUNDARIO,
            padding=(14, 8),
            borderwidth=0,
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", PANEL_CLARO)],
            foreground=[("selected", TEXTO)],
        )

        estilo.configure(
            "Treeview",
            background="#15151f",
            fieldbackground="#15151f",
            foreground=TEXTO,
            borderwidth=0,
            rowheight=24,
        )
        estilo.configure(
            "Treeview.Heading",
            background=PANEL_CLARO,
            foreground=TEXTO_SECUNDARIO,
            borderwidth=0,
        )
        estilo.map("Treeview", background=[("selected", "#33334a")])

        estilo.configure(
            "Vertical.TScrollbar",
            background=PANEL_CLARO,
            troughcolor=PANEL,
            borderwidth=0,
        )

# -- Dhamar Patiño
    # TOOLBAR
    def _construir_toolbar(self):
        barra = tk.Frame(self, background=PANEL, height=52)
        barra.pack(side="top", fill="x")
        
        tk.Label(
            barra,
            text="</> Analizador Dart — PLY",
            background=PANEL,
            foreground=TEXTO,
            font=("Segoe UI", 11, "bold"),
            padx=14,
        ).pack(side="left")

        tk.Frame(
            barra,
            width=20,
            background=PANEL
        ).pack(side="left")

        botones = (
            ("Abrir…", self.abrir_archivo),
            ("▶ Analizar", self.analizar_todo),
            ("◈  Léxico", self.analizar_lexico),
            ("⌘  Sintáctico", self.analizar_sintactico),
            ("⚙ Semántico", self.analizar_semantico),
            ("🗑️Limpiar", self.limpiar),
            ("⭳ Log", self.generar_logs),
        )

        for texto, accion in botones:
            ttk.Button(
                barra,
                text=texto,
                style="Toolbar.TButton",
                command=accion,
            ).pack(side="left", padx=3, pady=8)

        tk.Frame(
            barra,
            background=PANEL
        ).pack(
            side="left",
            expand=True,
            fill="x"
        )
        
        tk.Label(
            barra,
            text="Usuario GitHub:",
            background=PANEL,
            foreground=TEXTO_SECUNDARIO,
        ).pack(side="left", padx=(0, 5))

        tk.Entry(
            barra,
            textvariable=self.usuario_git,
            width=15,
            background="#15151f",
            foreground=TEXTO,
            insertbackground=TEXTO,
            relief="flat",
        ).pack(side="left", ipady=3, padx=(0,12))

        self.badge_estado = tk.Label(
            barra,
            text="✔ Listo",
            background=BORDE,
            foreground=TEXTO,
            padx=13,
            pady=4,
        )
        self.badge_estado.pack(side="right", padx=14)
# -- Cristina Pihuave

    # EDITOR + RESULTADOS

    def _construir_cuerpo(self):
        cuerpo = tk.PanedWindow(
            self,
            orient="horizontal",
            background=FONDO,
            sashwidth=4,
            borderwidth=0,
        )
        cuerpo.pack(side="top", fill="both", expand=True)

        cuerpo.add(self._construir_editor(cuerpo), stretch="always", width=580)
        cuerpo.add(self._construir_resultados(cuerpo), stretch="always")

    def _construir_editor(self, contenedor):
        marco = tk.Frame(contenedor, background=PANEL)

        tk.Label(
            marco,
            text="✎ EDITOR DE CÓDIGO DART",
            background=PANEL,
            foreground=TEXTO_SECUNDARIO,
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            padx=10,
            pady=6,
        ).pack(side="top", fill="x")

        zona = tk.Frame(marco, background="#15151f")
        zona.pack(side="top", fill="both", expand=True)

        self.texto_lineas = tk.Text(
            zona,
            width=4,
            padx=6,
            border=0,
            state="disabled",
            wrap="none",
            background="#15151f",
            foreground=TEXTO_SECUNDARIO,
            font=("Consolas", 11),
        )
        self.texto_lineas.pack(side="left", fill="y")

        self.texto_codigo = tk.Text(
            zona,
            wrap="none",
            undo=True,
            border=0,
            background="#15151f",
            foreground=TEXTO,
            insertbackground=TEXTO,
            selectbackground="#33334a",
            font=("Consolas", 11),
        )
        self.texto_codigo.pack(side="left", fill="both", expand=True)

        barra_scroll = ttk.Scrollbar(
            zona,
            orient="vertical",
            command=self._scroll_editor,
        )
        barra_scroll.pack(side="right", fill="y")
        self.texto_codigo.configure(yscrollcommand=barra_scroll.set)

        self.texto_codigo.tag_configure("kw", foreground=COLOR_KEYWORD)
        self.texto_codigo.tag_configure("type", foreground=COLOR_TYPE)
        self.texto_codigo.tag_configure("string", foreground=COLOR_STRING)
        self.texto_codigo.tag_configure("number", foreground=COLOR_NUMBER)
        self.texto_codigo.tag_configure("comment", foreground=TEXTO_SECUNDARIO)
        self.texto_codigo.tag_configure("linea_error", background="#3a1f1f")
        self.texto_lineas.tag_configure("linea_error", background="#3a1f1f")

        self.texto_codigo.bind("<KeyRelease>", self._al_escribir)
        self.texto_codigo.bind("<MouseWheel>", self._sincronizar_luego)
        self.texto_codigo.bind("<ButtonRelease>", self._sincronizar_luego)

        return marco

    def _construir_resultados(self, contenedor):
        marco = tk.Frame(contenedor, background=PANEL)

        tk.Label(
            marco,
            text="RESULTADOS",
            background=PANEL,
            foreground=TEXTO_SECUNDARIO,
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            padx=10,
            pady=6,
        ).pack(side="top", fill="x")

        self.notebook = ttk.Notebook(marco)
        self.notebook.pack(side="top", fill="both", expand=True, padx=8, pady=(0, 8))

        self.tab_tokens = self._crear_tabla(
            self.notebook,
            ("tipo", "valor", "línea"),
            anchos={"tipo": 130, "valor": 220, "línea": 70},
        )
        self.notebook.add(self.tab_tokens.master, text="Tokens")

        marco_arbol = tk.Frame(self.notebook, background=PANEL)
        self.tab_arbol = ttk.Treeview(marco_arbol, show="tree")
        self.tab_arbol.column("#0", width=700, stretch=False)

        scroll_arbol_v = ttk.Scrollbar(
            marco_arbol, orient="vertical", command=self.tab_arbol.yview
        )
        scroll_arbol_h = ttk.Scrollbar(
            marco_arbol, orient="horizontal", command=self.tab_arbol.xview
        )
        self.tab_arbol.configure(
            yscrollcommand=scroll_arbol_v.set,
            xscrollcommand=scroll_arbol_h.set,
        )

        self.tab_arbol.grid(row=0, column=0, sticky="nsew")
        scroll_arbol_v.grid(row=0, column=1, sticky="ns")
        scroll_arbol_h.grid(row=1, column=0, sticky="ew")
        marco_arbol.rowconfigure(0, weight=1)
        marco_arbol.columnconfigure(0, weight=1)

        self.notebook.add(marco_arbol, text="Árbol")

        self.tab_errores = self._crear_tabla(
            self.notebook,
            ("categoría", "línea", "mensaje"),
            anchos={"categoría": 110, "línea": 70, "mensaje": 900},
        )
        self.notebook.add(self.tab_errores.master, text="Errores")

        self.tab_errores.tag_configure("LÉXICO", foreground=COLOR_LEXICO)
        self.tab_errores.tag_configure("SINTÁCTICO", foreground=COLOR_SINTACTICO)
        self.tab_errores.tag_configure("SEMÁNTICO", foreground=COLOR_SEMANTICO)

        self.tab_tokens.tag_configure("kw", foreground=COLOR_KEYWORD)
        self.tab_tokens.tag_configure("type", foreground=COLOR_TYPE)
        self.tab_tokens.tag_configure("ident", foreground=COLOR_IDENT)
        self.tab_tokens.tag_configure("string", foreground=COLOR_STRING)
        self.tab_tokens.tag_configure("number", foreground=COLOR_NUMBER)
        self.tab_tokens.tag_configure("operador", foreground=COLOR_OPERADOR)

        marco_log = tk.Frame(self.notebook, background=PANEL)
        self.texto_log = tk.Text(
            marco_log,
            background="#15151f",
            foreground=TEXTO,
            border=0,
            wrap="word",
        )
        self.texto_log.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        self.notebook.add(marco_log, text="Log")

        return marco

    def _crear_tabla(self, notebook, columnas, anchos=None):
        anchos = anchos or {}
        marco = tk.Frame(notebook, background=PANEL)
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")

        for columna in columnas:
            tabla.heading(columna, text=columna.upper())
            tabla.column(
                columna,
                width=anchos.get(columna, 140),
                anchor="w",
                stretch=False,
            )

        scroll_v = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        scroll_h = ttk.Scrollbar(marco, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)

        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_v.grid(row=0, column=1, sticky="ns")
        scroll_h.grid(row=1, column=0, sticky="ew")

        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        return tabla

    def _construir_status_bar(self):
        barra = tk.Frame(self, background=PANEL, height=28)
        barra.pack(side="bottom", fill="x")

        self.var_estado = tk.StringVar(value="Listo")

        tk.Label(
            barra,
            textvariable=self.var_estado,
            background=PANEL,
            foreground=TEXTO_SECUNDARIO,
            padx=10,
            pady=4,
        ).pack(side="left")

        tk.Label(
            barra,
            text="Dart · PLY 3.11 · Dhamar Patiño · Cristina Pihuave",
            background=PANEL,
            foreground=TEXTO_SECUNDARIO,
            padx=10,
        ).pack(side="right")

    # EDITOR: numeración de líneas y resaltado

    def _scroll_editor(self, *args):
        self.texto_codigo.yview(*args)
        self.texto_lineas.yview(*args)

    def _sincronizar_luego(self, event=None):
        self.after(1, self._sincronizar_numeros_scroll)

    def _sincronizar_numeros_scroll(self):
        primero, _ = self.texto_codigo.yview()
        self.texto_lineas.yview_moveto(primero)

    def _al_escribir(self, event=None):
        self._actualizar_numeros_linea()
        self._resaltar_editor()

# -- Dhamar Patiño
    def _actualizar_numeros_linea(self):
        cantidad = int(self.texto_codigo.index("end-1c").split(".")[0])
        numeros = "\n".join(str(n) for n in range(1, cantidad + 1))

        self.texto_lineas.configure(state="normal")
        self.texto_lineas.delete("1.0", "end")
        self.texto_lineas.insert("1.0", numeros)
        self.texto_lineas.configure(state="disabled")
        posicion_actual = self.texto_codigo.yview()[0]
        self.texto_lineas.yview_moveto(posicion_actual)
# -- Dhamar Patiño

    def _resaltar_editor(self):
        codigo = self.texto_codigo.get("1.0", "end-1c")

        for etiqueta in ("kw", "type", "string", "number", "comment"):
            self.texto_codigo.tag_remove(etiqueta, "1.0", "end")

        protegido = []

        for patron, etiqueta in (
            (r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'', "string"),
            (r"//[^\n]*|/\*[\s\S]*?\*/", "comment"),
        ):
            for coincidencia in re.finditer(patron, codigo):
                inicio, fin = coincidencia.span()
                protegido.append((inicio, fin))
                self._aplicar_tag_editor(etiqueta, inicio, fin)

        def esta_protegido(pos):
            return any(inicio <= pos < fin for inicio, fin in protegido)

        for patron, etiqueta in (
            (
                r"\b(var|final|const|if|else|for|return|void|import"
                r"|true|false|print|stdin|readLineSync)\b",
                "kw",
            ),
            (r"\b(int|double|String|bool|List|Map)\b", "type"),
            (r"\b\d+\.\d+\b|\b\d+\b", "number"),
        ):
            for coincidencia in re.finditer(patron, codigo):
                inicio, fin = coincidencia.span()

                if not esta_protegido(inicio):
                    self._aplicar_tag_editor(etiqueta, inicio, fin)

    def _aplicar_tag_editor(self, etiqueta, inicio, fin):
        self.texto_codigo.tag_add(
            etiqueta,
            f"1.0+{inicio}c",
            f"1.0+{fin}c",
        )

    def _resaltar_lineas_error(self, lineas):
        self.texto_codigo.tag_remove("linea_error", "1.0", "end")
        self.texto_lineas.tag_remove("linea_error", "1.0", "end")

        for linea in lineas:
            self.texto_codigo.tag_add(
                "linea_error", f"{linea}.0", f"{linea}.0 lineend+1c"
            )
            self.texto_lineas.tag_add(
                "linea_error", f"{linea}.0", f"{linea}.0 lineend+1c"
            )

    # ACCIONES DE ANÁLISIS

    #-- Cristina Pihuave

    def obtener_codigo(self):
        return self.texto_codigo.get("1.0", "end-1c")

    def analizar_lexico(self):
        tokens, errores = ejecutar_lexico(self.obtener_codigo())

        self._poblar_tokens(tokens)
        errores_categorizados = [("LÉXICO", m) for m in errores]
        self._poblar_errores(errores_categorizados)
        self._actualizar_estado(errores_categorizados)
        self.notebook.select(0)

    def analizar_sintactico(self):
        errores, arbol = ejecutar_sintactico(self.obtener_codigo())

        self._poblar_arbol(arbol)
        errores_categorizados = [("SINTÁCTICO", m) for m in errores]
        self._poblar_errores(errores_categorizados)
        self._actualizar_estado(errores_categorizados)
        self.notebook.select(1)

    def analizar_semantico(self):
        errores = ejecutar_semantico(self.obtener_codigo())

        errores_categorizados = [("SEMÁNTICO", m) for m in errores]
        self._poblar_errores(errores_categorizados)
        self._actualizar_estado(errores_categorizados)
        self.notebook.select(2)

    def analizar_todo(self):
        codigo = self.obtener_codigo()

        tokens, errores_lexicos = ejecutar_lexico(codigo)
        errores_sint, arbol = ejecutar_sintactico(codigo)
        errores_sem = ejecutar_semantico(codigo)

        self._poblar_tokens(tokens)
        self._poblar_arbol(arbol)

        errores = (
            [("LÉXICO", m) for m in errores_lexicos]
            + [("SINTÁCTICO", m) for m in errores_sint]
            + [("SEMÁNTICO", m) for m in errores_sem]
        )
        self._poblar_errores(errores)
        self._actualizar_estado(errores)

        self.notebook.select(2 if errores else 0)

        self._escribir_logs(errores_lexicos, errores_sint, errores_sem)

    def limpiar(self):
        self.texto_codigo.delete("1.0", "end")
        self._actualizar_numeros_linea()
        self.tab_tokens.delete(*self.tab_tokens.get_children())
        self.tab_arbol.delete(*self.tab_arbol.get_children())
        self.tab_errores.delete(*self.tab_errores.get_children())
        self.texto_log.delete("1.0", "end")
        self._resaltar_lineas_error([])
        self._actualizar_estado([])

    # POBLAR PESTAÑAS

    #-- Cristina Pihuave

    def _poblar_tokens(self, tokens):
        self.tab_tokens.delete(*self.tab_tokens.get_children())

        for token in tokens:
            self.tab_tokens.insert(
                "",
                "end",
                values=(token.type, token.value, token.lineno),
                tags=(categoria_token(token.type),),
            )

    def _poblar_arbol(self, arbol):
        self.tab_arbol.delete(*self.tab_arbol.get_children())

        if arbol is not None:
            self._insertar_nodo_arbol("", arbol)

    def _insertar_nodo_arbol(self, padre, nodo):
        if nodo["tipo"] == "token":
            etiqueta = f'{nodo["nombre"]}  →  {nodo["valor"]!r}'
            self.tab_arbol.insert(padre, "end", text=etiqueta)
            return

        item = self.tab_arbol.insert(padre, "end", text=nodo["nombre"], open=True)

        for hijo in nodo["hijos"]:
            self._insertar_nodo_arbol(item, hijo)

    def _poblar_errores(self, errores):
        self.tab_errores.delete(*self.tab_errores.get_children())
        lineas = []

        for categoria, mensaje in errores:
            linea = extraer_linea(mensaje)

            if linea is not None:
                lineas.append(linea)

            self.tab_errores.insert(
                "",
                "end",
                values=(categoria, linea if linea is not None else "-", mensaje),
                tags=(categoria,),
            )

        self._resaltar_lineas_error(lineas)

    def _actualizar_estado(self, errores):
        cantidad = len(errores)

        if cantidad == 0:
            self.var_estado.set("Análisis completado · 0 errores")
            self.badge_estado.configure(text="✓ Sin errores", background=COLOR_EXITO)
            return

        plural_error = "es" if cantidad != 1 else ""
        plural_encontrado = "s" if cantidad != 1 else ""
        self.var_estado.set(
            f"{cantidad} error{plural_error} encontrado{plural_encontrado}"
        )
        self.badge_estado.configure(
            text=f"⚠ {cantidad} error{plural_error}", background=COLOR_LEXICO
        )

    # LOGS

    #-- Dhamar Patiño

    def _escribir_logs(self, errores_lexicos, errores_sint, errores_sem):
        RUTA_LOGS.mkdir(parents=True, exist_ok=True)
        fecha = datetime.now().strftime("%d%m%Y-%Hh%M")
        usuario = self.usuario_git.get().strip() or "invitado"

        rutas = {
            "lexico": RUTA_LOGS / f"lexico-{usuario}-{fecha}.txt",
            "sintactico": RUTA_LOGS / f"sintactico-{usuario}-{fecha}.txt",
            "semantico": RUTA_LOGS / f"semantico-{usuario}-{fecha}.txt",
        }

        self._escribir_un_log(rutas["lexico"], errores_lexicos, "léxicos")
        self._escribir_un_log(rutas["sintactico"], errores_sint, "sintácticos")
        self._escribir_un_log(rutas["semantico"], errores_sem, "semánticos")

        self.texto_log.delete("1.0", "end")

        for tipo, ruta in rutas.items():
            self.texto_log.insert("end", f"--- {ruta.name} ---\n")
            self.texto_log.insert("end", ruta.read_text(encoding="utf-8"))
            self.texto_log.insert("end", "\n")

        self.notebook.select(3)

    def _escribir_un_log(self, ruta, errores, nombre):
        with open(ruta, "w", encoding="utf-8") as log:
            if errores:
                for error in errores:
                    log.write(error + "\n")
            else:
                log.write(f"No se encontraron errores {nombre}.\n")

    def generar_logs(self):
        self.analizar_todo()

    # ARCHIVO

    #-- Cristina Pihuave

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Abrir algoritmo Dart",
            initialdir=RUTA_TESTS if RUTA_TESTS.exists() else BASE_DIR,
            filetypes=[("Archivos Dart", "*.dart"), ("Todos", "*.*")],
        )

        if not ruta:
            return

        try:
            contenido = Path(ruta).read_text(encoding="utf-8")
        except OSError as error:
            messagebox.showerror("No se pudo abrir el archivo", str(error))
            return

        self.texto_codigo.delete("1.0", "end")
        self.texto_codigo.insert("1.0", contenido)
        self._actualizar_numeros_linea()
        self._resaltar_editor()

    @staticmethod
    def _codigo_de_ejemplo():
        return (
            "// Programa de ejemplo en Dart\n"
            "void main() {\n"
            "  int edad = 25;\n"
            "  String nombre = 'Ana';\n"
            "\n"
            "  if (edad >= 18) {\n"
            "    print('Hola $nombre');\n"
            "  }\n"
            "}\n"
        )


def main():
    aplicacion = AplicacionAnalizador()
    aplicacion.mainloop()


if __name__ == "__main__":
    main()

