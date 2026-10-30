"""Parte 3: matriz inversa por cofactores y adjunta, paso a paso."""
from pylatex import Section, Subsection

from calculo import a_fracciones, cofactores, inversa, menor, producto
from determinante import agregar_procedimiento
from latex_utils import (alineadas, ecuacion, guardar, matriz_latex,
                         nuevo_documento, num, parrafo)


def documento_inversa(A, archivo="inversa", pdf=True, autor=""):
    A = a_fracciones(A)
    n = len(A)
    res = inversa(A)
    det = res["det"]

    doc = nuevo_documento("Cálculo de la matriz inversa", autor)
    with doc.create(Section("Matriz dada", numbering=False)):
        ecuacion(doc, "A = " + matriz_latex(A))

    with doc.create(Section("1. Determinante", numbering=False)):
        parrafo(doc, "La inversa existe solo si $\\det(A)\\neq 0$. Se calcula por Gauss:")
        agregar_procedimiento(doc, A)
        if det == 0:
            parrafo(doc, "Como $\\det(A)=0$, la matriz \\textbf{no tiene inversa}.")
            guardar(doc, archivo, pdf)
            return res

    with doc.create(Section("2. Matriz de cofactores", numbering=False)):
        parrafo(doc, "$C_{ij} = (-1)^{i+j}\\det(M_{ij})$, donde $M_{ij}$ es la matriz que queda "
                     "al quitar la fila $i$ y la columna $j$.")
        lineas = []
        for i in range(n):
            for j in range(n):
                c = res["cof"][i][j]
                if n == 1:
                    lineas.append(rf"C_{{{i + 1}{j + 1}}} &= 1")
                    continue
                m = menor(A, i, j)
                interior = (rf"\left({num(m[0][0])}\right)" if len(m) == 1
                            else matriz_latex(m, "vmatrix"))
                lineas.append(rf"C_{{{i + 1}{j + 1}}} &= (-1)^{{{i + 1}+{j + 1}}} {interior} = {num(c)}")
        alineadas(doc, lineas)
        ecuacion(doc, "C = " + matriz_latex(res["cof"]))

    with doc.create(Section("3. Matriz adjunta", numbering=False)):
        parrafo(doc, "La adjunta es la transpuesta de la matriz de cofactores.")
        ecuacion(doc, r"\operatorname{adj}(A) = C^{T} = " + matriz_latex(res["adj"]))

    with doc.create(Section("4. Matriz inversa", numbering=False)):
        parrafo(doc, "$A^{-1} = \\dfrac{1}{\\det(A)}\\operatorname{adj}(A)$")
        ecuacion(doc, rf"A^{{-1}} = \left({num(1 / det)}\right)" + matriz_latex(res["adj"])
                 + " = " + matriz_latex(res["inv"]))

    with doc.create(Section("5. Verificación", numbering=False)):
        I = producto(A, res["inv"])
        ecuacion(doc, "A\\,A^{-1} = " + matriz_latex(A) + matriz_latex(res["inv"]) + " = " + matriz_latex(I))

    guardar(doc, archivo, pdf)
    return res
