// Algoritmo de prueba Dhamar Patiño
import 'dart:io';

/*
Sistema de gestión de préstamos de una biblioteca universitaria.
Valida tipos de datos, estructuras de datos, funciones,
expresiones aritméticas, estructuras de control y entrada de datos.
*/

const int maxPrestamos = 3;
final String biblioteca = "Biblioteca Central";

var usuarioActivo = true;
bool tieneMultas = false;
int opcion = 2;

List<String> libros = [
  "Estructuras de Datos",
  "Compiladores",
  "Ingenieria de Software"
];

Map<String, int> ejemplaresDisponibles = {
  "Estructuras de Datos": 5,
  "Compiladores": 2,
  "Ingenieria de Software": 4
};

double calcularPorcentajeDisponibilidad(int disponibles, int total) {
  return (disponibles / total) * 100;
}

int calcularDiasRetraso(int dias) => dias * dias;

void main() {

  String nombre = stdin.readLineSync()!;
  print("Bienvenido, $nombre");

  print("Libros disponibles:");

  for (int i = 0; i < maxPrestamos; i++) {
    print(libros[i]);
  }

  double porcentaje =
      calcularPorcentajeDisponibilidad(
          ejemplaresDisponibles["Compiladores"]!,
          10);

  int penalizacion = calcularDiasRetraso(2);

  if (usuarioActivo &&
      !tieneMultas &&
      ejemplaresDisponibles["Compiladores"]! > 0) {

    print("Usuario autorizado para préstamo");
    print("Bienvenido, $nombre");
    print("Biblioteca: $biblioteca");
    print("Disponibilidad: $porcentaje");
    print("Penalización calculada: $penalizacion");

    print("Seleccione el número del libro a prestar:");
    String libro = libros[opcion - 1];

    print("Préstamo realizado con éxito.");
    print("Libro prestado: $libro");

  } else {

    print("No es posible realizar el préstamo");

  }

}