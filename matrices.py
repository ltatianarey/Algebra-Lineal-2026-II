"""Parte 1: matrices aleatorias de distintos tipos y documento LaTeX."""
from pylatex import Section
from pylatex.utils import NoEscape

from calculo import TIPOS, matriz_aleatoria
from latex_utils import ecuacion, guardar, matriz_latex, nuevo_documento, parrafo

DEFINICIONES = {
    "fila": "Una matriz fila tiene una sola fila ($1\\times n$).",
    "columna": "Una matriz columna tiene una sola columna ($m\\times 1$).",
    "cuadrada": "Una matriz cuadrada tiene el mismo número de filas y de columnas ($n\\times n$).",
    "rectangular": "Una matriz rectangular tiene un número distinto de filas y de columnas ($m\\times n$, $m\\neq n$).",
    "diagonal": "Una matriz diagonal es cuadrada y todos sus elementos fuera de la diagonal principal son cero.",
    "triangular_superior": "Una matriz triangular superior es cuadrada y tiene ceros debajo de la diagonal principal.",
    "triangular_inferior": "Una matriz triangular inferior es cuadrada y tiene ceros encima de la diagonal principal.",
    "identidad": "La matriz identidad es diagonal con unos en la diagonal principal.",
    "nula": "Una matriz nula tiene todos sus elementos iguales a cero.",
}


def documento_matriz(tipo, filas=3, columnas=3, rango=(-9, 9), semilla=None,
                     archivo="matriz", pdf=True, autor=""):
    """Genera un documento LaTeX con una matriz aleatoria del tipo pedido.

    Con tipo='todas' incluye un ejemplo de cada tipo.
    """
    tipos = TIPOS if tipo == "todas" else [tipo]
    doc = nuevo_documento("Matrices aleatorias", autor)
    for t in tipos:
        A = matriz_aleatoria(t, filas, columnas, rango, semilla)
        with doc.create(Section(t.replace("_", " ").capitalize(), numbering=False)):
            parrafo(doc, DEFINICIONES[t])
            ecuacion(doc, f"A = {matriz_latex(A)}")
            parrafo(doc, f"Dimensión: ${len(A)}\\times {len(A[0])}$.")
    guardar(doc, archivo, pdf)
    return doc
