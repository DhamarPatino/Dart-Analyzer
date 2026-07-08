// Algoritmo de prueba Cristina Pihuave (CrisPih)
import 'dart:io';

/*
Simula el registro de notas de un curso.
Contiene errores intencionales de los tres analizadores
(léxico, sintáctico y semántico) para la sustentación.
*/

const double notaMinima = 7.0;
final String curso = "Lenguajes de Programacion";

void main() {
  String nombreEstudiante = "Andrea";
  double notaParcial = 8.5;

  // Error semántico Regla 1: variable no declarada
  print(cursoInexistente);

  // Error semántico Regla 2: tipo incompatible en asignación
  int notaFinal = "ocho";

  // Error semántico Regla 3: operación entre tipos incompatibles
  double promedioCurso = notaParcial + curso;

  print(nombreEstudiante);
}

// Error semántico Regla 4: retorno incorrecto
int calcularAprobados() {
  return "no numerico";
}

// Error léxico: identificador que comienza con dígito
double 2doParcial = 9.0;

// Error léxico: carácter no reconocido
int totalAsistencias = 10 @ 2;

// Error sintáctico: falta '(' después de 'if'
void mostrarEstadoFinal() {
  double promedioFinal = 8.0;
  if promedioFinal >= notaMinima) {
    print("Aprobado");
  }
}
