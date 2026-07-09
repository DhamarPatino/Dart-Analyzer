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
// DESCOMENTAR UNA PRUEBA A LA VEZ
// ==========================================================



// ==========================================================
// ERRORES LÉXICOS
// ==========================================================

 $
 int 123edad = 10;



// ==========================================================
// ERRORES SINTÁCTICOS
// ==========================================================

 int numero = ;

 if(edad > 18 {
 }

 for(int i=0 i<5;i++){
 }

 List<int> lista=[1,2,3;

 Map<String,int> datos={
 "uno" 1
 };
 int suma(int a int b){
 }



// ==========================================================
// ERRORES SEMÁNTICOS
// Regla 1 - Variable no declarada
// ==========================================================

apellido = "Patiño";

print(ciudad);

if(altura > 180){
}



// ==========================================================
// ERRORES SEMÁNTICOS
// Regla 2 - Tipo incompatible
// ==========================================================

edad = "veinte";
promedio = true;
aprobado = 100;
nombre = 25;
int numero2 = "hola";



// ==========================================================
// REGLAS SEMÁNTICAS DE CRISTINA
// Operaciones incompatibles
// ==========================================================

 int a = 5;
 String b = "hola";
 a + b;
 bool activo = true;
 activo + 5;
 "hola" * 3;
 true / 2;



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

 int promedioFinal(){
}