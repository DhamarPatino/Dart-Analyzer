// Algoritmo de errores semanticos Cristina Pihuave
import 'dart:io';

// Prueba de las reglas semanticas 3 y 4.
// Regla 3: Operaciones entre tipos de datos
// Regla 4: Retorno de funciones
// Caso: registro academico de un estudiante

const double notaMinima = 7.0;
final String ciudad = "Guayaquil";

var estudianteActivo = true;
bool tieneRecuperacion = false;

List<String> materias = [
    "Lenguajes de Programacion",
    "Diseno de Interfaces"
];

Map<String, int> asistencias = {
    "Lenguajes de Programacion": 90,
    "Diseno de Interfaces": 85
};


// Probando una operacion correcta entre valores double
double calcularPromedio(double nota1, double nota2) {
    return (nota1 + nota2) / 2;
}


// Probando una operacion correcta entre valores int
int calcularPuntajeExtra(int puntos) => puntos * puntos;


// Probando regla 4: declara int pero retorna String
int obtenerAsistenciaIncorrecta() {
    return "noventa";
}


// Probando regla 4: declara bool pero retorna double
bool verificarAprobacionIncorrecta(double promedio) {
    return promedio;
}


// Probando regla 4: una funcion void no puede retornar un valor
void mostrarNombreIncorrecto(String nombre) {
    return nombre;
}


// Probando regla 4: declara String pero usa return sin valor
String obtenerCiudadIncorrecta() {
    return;
}


// Probando regla 4: declara int pero la funcion flecha retorna double
int obtenerNotaMinimaIncorrecta() => notaMinima;


void main() {
    print("Ingrese el nombre del estudiante:");

    String nombre = stdin.readLineSync()!;

    int asistenciaLenguajes =
        asistencias["Lenguajes de Programacion"];


    // Probando regla 3: String + String es correcto
    String mensaje =
        "Estudiante: " + nombre;


    // Probando regla 3: double + int es correcto
    double notaAdicional =
        notaMinima + 1;


    // Probando regla 3: int + int es correcto
    int asistenciaAdicional =
        asistenciaLenguajes + 5;


    // Probando regla 3: no se puede sumar double con String
    double errorNota =
        notaMinima + nombre;


    // Probando regla 3: no se puede multiplicar int con bool
    int errorAsistencia =
        asistenciaLenguajes * estudianteActivo;


    // Probando regla 3: no se pueden restar dos String
    String errorCiudad =
        ciudad - nombre;


    // Probando regla 3: no se puede sumar String con int
    String errorMensaje =
        "Asistencia: " + asistenciaLenguajes;


    print(mensaje);
    print(notaAdicional);
    print(asistenciaAdicional);


    for (int i = 0; i < 2; i++) {
        print(materias[i]);
    }


    if (
        estudianteActivo
        && asistencias["Lenguajes de Programacion"] >= 80
    ) {
        print("Estudiante habilitado en $ciudad");
        print("Bienvenido, $nombre");
    } else {
        print("Estudiante no habilitado");
    }
}