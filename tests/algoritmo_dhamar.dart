// Algoritmo de prueba Dhamar

/*
Evalúa operaciones sobre nota, asistencia y faltas para probar operadores del analizador léxico.
*/

double nota = 8.5;
int asistencia = 90;
int faltas = 2;
int total = 10;

nota = nota + 1;
nota = nota - 0.5;
nota = nota * 2;
nota = nota / 2;
faltas = total % 3;

nota += 1;
nota -= 1;
nota *= 2;
nota /= 2;

if (nota >= 7 && asistencia >= 80) {
    nota += 1;
}

if (nota > 9 || asistencia < 75) {
    faltas += 1;
}

if (nota == 10 && asistencia != 0) {
    total += 1;
}

if (!(asistencia <= 50)) {
    total += 1;
}