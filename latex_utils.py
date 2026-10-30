"""Utilidades comunes para construir documentos LaTeX con PyLaTeX."""
from fractions import Fraction

from pylatex import Command, Document, Math, Package
from pylatex.utils import NoEscape


def num(x):
    """Número (entero o fracción) en notación LaTeX."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    signo = "-" if x < 0 else ""
    return rf"{signo}\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def matriz_latex(A, entorno="bmatrix"):
    filas = [" & ".join(num(x) for x in fila) for fila in A]
    return rf"\begin{{{entorno}}} " + r" \\ ".join(filas) + rf" \end{{{entorno}}}"


def nuevo_documento(titulo, autor=""):
    doc = Document(
        documentclass="article",
        document_options=["11pt", "a4paper"],
        geometry_options={"margin": "2.5cm"},
    )
    doc.packages.append(Package("babel", options=["spanish"]))
    doc.packages.append(Package("amsmath"))
    doc.preamble.append(Command("title", titulo))
    doc.preamble.append(Command("author", autor))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))
    return doc


def parrafo(doc, texto):
    """Párrafo de texto; puede contener matemáticas entre $...$."""
    doc.append(NoEscape(texto + r"\par"))


def ecuacion(doc, latex):
    """Ecuación en modo display (\\[ ... \\])."""
    doc.append(Math(data=[NoEscape(latex)], escape=False))


def alineadas(doc, lineas):
    """Varias ecuaciones alineadas en '&'."""
    doc.append(NoEscape(r"\begin{align*}" + r" \\[6pt] ".join(lineas) + r"\end{align*}"))


def guardar(doc, nombre, pdf=True):
    """Guarda <nombre>.tex y, si es posible, compila <nombre>.pdf."""
    if pdf:
        # Primero pdflatex (no necesita Perl); si falla, el compilador por defecto de PyLaTeX (latexmk).
        for compilador in ("pdflatex", None):
            try:
                doc.generate_pdf(nombre, clean_tex=False, compiler=compilador)
                print(f"Generados {nombre}.tex y {nombre}.pdf")
                return
            except Exception as error:
                ultimo = error.__class__.__name__
        print(f"No se pudo compilar el PDF ({ultimo}). Se guarda solo el .tex")
    doc.generate_tex(nombre)
    print(f"Generado {nombre}.tex")