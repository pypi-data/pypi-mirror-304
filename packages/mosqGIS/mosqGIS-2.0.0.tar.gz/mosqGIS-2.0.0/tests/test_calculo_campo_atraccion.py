import unittest
import numpy as np
from mosqGIS.modulos.calculador.calculador_campo_atraccion import CalculadorCampoAtraccion
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
class TestCalculadorCampoAtraccion(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial del test. Crea una matriz de urbanización de ejemplo
        y una carpeta simulada para las imágenes recortadas.
        """
        self.carpeta_recortadas = "carpeta_fake"
        # Matriz binaria donde 1 indica presencia de viviendas, y 0 indica ausencia
        self.urbanizacion = np.array([
            [0, 1, 0, 0, 1, 0, 0],
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 1, 0],
            [1, 0, 0, 1, 1, 0, 1],
            [0, 1, 0, 0, 1, 0, 0]
        ])

        self.calculador = CalculadorCampoAtraccion(self.carpeta_recortadas, self.urbanizacion)

    def test_calcular_mapa(self):
        """
        Verifica que el cálculo del campo de atracción retorna una matriz
        con los valores esperados de atracción basados en la urbanización.
        """
        resultado = self.calculador.calcular_mapa()
        # Verificar que el resultado tiene las mismas dimensiones que la matriz original
        self.assertEqual(resultado.shape, self.urbanizacion.shape)

        # Verificar que la suma de la matriz de atracción es mayor a 0
        self.assertGreater(np.sum(resultado), 0, "El campo de atracción debe tener valores mayores a 0")

    def test_valores_atraccion(self):
        """
        Verifica que los valores del campo de atracción estén dentro del rango esperado [0,1].
        """
        resultado = self.calculador.calcular_mapa()
        # Verificar que los valores están en el rango [0, 1]
        self.assertTrue(np.all(resultado >= 0) and np.all(resultado <= 1), "Los valores de atracción deben estar entre 0 y 1")

if __name__ == '__main__':
    unittest.main()
