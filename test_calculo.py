import unittest
from fractions import Fraction

from calculo import (TIPOS, det_laplace, eliminacion_gauss, inversa,
                     matriz_aleatoria, parse_matriz, producto)


class Pruebas(unittest.TestCase):
    def test_determinante_conocido(self):
        A = parse_matriz("2 1 3; 0 -1 4; 1 2 5")
        self.assertEqual(eliminacion_gauss(A)["det"], -19)

    def test_gauss_igual_a_laplace(self):
        for semilla in range(30):
            A = matriz_aleatoria("cuadrada", 4, 4, (-6, 6), semilla)
            self.assertEqual(eliminacion_gauss(A)["det"], det_laplace(A))

    def test_matriz_singular(self):
        r = eliminacion_gauss(parse_matriz("1 2; 2 4"))
        self.assertTrue(r["singular"])
        self.assertEqual(r["det"], 0)
        self.assertIsNone(inversa(parse_matriz("1 2; 2 4"))["inv"])

    def test_inversa(self):
        for semilla in range(30):
            A = matriz_aleatoria("cuadrada", 3, 3, (-5, 5), semilla)
            r = inversa(A)
            if r["det"] != 0:
                n = len(A)
                I = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
                self.assertEqual(producto(A, r["inv"]), I)

    def test_tipos(self):
        for t in TIPOS:
            M = matriz_aleatoria(t, 4, 5, (-9, 9), 1)
            f, c = len(M), len(M[0])
            if t == "fila": self.assertEqual(f, 1)
            if t == "columna": self.assertEqual(c, 1)
            if t == "rectangular": self.assertNotEqual(f, c)
            if t == "diagonal": self.assertTrue(all(M[i][j] == 0 for i in range(f) for j in range(c) if i != j))
            if t == "triangular_superior": self.assertTrue(all(M[i][j] == 0 for i in range(f) for j in range(c) if i > j))
            if t == "triangular_inferior": self.assertTrue(all(M[i][j] == 0 for i in range(f) for j in range(c) if i < j))
            if t == "identidad": self.assertTrue(all(M[i][j] == int(i == j) for i in range(f) for j in range(c)))
            if t == "nula": self.assertTrue(all(x == 0 for fila in M for x in fila))


if __name__ == "__main__":
    unittest.main()
