// Algoritmo de prueba Cristina Pihuave

import 'dart:io';

/*
Validar tipos de datos, palabras reservadas, literales, delimitadores y operadores especiales.
*/

const double iva = 0.15;
final String ciudad = "Guayaquil";
var activo = true;

List<String> tareas = [
    "Hacer avance de LP",
    "Avanzar diseño de interfaces"
];

Map<String, int> frutas = {
    "manzanas": 5,
    "bananas": 10
};

double calcularPromedio(double nota1, double nota2) {
    return (nota1 + nota2) / 2;
}

int calcularCuadrado(int numero) => numero * numero;

void main() {
    for (int i = 0; i < 2; i++) {
        print(tareas[i]);
    }

    if (activo && frutas["manzanas"] >= 1) {
        print("Ingrese su nombre:");

        String nombre = stdin.readLineSync()!;

        print("Bienvenido, $nombre");
    } else {
        print("Proceso finalizado");
    }
}