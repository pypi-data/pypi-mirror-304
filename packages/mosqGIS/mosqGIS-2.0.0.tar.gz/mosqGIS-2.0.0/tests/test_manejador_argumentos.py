import unittest
import argparse
from unittest.mock import patch
from mosqGIS.modulos.manejador.manejador_argumentos import ManejadorArgumentos

class TestManejadorArgumentos(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(carpeta_recortadas='Imagenes',
                                           carpeta_no_recortadas='Imagenes_recortadas',
                                           ruta_poligono='poligono.ghp',
                                           ruta_datos_ovitrampas='datos_ovitrampas_reales.csv'))
    def test_argumentos_completos(self, mock_args):
        manejador = ManejadorArgumentos()
        args = manejador.obtener_argumentos()
        self.assertEqual(args.carpeta_recortadas, 'Imagenes')
        self.assertEqual(args.carpeta_no_recortadas, 'Imagenes_recortadas')
        self.assertEqual(args.ruta_poligono, 'poligono.ghp')
        self.assertEqual(args.ruta_datos_ovitrampas, 'datos_ovitrampas_reales.csv')

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(carpeta_recortadas='recortadas',
                                           carpeta_no_recortadas=None,
                                           ruta_poligono=None,
                                           ruta_datos_ovitrampas=None))
    def test_argumentos_parciales(self, mock_args):
        manejador = ManejadorArgumentos()
        args = manejador.obtener_argumentos()
        self.assertEqual(args.carpeta_recortadas, 'recortadas')
        self.assertIsNone(args.carpeta_no_recortadas)
        self.assertIsNone(args.ruta_poligono)
        self.assertIsNone(args.ruta_datos_ovitrampas)

if __name__ == '__main__':
    unittest.main()
