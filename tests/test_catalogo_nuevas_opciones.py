import unittest

from src.catalogo import CATALOGO


class CatalogoNuevasOpcionesTest(unittest.TestCase):
    def test_productos_nuevos_de_neveras_y_congeladores_estan_en_catalogo(self):
        nevera = CATALOGO["nevera"]

        self.assertIn("4", nevera["subcategorias"])
        self.assertIn("5", nevera["subcategorias"])

        subcat_avanzadas = nevera["subcategorias"]["4"]["productos"]
        subcat_congeladores = nevera["subcategorias"]["5"]["productos"]

        self.assertIn("1", subcat_avanzadas)
        self.assertIn("2", subcat_avanzadas)
        self.assertIn("3", subcat_avanzadas)

        nombres_avanzadas = {producto["nombre"] for producto in subcat_avanzadas.values()}
        self.assertIn("Nevecón Midea MDR700FGM45CO2", nombres_avanzadas)
        self.assertIn("Nevecón LG 519 Litros (6551BPD.AHSCCLM)", nombres_avanzadas)
        self.assertIn("Refrigerador Electrolux 421 Litros (ERQU4DE3HWS 421)", nombres_avanzadas)

        nombres_congeladores = {producto["nombre"] for producto in subcat_congeladores.values()}
        self.assertIn("Congelador Horizontal Challenger CH-100 (97L)", nombres_congeladores)
        self.assertIn("Congelador Horizontal Electrolux (EFH70S3CSAV)", nombres_congeladores)
        self.assertIn("Congelador Horizontal Inducol Industrial (CH-DPB350BL1)", nombres_congeladores)


if __name__ == "__main__":
    unittest.main()
