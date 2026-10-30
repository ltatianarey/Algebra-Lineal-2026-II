"""Genera con PyLaTeX el PDF de entrega (datos del equipo, enlaces y detalles)."""
import argparse

from pylatex import Section, Package
from pylatex.utils import NoEscape

from latex_utils import guardar, nuevo_documento, parrafo


def main():
    ap = argparse.ArgumentParser(description="Genera el PDF de entrega de la tarea.")
    ap.add_argument("--integrante", action="append", default=None,
                    help='Formato "Nombre - código". Repetir para cada integrante.')
    ap.add_argument("--github", default="https://github.com/USUARIO/REPOSITORIO")
    ap.add_argument("--video", default="https://www.youtube.com/watch?v=XXXXXXXXXXX")
    ap.add_argument("--salida", default="entrega")
    ap.add_argument("--sin-pdf", action="store_true")
    a = ap.parse_args()
    integrantes = a.integrante or ["Lizeth Rey - 2150074"]

    doc = nuevo_documento("Entrega: matrices con Python y PyLaTeX", "Álgebra Lineal")
    doc.packages.append(Package("hyperref"))

    with doc.create(Section("Integrantes", numbering=False)):
        doc.append(NoEscape(r"\begin{itemize}"))
        for i in integrantes:
            doc.append(NoEscape(r"\item " + i.replace("&", r"\&")))
        doc.append(NoEscape(r"\end{itemize}"))
    with doc.create(Section("Enlaces", numbering=False)):
        doc.append(NoEscape(r"\textbf{Repositorio en GitHub:} \url{" + a.github + r"}\par"))
        doc.append(NoEscape(r"\textbf{Video en YouTube:} \url{" + a.video + r"}\par"))
    with doc.create(Section("Detalles del proyecto", numbering=False)):
        parrafo(doc, "El proyecto se escribió en Python y usa la biblioteca PyLaTeX para generar documentos LaTeX. "
                     "Incluye tres programas: (1) generación de matrices aleatorias de distintos tipos, "
                     "(2) cálculo del determinante por el método de Gauss y (3) cálculo de la matriz inversa "
                     "mediante cofactores y adjunta, mostrando cada paso en el documento generado.")
        parrafo(doc, "Los cálculos usan fracciones exactas para evitar errores de redondeo.")
    guardar(doc, a.salida, not a.sin_pdf)


if __name__ == "__main__":
    main()
