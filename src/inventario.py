import csv
import os

from src.catalogo_builder import construir_catalogo_desde_articulos
from src.database import DatabaseService


class InventarioService:
    def __init__(self):
        self.db = DatabaseService()
        self.productos_backup = self._cargar_csv_respaldo()

    def _cargar_csv_respaldo(self, filepath="data/inventario.csv"):
        productos = []
        if os.path.exists(filepath):
            with open(filepath, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["precio"] = float(row.get("precio", 0) or 0)
                    if "stock" in row:
                        row["stock"] = int(row.get("stock", 0) or 0)
                    productos.append(row)
        return productos

    def obtener_todos_productos(self):
        """Obtiene productos desde MySQL o, si no hay datos, desde CSV local."""
        db_articulos = self.db.obtener_articulos()
        if db_articulos:
            return db_articulos
        return self.productos_backup

    def construir_catalogo_desde_bd(self):
        """Genera el catálogo conversacional desde la tabla articulos."""
        articulos = self.db.obtener_articulos()
        if articulos:
            return construir_catalogo_desde_articulos(articulos)

        if self.productos_backup:
            return construir_catalogo_desde_articulos(self.productos_backup)

        return None

    def buscar_producto(self, consulta):
        """Busca productos por nombre, referencia o categoría."""
        db_resultados = self.db.obtener_articulos(consulta)
        if db_resultados:
            return db_resultados

        productos = self.obtener_todos_productos()
        resultados = []
        consulta_lower = consulta.lower().strip()

        sinonimos = {
            "televisor": "tv",
            "televisores": "tv",
            "tele": "tv",
            "nevera": "refrigera",
            "refrigerador": "refrigera",
            "refri": "refrigera",
        }

        for original, reemplazo in sinonimos.items():
            if original in consulta_lower:
                consulta_lower = consulta_lower.replace(original, reemplazo)

        palabras_busqueda = consulta_lower.split()

        for producto in productos:
            nombre = str(producto.get("nombre", "")).lower()
            referencia = str(producto.get("referencia", "")).lower()
            categoria = str(producto.get("categoria", "")).lower()
            texto_completo = f"{nombre} {referencia} {categoria}"

            if any(palabra in texto_completo for palabra in palabras_busqueda):
                resultados.append(producto)

        return resultados

    def registrar_interes(self, telefono, busqueda):
        """Registra qué busca el cliente en MySQL."""
        self.db.registrar_interes(telefono, busqueda)

    def crear_orden(
        self,
        telefono,
        cliente,
        direccion,
        producto_info,
        total,
        nombre_producto=None,
        id_articulo=None,
    ):
        """Crea una orden de venta en MySQL."""
        precio_monto = 0.0
        if isinstance(total, (int, float)):
            precio_monto = float(total)

        if id_articulo is None and nombre_producto:
            resultados = self.db.obtener_articulos(nombre_producto)
            if resultados:
                articulo = resultados[0]
                id_articulo = articulo.get("id_articulo")
                print(f"Articulo encontrado en BD: id={id_articulo}")
            else:
                print(
                    f"Articulo '{nombre_producto}' no encontrado en tabla articulos. "
                    "detalle_ventas se registrará sin FK."
                )

        self.db.crear_venta(
            telefono=telefono,
            datos_cliente=f"Cliente: {cliente} - Dir/Datos: {direccion}",
            producto_nombre=producto_info,
            total_monto=precio_monto,
            id_articulo=id_articulo,
        )
        return True
