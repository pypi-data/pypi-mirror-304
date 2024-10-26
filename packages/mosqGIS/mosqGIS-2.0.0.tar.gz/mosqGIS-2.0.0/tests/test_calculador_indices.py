import unittest
import rasterio
import numpy as np
import os
from mosqGIS.modulos.calculador.calculo_indices import calcular_ndvi, calcular_ndwi, calcular_ndbi, calcular_ndbai, calcular_ndmi

class TestCalculadorIndices(unittest.TestCase):

    def setUp(self):
        # Crear archivos de prueba en memoria
        self.b4_file = 'banda4.tif'
        self.b5_file = 'banda5.tif'
        self.b3_file = 'banda3.tif'
        self.b6_file = 'banda6.tif'
        self.b10_file = 'banda10.tif'

        # Generar datos sintéticos de 100x100
        self.data_b4 = np.random.rand(100, 100).astype('float32')  # Banda 4 (rojo)
        self.data_b5 = np.random.rand(100, 100).astype('float32')  # Banda 5 (infrarrojo cercano)
        self.data_b3 = np.random.rand(100, 100).astype('float32')  # Banda 3 (verde)
        self.data_b6 = np.random.rand(100, 100).astype('float32')  # Banda 6 (infrarrojo de onda corta)
        self.data_b10 = np.random.rand(100, 100).astype('float32')  # Banda 10 (térmica)

        self.create_raster(self.b4_file, self.data_b4)
        self.create_raster(self.b5_file, self.data_b5)
        self.create_raster(self.b3_file, self.data_b3)
        self.create_raster(self.b6_file, self.data_b6)
        self.create_raster(self.b10_file, self.data_b10)

    def tearDown(self):
        # Eliminar archivos de prueba
        for file in [self.b4_file, self.b5_file, self.b3_file, self.b6_file, self.b10_file]:
            if os.path.exists(file):
                os.remove(file)

    def create_raster(self, filename, data):
        """Crea un archivo raster para pruebas."""
        with rasterio.open(
                filename,
                'w',
                driver='GTiff',
                height=data.shape[0],
                width=data.shape[1],
                count=1,
                dtype=data.dtype,
                crs='EPSG:4326',
                transform=rasterio.transform.from_origin(0, 100, 1, 1),
        ) as dst:
            dst.write(data, 1)

    def test_calcular_ndvi(self):
        output_file = 'ndvi_output.tif'
        calcular_ndvi(self.b4_file, self.b5_file, output_file)

        with rasterio.open(output_file) as src:
            result = src.read(1)
            expected = np.where(
                (self.data_b5 + self.data_b4) == 0,
                0,
                (self.data_b5 - self.data_b4) / (self.data_b5 + self.data_b4)  # Cálculo manual
            )
            np.testing.assert_array_almost_equal(result, expected, decimal=5)  # Verificar resultados
        os.remove(output_file)

    def test_calcular_ndwi(self):
        output_file = 'ndwi_output.tif'
        calcular_ndwi(self.b3_file, self.b5_file, output_file)

        with rasterio.open(output_file) as src:
            result = src.read(1)
            expected = np.where(
                (self.data_b5 + self.data_b3) == 0,
                0,
                (self.data_b3 - self.data_b5) / (self.data_b3 + self.data_b5)  # Cálculo manual
            )
            np.testing.assert_array_almost_equal(result, expected, decimal=5)  # Verificar resultados
        os.remove(output_file)

    def test_calcular_ndbi(self):
        output_file = 'ndbi_output.tif'
        calcular_ndbi(self.b5_file, self.b6_file, output_file)

        with rasterio.open(output_file) as src:
            result = src.read(1)
            expected = np.where(
                (self.data_b5 + self.data_b6) == 0,
                0,
                (self.data_b6 - self.data_b5) / (self.data_b6 + self.data_b5)  # Cálculo manual
            )
            np.testing.assert_array_almost_equal(result, expected, decimal=5)  # Verificar resultados
        os.remove(output_file)

    def test_calcular_ndbai(self):
        output_file = 'ndbai_output.tif'
        calcular_ndbai(self.b6_file, self.b10_file, output_file)

        with rasterio.open(output_file) as src:
            result = src.read(1)
            expected = np.where(
                (self.data_b6 + self.data_b10) == 0,
                0,
                (self.data_b6 - self.data_b10) / (self.data_b6 + self.data_b10)  # Cálculo manual
            )
            np.testing.assert_array_almost_equal(result, expected, decimal=5)  # Verificar resultados
        os.remove(output_file)

    def test_calcular_ndmi(self):
        output_file = 'ndmi_output.tif'
        calcular_ndmi(self.b5_file, self.b6_file, output_file)

        with rasterio.open(output_file) as src:
            result = src.read(1)
            expected = np.where(
                (self.data_b5 + self.data_b6) == 0,
                0,
                (self.data_b5 - self.data_b6) / (self.data_b5 + self.data_b6)  # Cálculo manual
            )
            np.testing.assert_array_almost_equal(result, expected, decimal=5)  # Verificar resultados
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
