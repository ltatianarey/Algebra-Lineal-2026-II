"""Lógica de álgebra lineal (sin LaTeX): matrices aleatorias, Gauss, cofactores e inversa.

Se usan fracciones exactas (fractions.Fraction) para evitar errores de redondeo.
"""
import random
from fractions import Fraction

TIPOS = [
    "fila", "columna", "cuadrada", "rectangular", "diagonal",
    "triangular_superior", "triangular_inferior", "identidad", "nula",
]


# ---------------------------------------------------------------- utilidades
def a_fracciones(A):
    return [[Fraction(x) for x in fila] for fila in A]


def copiar(A):
    return [fila[:] for fila in A]


def es_cuadrada(A):
    return len(A) > 0 and all(len(fila) == len(A) for fila in A)


def transpuesta(A):
    return [list(col) for col in zip(*A)]


def producto(A, B):
    return [[sum(a * b for a, b in zip(fila, col)) for col in zip(*B)] for fila in A]


def parse_matriz(texto):
    """Convierte '1 2 3; 4 5 6' (o con comas, o fracciones como 1/2) en una matriz."""
    filas = [f.split() for f in texto.replace(",", " ").split(";") if f.strip()]
    M = [[Fraction(x) for x in fila] for fila in filas]
    if not M or any(len(fila) != len(M[0]) for fila in M):
        raise ValueError("La matriz debe tener todas las filas con el mismo número de elementos.")
    return M


# ------------------------------------------------------- matrices aleatorias
def matriz_aleatoria(tipo, filas=3, columnas=3, rango=(-9, 9), semilla=None):
    """Genera una matriz (lista de listas de enteros) del tipo pedido.

    tipo: uno de TIPOS. Para los tipos cuadrados se usa `filas` como orden.
    """
    if tipo not in TIPOS:
        raise ValueError(f"Tipo desconocido: {tipo}. Opciones: {', '.join(TIPOS)}")
    if rango[0] == 0 and rango[1] == 0:
        raise ValueError("El rango debe incluir algún entero distinto de cero.")
    rnd = random.Random(semilla)

    def cualquiera():
        return rnd.randint(*rango)

    def no_cero():
        v = 0
        while v == 0:
            v = rnd.randint(*rango)
        return v

    if tipo == "fila":
        return [[cualquiera() for _ in range(columnas)]]
    if tipo == "columna":
        return [[cualquiera()] for _ in range(filas)]
    if tipo == "cuadrada":
        return [[cualquiera() for _ in range(filas)] for _ in range(filas)]
    if tipo == "rectangular":
        if columnas == filas:
            columnas += 1
        return [[cualquiera() for _ in range(columnas)] for _ in range(filas)]
    if tipo == "nula":
        return [[0] * columnas for _ in range(filas)]

    n = filas
    if tipo == "identidad":
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    if tipo == "diagonal":
        return [[no_cero() if i == j else 0 for j in range(n)] for i in range(n)]
    if tipo == "triangular_superior":
        return [[(no_cero() if i == j else cualquiera()) if i <= j else 0 for j in range(n)] for i in range(n)]
    # triangular_inferior
    return [[(no_cero() if i == j else cualquiera()) if i >= j else 0 for j in range(n)] for i in range(n)]


# ------------------------------------------------------------- determinante
def eliminacion_gauss(A):
    """Reduce A a forma triangular superior y calcula det(A).

    Devuelve un diccionario con:
      pasos: lista de dicts {tipo: 'swap'|'suma', i, j, m, antes, despues}
      final: matriz triangular obtenida
      intercambios: número de intercambios de fila (cada uno cambia el signo)
      det: determinante (Fraction)
      singular: True si apareció una columna sin pivote (det = 0)
      columna_sin_pivote: índice (base 0) de esa columna, si aplica
    """
    M = a_fracciones(A)
    if not es_cuadrada(M):
        raise ValueError("El determinante solo está definido para matrices cuadradas.")
    n = len(M)
    pasos, intercambios = [], 0

    for k in range(n):
        p = next((i for i in range(k, n) if M[i][k] != 0), None)
        if p is None:
            return {"pasos": pasos, "final": M, "intercambios": intercambios,
                    "det": Fraction(0), "singular": True, "columna_sin_pivote": k}
        if p != k:
            antes = copiar(M)
            M[k], M[p] = M[p], M[k]
            intercambios += 1
            pasos.append({"tipo": "swap", "i": k, "j": p, "m": None,
                          "antes": antes, "despues": copiar(M)})
        for i in range(k + 1, n):
            if M[i][k] != 0:
                m = M[i][k] / M[k][k]
                antes = copiar(M)
                M[i] = [a - m * b for a, b in zip(M[i], M[k])]
                pasos.append({"tipo": "suma", "i": i, "j": k, "m": m,
                              "antes": antes, "despues": copiar(M)})

    det = Fraction((-1) ** intercambios)
    for k in range(n):
        det *= M[k][k]
    return {"pasos": pasos, "final": M, "intercambios": intercambios,
            "det": det, "singular": False, "columna_sin_pivote": None}


# ------------------------------------------------------------------ inversa
def menor(A, i, j):
    """Submatriz que resulta de eliminar la fila i y la columna j."""
    return [fila[:j] + fila[j + 1:] for k, fila in enumerate(A) if k != i]


def det_laplace(A):
    """Determinante por expansión de cofactores (se usa para los menores)."""
    n = len(A)
    if n == 0:
        return Fraction(1)
    if n == 1:
        return Fraction(A[0][0])
    return sum((-1) ** j * Fraction(A[0][j]) * det_laplace(menor(A, 0, j)) for j in range(n))


def cofactores(A):
    n = len(A)
    return [[(-1) ** (i + j) * det_laplace(menor(A, i, j)) for j in range(n)] for i in range(n)]


def inversa(A):
    """Devuelve dict con det, cof (cofactores), adj (adjunta) e inv (None si det = 0)."""
    M = a_fracciones(A)
    if not es_cuadrada(M):
        raise ValueError("Solo las matrices cuadradas tienen inversa.")
    det = eliminacion_gauss(M)["det"]
    cof = cofactores(M)
    adj = transpuesta(cof)
    inv = None if det == 0 else [[x / det for x in fila] for fila in adj]
    return {"det": det, "cof": cof, "adj": adj, "inv": inv}
