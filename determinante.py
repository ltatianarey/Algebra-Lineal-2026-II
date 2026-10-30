"""Parte 2: determinante por el método de Gauss, paso a paso."""
from pylatex import Section, Subsection

from calculo import a_fracciones, eliminacion_gauss
from latex_utils import ecuacion, guardar, matriz_latex, nuevo_documento, num, parrafo


def _operacion(p):
    if p["tipo"] == "swap":
        return rf"R_{{{p['i'] + 1}}} \leftrightarrow R_{{{p['j'] + 1}}}"
    return (rf"R_{{{p['i'] + 1}}} \leftarrow R_{{{p['i'] + 1}}} "
            rf"- \left({num(p['m'])}\right) R_{{{p['j'] + 1}}}")


def agregar_procedimiento(doc, A):
    """Escribe en `doc` el cálculo de det(A) por Gauss. Devuelve el resultado de eliminacion_gauss."""
    A = a_fracciones(A)
    r = eliminacion_gauss(A)

    with doc.create(Subsection("Reglas usadas", numbering=False)):
        parrafo(doc, "Intercambiar dos filas cambia el signo del determinante. "
                     "Restar a una fila un múltiplo de otra no lo altera. "
                     "El determinante de una matriz triangular es el producto de los elementos de su diagonal.")

    with doc.create(Subsection("Eliminación de Gauss", numbering=False)):
        ecuacion(doc, r"A^{(0)} = " + matriz_latex(A))
        for k, p in enumerate(r["pasos"], start=1):
            parrafo(doc, f"Paso {k}: $" + _operacion(p) + "$")
            ecuacion(doc, rf"A^{{({k})}} = " + matriz_latex(p["despues"]))
        if not r["pasos"]:
            parrafo(doc, "La matriz ya es triangular superior; no se necesitan operaciones.")

    with doc.create(Subsection("Resultado", numbering=False)):
        n = len(A)
        if r["singular"]:
            c = r["columna_sin_pivote"] + 1
            parrafo(doc, f"En la columna {c} no hay ningún elemento distinto de cero para usar como pivote, "
                         "así que la matriz es singular y $\\det(A)=0$.")
        else:
            diag = r"\cdot ".join(rf"\left({num(r['final'][k][k])}\right)" for k in range(n))
            parrafo(doc, f"Se hicieron {r['intercambios']} intercambio(s) de filas, por lo que el signo es "
                         f"$(-1)^{{{r['intercambios']}}}$.")
            ecuacion(doc, rf"\det(A) = (-1)^{{{r['intercambios']}}} \cdot {diag} = {num(r['det'])}")
    return r


def documento_determinante(A, archivo="determinante", pdf=True, autor=""):
    A = a_fracciones(A)
    doc = nuevo_documento("Cálculo del determinante por el método de Gauss", autor)
    with doc.create(Section("Matriz dada", numbering=False)):
        ecuacion(doc, "A = " + matriz_latex(A))
    with doc.create(Section("Procedimiento", numbering=False)):
        r = agregar_procedimiento(doc, A)
    guardar(doc, archivo, pdf)
    return r
