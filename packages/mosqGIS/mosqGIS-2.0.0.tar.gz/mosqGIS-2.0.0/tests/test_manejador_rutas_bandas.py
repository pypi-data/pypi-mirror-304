import unittest
from unittest.mock import patch, MagicMock
from mosqGIS.modulos.manejador.manejador_rutas_bandas import ManejadorRutasBandas


class TestManejadorRutasBandas(unittest.TestCase):

    @patch('subprocess.run')
    def setUp(self, mock_run):
        # Simular la salida del comando `ls` para las bandas
        self.carpeta_recortadas = "ruta/a/imagenes"

        # Simulamos la salida del comando ls para que devuelva rutas válidas
        mock_run.side_effect = [
            MagicMock(stdout='ruta/a/imagenes/B4.TIF\n', stderr='', returncode=0),  # Para B4
            MagicMock(stdout='ruta/a/imagenes/B5.TIF\n', stderr='', returncode=0),  # Para B5
            MagicMock(stdout='ruta/a/imagenes/B3.TIF\n', stderr='', returncode=0),  # Para B3
            MagicMock(stdout='ruta/a/imagenes/B6.TIF\n', stderr='', returncode=0),  # Para B6
            MagicMock(stdout='ruta/a/imagenes/B10.TIF\n', stderr='', returncode=0)  # Para B10
        ]

        # Inicializar la clase ManejadorRutasBandas
        self.manejador = ManejadorRutasBandas(self.carpeta_recortadas)

    def test_init_y_cargar_rutas(self):
        # Verifica que las rutas de las bandas B4, B5, B3, B6 y B10 se carguen correctamente
        self.assertEqual(self.manejador.rutas['B4'], 'ruta/a/imagenes/B4.TIF')
        self.assertEqual(self.manejador.rutas['B5'], 'ruta/a/imagenes/B5.TIF')
        self.assertEqual(self.manejador.rutas['B3'], 'ruta/a/imagenes/B3.TIF')
        self.assertEqual(self.manejador.rutas['B6'], 'ruta/a/imagenes/B6.TIF')
        self.assertEqual(self.manejador.rutas['B10'], 'ruta/a/imagenes/B10.TIF')

        # Verifica que las rutas de NDVI, NDWI, NDBI, NDBAI, y NDMI se establezcan correctamente
        self.assertEqual(self.manejador.rutas['NDVI'], "ruta/a/imagenes/ndvi.TIF")
        self.assertEqual(self.manejador.rutas['NDWI'], "ruta/a/imagenes/ndwi.TIF")
        self.assertEqual(self.manejador.rutas['NDBI'], "ruta/a/imagenes/ndbi.TIF")
        self.assertEqual(self.manejador.rutas['NDBAI'], "ruta/a/imagenes/ndbai.TIF")
        self.assertEqual(self.manejador.rutas['NDMI'], "ruta/a/imagenes/ndmi.TIF")

    def test_obtener_ruta(self):
        # Verifica que se obtenga la ruta correcta para una banda existente
        self.assertEqual(self.manejador.obtener_ruta('B4'), 'ruta/a/imagenes/B4.TIF')

        # Verifica que se obtenga None para una banda que no existe
        self.assertIsNone(self.manejador.obtener_ruta('B99'))  # Banda inexistente

    def test_establecer_ruta(self):
        # Verifica que se pueda establecer correctamente la ruta de una banda
        self.manejador.establecer_ruta('B4', 'nueva/ruta/B4.TIF')
        self.assertEqual(self.manejador.rutas['B4'], 'nueva/ruta/B4.TIF')


if __name__ == '__main__':
    unittest.main()
