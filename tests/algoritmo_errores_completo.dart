// ==========================================================
// ALGORITMO DE PRUEBA - ANALIZADOR DART
// Prueba de análisis léxico, sintáctico y semántico
// ==========================================================

import 'dart:io';

const int MAXIMO = 5;
final String universidad = "ESPOL";

var usuarioActivo = true;
bool tieneMultas = false;

// ----------------------------
// LIST
// ----------------------------

List<String> materias = [
  "Compiladores",
  "Base de Datos",
  "IA"
];

// ----------------------------
// MAP
// ----------------------------

Map<String, int> creditos = {
  "Compiladores": 4,
  "Base de Datos": 5,
  "IA": 3
};

// ----------------------------
// FUNCIÓN CLÁSICA
// ----------------------------

double calcularPromedio(
    int nota1,
    int nota2
) {

  return (nota1 + nota2) / 2;

}

// ----------------------------
// FUNCIÓN FLECHA
// ----------------------------

int cuadrado(int numero) => numero * numero;

// ----------------------------
// MAIN
// ----------------------------

void main() {

  print("Ingrese su nombre:");

  String nombre =
      stdin.readLineSync()!;

  int edad = 20;

  double promedio = 8.5;

  bool aprobado = true;

  print(nombre);

  edad = 25;

  promedio = 9.4;

  edad += 2;
  edad -= 1;
  edad *= 2;
  edad /= 2;

  double resultado =
      calcularPromedio(8,10);

  int numero =
      cuadrado(5);

  print(resultado);
  print(numero);

  print(materias[0]);

  print(
      creditos["Compiladores"]
  );

  if(
      edad > 18 &&
      aprobado
  ){

      print("Mayor de edad");

  }
  else{

      print("Menor");

  }

  for(
      int i = 0;
      i < 3;
      i++
  ){

      print(materias[i]);

  }

  print(universidad);

}

// ==========================================================
// ERRORES LÉXICOS
// ==========================================================

 $
 int 123edad = 10;

// ==========================================================
// ERRORES SEMÁNTICOS
// Regla 1 - Variable no declarada
// Regla 2 - Tipo incompatible
// ==========================================================

void pruebaSemanticaDhamar() {

  apellido = "Patiño";

  print(ciudad);

  if (altura > 180) {
  }

  edad = "veinte";
  promedio = true;
  aprobado = 100;
  nombre = 25;

  int numero2 = "hola";

}

// ==========================================================
// REGLAS SEMÁNTICAS DE CRISTINA
// Operaciones incompatibles
// ==========================================================

void pruebaSemanticaCristina() {

  int a = 5;
  String b = "hola";
  var resultado1 = a + b;

  bool activo = true;
  var resultado2 = activo + 5;

  var resultado3 = "hola" * 3;

  var resultado4 = true / 2;

}

// ==========================================================
// REGLAS SEMÁNTICAS DE CRISTINA
// Retorno incorrecto
// ==========================================================

 int suma(){
     return "hola";
 }

 int resta(){
     return true;
 }

 void mostrar(){
     return 5;
 }

// ==========================================================
// ERRORES SINTÁCTICOS
// ==========================================================

 int numeroSinValor = ;

 List<int> listaSinCerrar=[1,2,3;

 Map<String,int> datosSinDosPuntos={
 "uno" 1
 };

void pruebaSintacticaFor() {

  for(int i=0 i<5;i++){
  }

}

// El caso de 'if' sin '(' ya está cubierto en
// algoritmo_cristina_errores_completo.dart. Este error de
// parámetros (falta coma) se deja al final: su recuperación
// consume el resto del archivo, así que nada relevante va después.
 int sumaMal(int a int b){
 }
