// Algoritmo de prueba Cristina Pihuave
import 'dart:io';

/*
Valida tipos de datos, palabras reservadas, literales, delimitadores y operadores especiales.
Con un caso: validar registro académico de un estudiante.
*/

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

double calcularPromedio(double nota1, double nota2) {
    return (nota1 + nota2) / 2;
}

int calcularPuntajeExtra(int puntos) => puntos * puntos;

void main() {
    print("Ingrese el nombre del estudiante:");

    String nombre = stdin.readLineSync()!;

    for (int i = 0; i < 2; i++) {
        print(materias[i]);
    }

    if (estudianteActivo && asistencias["Lenguajes de Programacion"] >= 80) {
        print("Estudiante habilitado en $ciudad");
        print("Bienvenido, $nombre");
    } else {
        print("Estudiante no habilitado");
    }
}