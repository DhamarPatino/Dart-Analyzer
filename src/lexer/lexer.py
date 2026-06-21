import ply.lex as lex
import re


#-- Cristina Pihuave
data_types = {
    "int": "INT_TYPE",
    "double": "DOUBLE_TYPE",
    "String": "STRING_TYPE",
    "bool": "BOOL_TYPE",
    "List": "LIST_TYPE",
    "Map": "MAP_TYPE",
}


reserved = {
    "var": "VAR",
    "final": "FINAL",
    "const": "CONST",
    "if": "IF",
    "else": "ELSE",
    "for": "FOR",
    "return": "RETURN",
    "void": "VOID",
    "import": "IMPORT",
    "true": "TRUE",
    "false": "FALSE",
}


# Identificadores predefinidos utilizados por el subconjunto de Dart.
predefined_identifiers = {
    "print": "PRINT",
    "stdin": "STDIN",
    "readLineSync": "READ_LINE_SYNC",
}
#-- Cristina Pihuave


tokens = (
    #-- Dhamar Patiño
    "IDENTIFIER",

    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "MODULO",

    "EQUALS",
    "NOT_EQUALS",

    "GREATER_THAN",
    "LESS_THAN",
    "GREATER_EQUAL",
    "LESS_EQUAL",

    "AND",
    "OR",
    "NOT",

    "ASSIGN",

    "PLUS_ASSIGN",
    "MINUS_ASSIGN",
    "TIMES_ASSIGN",
    "DIVIDE_ASSIGN",
    #-- Dhamar Patiño

    #-- Cristina Pihuave
    "INT_TYPE",
    "DOUBLE_TYPE",
    "STRING_TYPE",
    "BOOL_TYPE",
    "LIST_TYPE",
    "MAP_TYPE",

    "INTEGER_LITERAL",
    "DOUBLE_LITERAL",
    "STRING_LITERAL",

    "VAR",
    "FINAL",
    "CONST",
    "IF",
    "ELSE",
    "FOR",
    "RETURN",
    "VOID",
    "IMPORT",
    "TRUE",
    "FALSE",

    "PRINT",
    "STDIN",
    "READ_LINE_SYNC",

    "SEMICOLON",

    "LLLAVE",
    "RLLAVE",

    "LPAREN",
    "RPAREN",

    "LCORCHETE",
    "RCORCHETE",

    "COMA",
    "PUNTO",
    "COLON",

    "INCREMENT",
    "ARROW",
    #-- Cristina Pihuave
)


#-- Dhamar Patiño
t_PLUS = r"\+"
t_MINUS = r"-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_MODULO = r"%"

t_EQUALS = r"=="
t_NOT_EQUALS = r"!="

t_GREATER_EQUAL = r">="
t_LESS_EQUAL = r"<="

t_GREATER_THAN = r">"
t_LESS_THAN = r"<"

t_AND = r"&&"
t_OR = r"\|\|"
t_NOT = r"!"

t_ASSIGN = r"="

t_PLUS_ASSIGN = r"\+="
t_MINUS_ASSIGN = r"-="
t_TIMES_ASSIGN = r"\*="
t_DIVIDE_ASSIGN = r"/="
#-- Dhamar Patiño


#-- Cristina Pihuave
t_INCREMENT = r"\+\+"
t_ARROW = r"=>"

t_SEMICOLON = r";"

# Llaves
t_LLLAVE = r"\{"
t_RLLAVE = r"\}"

# Paréntesis
t_LPAREN = r"\("
t_RPAREN = r"\)"

# Corchetes
t_LCORCHETE = r"\["
t_RCORCHETE = r"\]"

t_COMA = r","
t_PUNTO = r"\."
t_COLON = r":"
#-- Cristina Pihuave


#-- Dhamar Patiño
# Variables, palabras reservadas, tipos e identificadores predefinidos.
def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"

    t.type = reserved.get(
        t.value,
        data_types.get(
            t.value,
            predefined_identifiers.get(
                t.value,
                "IDENTIFIER"
            )
        )
    )

    return t


# Ignorar espacios, tabulaciones y retorno de carro.
t_ignore = " \t\r"


# Los comentarios se reconocen, pero no se envían al parser.
def t_COMMENT_SINGLE(t):
    r"//[^\n]*"
    pass


def t_COMMENT_MULTI(t):
    r"/\*[\s\S]*?\*/"
    t.lexer.lineno += t.value.count("\n")
    pass


# Actualizar el contador de líneas.
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
#-- Dhamar Patiño


#-- Cristina Pihuave
def t_STRING_LITERAL(t):
    r"\"([^\"\\]|\\.)*\"|\'([^\'\\]|\\.)*\'"
    return t


def t_DOUBLE_LITERAL(t):
    r"\d+\.\d+(?![A-Za-z0-9_.])"
    t.value = float(t.value)
    return t


def t_INTEGER_LITERAL(t):
    r"\d+(?![A-Za-z0-9_.])"
    t.value = int(t.value)
    return t


# Manejo de errores léxicos.
def calculate_column(lexdata, lexpos):
    last_newline = lexdata.rfind(
        "\n",
        0,
        lexpos
    )

    return lexpos - last_newline


def register_error(lexer_instance, message):
    lexer_instance.pending_errors.append(
        message
    )


def t_error(t):
    column = calculate_column(
        t.lexer.lexdata,
        t.lexpos
    )

    # Detectar secuencias inválidas como 2saldo o 15iva.
    invalid_identifier = re.match(
        r"\d+(?:\.\d+)?[A-Za-z_][A-Za-z0-9_]*",
        t.value
    )

    if invalid_identifier:
        value = invalid_identifier.group(0)

        message = (
            f"Error léxico en la línea {t.lexer.lineno}, "
            f"columna {column}: '{value}' no es un identificador "
            "válido porque comienza con un dígito."
        )

        register_error(
            t.lexer,
            message
        )

        t.lexer.skip(
            len(value)
        )

        return

    # Detectar caracteres inválidos como @.
    message = (
        f"Error léxico en la línea {t.lexer.lineno}, "
        f"columna {column}: el carácter "
        f"'{t.value[0]}' no es válido."
    )

    register_error(
        t.lexer,
        message
    )

    t.lexer.skip(1)
#-- Cristina Pihuave


#-- Dhamar Patiño
lexer = lex.lex()
#-- Dhamar Patiño


#-- Cristina Pihuave
lexer.pending_errors = []
#-- Cristina Pihuave
