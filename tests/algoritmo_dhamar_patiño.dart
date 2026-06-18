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

  print("Ingrese el nombre del usuario:");

  String nombre = stdin.readLineSync()!;

  print("Libros disponibles:");

  for (int i = 0; i < 3; i++) {
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

  } else {

    print("No es posible realizar el préstamo");

  }

}