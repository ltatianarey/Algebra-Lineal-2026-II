"""Interfaz de línea de comandos del proyecto.

Ejemplos:
  python main.py matriz --tipo diagonal --filas 4
  python main.py matriz --tipo todas
  python main.py determinante --matriz "2 1 3; 0 -1 4; 1 2 5"
  python main.py inversa --matriz "2 1; 5 3"
  python main.py inversa --aleatoria 3
"""
import argparse
import sys

from calculo import TIPOS, det_laplace, matriz_aleatoria, parse_matriz
from determinante import documento_determinante
from inversa import documento_inversa
from matrices import documento_matriz


def obtener_matriz(a, invertible=False):
    if a.matriz:
        return parse_matriz(a.matriz)
    if a.aleatoria:
        n = a.aleatoria
        for intento in range(200):
            semilla = None if a.semilla is None else a.semilla + intento
            M = matriz_aleatoria("cuadrada", n, n, (-5, 5), semilla)
            if not invertible or det_laplace(M) != 0:
                return M
        raise SystemExit("No se pudo generar una matriz invertible.")
    return parse_matriz(input("Matriz (filas separadas por ';', ej. 2 1; 5 3): "))


def menu():
    """Menú interactivo: se usa cuando se ejecuta main.py sin argumentos."""
    autor = "Lizeth Rey - 2150074"
    print("=== Matrices con Python y PyLaTeX ===")
    print("1. Matriz aleatoria de un tipo")
    print("2. Determinante por el método de Gauss")
    print("3. Matriz inversa")
    print("0. Salir")
    op = input("Opción: ").strip()
    if op == "1":
        print("Tipos:", ", ".join(TIPOS + ["todas"]))
        tipo = input("Tipo: ").strip()
        if tipo not in TIPOS + ["todas"]:
            raise SystemExit("Tipo no válido.")
        filas = int(input("Filas [3]: ") or 3)
        columnas = int(input("Columnas [3]: ") or 3)
        documento_matriz(tipo, filas, columnas, (-9, 9), None, "matriz", True, autor)
    elif op in ("2", "3"):
        A = parse_matriz(input("Matriz (filas separadas por ';', ej. 2 1; 5 3): "))
        if op == "2":
            documento_determinante(A, "determinante", True, autor)
        else:
            documento_inversa(A, "inversa", True, autor)


def main():
    if len(sys.argv) == 1:
        return menu()
    ap = argparse.ArgumentParser(description="Matrices con Python y PyLaTeX")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def comunes(p, defecto):
        p.add_argument("--salida", default=defecto, help="nombre del archivo (sin extensión)")
        p.add_argument("--autor", default="Lizeth Rey - 2150074")
        p.add_argument("--sin-pdf", action="store_true", help="solo generar el .tex")
        p.add_argument("--semilla", type=int, default=None)

    m = sub.add_parser("matriz", help="matriz aleatoria de un tipo")
    m.add_argument("--tipo", choices=TIPOS + ["todas"], required=True)
    m.add_argument("--filas", type=int, default=3)
    m.add_argument("--columnas", type=int, default=3)
    m.add_argument("--min", type=int, default=-9)
    m.add_argument("--max", type=int, default=9)
    comunes(m, "matriz")

    for nombre, ayuda in (("determinante", "determinante por Gauss"), ("inversa", "matriz inversa")):
        p = sub.add_parser(nombre, help=ayuda)
        p.add_argument("--matriz", help="p. ej. '2 1; 5 3' (admite fracciones como 1/2)")
        p.add_argument("--aleatoria", type=int, metavar="N", help="usar una matriz cuadrada aleatoria de orden N")
        comunes(p, nombre)

    a = ap.parse_args()
    pdf = not a.sin_pdf
    if a.cmd == "matriz":
        documento_matriz(a.tipo, a.filas, a.columnas, (a.min, a.max), a.semilla, a.salida, pdf, a.autor)
    elif a.cmd == "determinante":
        documento_determinante(obtener_matriz(a), a.salida, pdf, a.autor)
    else:
        documento_inversa(obtener_matriz(a, invertible=True), a.salida, pdf, a.autor)


if __name__ == "__main__":
    main()