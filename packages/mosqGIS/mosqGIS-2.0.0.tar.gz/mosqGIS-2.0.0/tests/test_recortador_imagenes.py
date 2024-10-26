import unittest
import os
import shutil
import numpy as np
import rasterio
import geopandas as gpd
from shapely.geometry import Polygon
from unittest.mock import patch
from mosqGIS.modulos.procesador.procesador_imagenes import RecortadorImagenes, crop_tif

class TestRecortadorImagenes(unittest.TestCase):

    def setUp(self):
        """Configura las rutas y crea carpetas temporales para las pruebas."""
        self.carpeta_recortadas = "test/carpeta_recortadas"
        self.carpeta_no_recortadas = "test/carpeta_no_recortadas"
        self.ruta_poligono = "test/poligono.shp"

        os.makedirs(self.carpeta_no_recortadas, exist_ok=True)
        os.makedirs(self.carpeta_recortadas, exist_ok=True)

        # Crear un archivo TIFF de prueba
        self.create_test_tiff(os.path.join(self.carpeta_no_recortadas, "imagen_prueba.TIF"))

        # Crear un shapefile de prueba
        self.create_test_shapefile(self.ruta_poligono)

    def tearDown(self):
        """Limpia después de las pruebas eliminando las carpetas temporales."""
        shutil.rmtree("test", ignore_errors=True)

    def create_test_tiff(self, path):
        """Crea un archivo TIFF de prueba con información de CRS."""
        width = 10
        height = 10
        data = np.random.randint(0, 256, (height, width), dtype=np.uint8)

        # Definir el CRS (en este caso, EPSG:4326)
        transform = rasterio.transform.from_origin(0, 10, 1, 1)  # (west, north, xsize, ysize)

        with rasterio.open(path, 'w', driver='GTiff', height=height, width=width, count=1,
                           dtype='uint8', crs='EPSG:4326', transform=transform) as dst:
            dst.write(data, 1)

    def create_test_shapefile(self, path):
        """Crea un shapefile de prueba con un polígono simple."""
        polygon = Polygon([(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)])
        gdf = gpd.GeoDataFrame({'geometry': [polygon]}, crs="EPSG:4326")
        gdf.to_file(path, driver='ESRI Shapefile')

    def test_init(self):
        """Prueba la inicialización de la clase."""
        recortador = RecortadorImagenes(self.carpeta_recortadas, self.carpeta_no_recortadas, self.ruta_poligono)
        self.assertEqual(recortador.carpeta_recortadas, self.carpeta_recortadas)
        self.assertEqual(recortador.carpeta_no_recortadas, self.carpeta_no_recortadas)
        self.assertEqual(recortador.ruta_poligono, self.ruta_poligono)

    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("os.system")
    def test_recortar_imagenes_crear_carpeta(self, mock_system, mock_exists, mock_makedirs):
        """Prueba la creación de la carpeta de recortes si no existe."""
        mock_exists.return_value = False  # Simula que la carpeta no existe

        recortador = RecortadorImagenes(self.carpeta_recortadas, self.carpeta_no_recortadas, self.ruta_poligono)
        recortador.recortar_imagenes()

        # Verifica que se haya intentado crear la carpeta
        mock_makedirs.assert_called_once_with(self.carpeta_recortadas)

    @patch("os.listdir")
    @patch("mosqGIS.modulos.procesador.procesador_imagenes.crop_tif")  # Simular la función crop_tif
    @patch("os.makedirs")  # Asegúrate de estar usando el mock aquí también
    @patch("os.path.exists")
    def test_recortar_imagenes(self, mock_exists, mock_makedirs, mock_crop_tif, mock_listdir):
        """Prueba el recorte de imágenes sin ejecutar gdalwarp."""
        mock_exists.return_value = True  # Simula que la carpeta ya existe
        mock_listdir.return_value = ["imagen_prueba.TIF"]  # Simula que hay un archivo en la carpeta

        recortador = RecortadorImagenes(self.carpeta_recortadas, self.carpeta_no_recortadas, self.ruta_poligono)
        recortador.recortar_imagenes()

        # Verifica que se haya llamado a la función crop_tif
        mock_crop_tif.assert_called_once_with(
            os.path.join(self.carpeta_no_recortadas, "imagen_prueba.TIF"),
            os.path.join(self.carpeta_recortadas, "imagen_prueba.TIF"),
            self.ruta_poligono
        )

if __name__ == "__main__":
    unittest.main()
