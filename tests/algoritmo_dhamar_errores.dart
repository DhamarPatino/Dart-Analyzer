// --- PRUEBA DE ERRORES GLOBAL ---

// 1. ERRORES LÉXICOS (Tokens inválidos)
int usuario$ = 1;
int 123edad = 20;
$

// 2. ERRORES SEMÁNTICOS (Tipos y declaraciones)
void verificarAcceso() {
  int autorizacio = 5;
  
  // Error Semántico: Variable 'nombre' no declarada
  print(nombre); 
  
  // Error Semántico: Asignación incompatible (String a int)
  autorizacio = "SÍ"; 
}

void main() {

  // 3. ERRORES SINTÁCTICOS (Estructura incorrecta)
  // Error Sintáctico: Falta punto y coma
  int edad = 25 

  // Error Sintáctico: Estructura 'if' mal formada (falta la palabra IF)
  (edad >= 18) {
    print("Es mayor de edad");
  }

  // Error Sintáctico: Bloque de for mal cerrado o incompleto
  for (int i = 0; i < 3; i++ {
    print(i);
  }

}