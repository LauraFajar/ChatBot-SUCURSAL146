import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import csv

class InventarioService:
    def __init__(self):
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.creds_file = "credenciales_sheets.json"
        self.client = None
        self.sheet = None
        self.usando_backup = False
        
        # Intentar conectar a Google Sheets
        try:
            if os.path.exists(self.creds_file):
                self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, self.scope)
                self.client = gspread.authorize(self.creds)
                # Intenta abrir la hoja usando el ID proporcionado
                SPREADSHEET_ID = "1iZ0viBh34WIQc_Pq6Zqm0kthaC766wa3bslNvyLe0xU"
                self.doc = self.client.open_by_key(SPREADSHEET_ID)
                self.sheet = self.doc.sheet1 
                print("✅ Conexión exitosa con Google Sheets (LAGOBO)")
            else:
                print(f"⚠️ No encontré {self.creds_file}. Usando modo respaldo CSV.")
                self.usando_backup = True
        except Exception as e:
            print(f"⚠️ Error conectando a Sheets: {e}. Usando modo respaldo CSV.")
            self.usando_backup = True
            
        # Si falló Sheets, cargamos el CSV local como respaldo
        self.productos_backup = self._cargar_csv_respaldo() if self.usando_backup else []

    def _cargar_csv_respaldo(self, filepath="data/inventario.csv"):
        productos = []
        if os.path.exists(filepath):
            with open(filepath, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['precio'] = float(row['precio'])
                    row['stock'] = int(row['stock'])
                    productos.append(row)
        return productos

    def obtener_todos_productos(self):
        """Obtiene la lista fresca de productos"""
        if self.usando_backup:
            return self.productos_backup
        try:
            # Obtener todos los valores desde la hoja
            all_values = self.sheet.get_all_values()
            if not all_values or len(all_values) < 2:
                return []
            
            headers = all_values[0]
            productos = []
            
            for row in all_values[1:]:  
                if len(row) >= 2 and row[0] and row[1]:  
                    productos.append({
                        'referencia': row[0].strip(),
                        'nombre': row[1].strip()
                    })
            
            print(f"DEBUG: Leídos {len(productos)} productos del Sheet")
            return productos
        except Exception as e:
            print(f"Error leyendo Sheet: {e}")
            import traceback
            traceback.print_exc()
            return []

    def buscar_producto(self, consulta):
        """Busca productos por nombre o referencia"""
        productos = self.obtener_todos_productos()
        resultados = []
        consulta_lower = consulta.lower().strip()
        
        # Diccionario de sinónimos para búsqueda más inteligente
        sinonimos = {
            'televisor': 'tv',
            'televisores': 'tv',
            'tele': 'tv',
            'nevera': 'refrigera',
            'refrigerador': 'refrigera',
            'refri': 'refrigera'
        }
        
        # Reemplazar sinónimos
        for original, reemplazo in sinonimos.items():
            if original in consulta_lower:
                consulta_lower = consulta_lower.replace(original, reemplazo)
        
        # Dividir en palabras para búsqueda más flexible
        palabras_busqueda = consulta_lower.split()
        
        for p in productos:
            # Buscar en nombre y referencia
            nombre = str(p.get('nombre', '')).lower()
            referencia = str(p.get('referencia', '')).lower()
            texto_completo = f"{nombre} {referencia}"
            
            # Si al menos una palabra de la búsqueda aparece en el producto
            if any(palabra in texto_completo for palabra in palabras_busqueda):
                resultados.append(p)
        
        print(f"DEBUG: Búsqueda '{consulta}' (normalizado: '{consulta_lower}') encontró {len(resultados)} resultados")
        return resultados

    def verificar_stock(self, producto_id):
        """Verifica stock en tiempo real"""
        # Nota: En un sistema real de alto tráfico, leeríamos solo la celda específica.
        # Por simplicidad ahora leemos todo.
        productos = self.obtener_todos_productos()
        for p in productos:
            if str(p.get('id')) == str(producto_id):
                return int(p.get('stock', 0))
        return 0

    def crear_link_pago_simulado(self, total):
        return f"https://pagos-prueba.com/checkout?monto={total}"

    def _get_or_create_worksheet(self, title):
        try:
            return self.doc.worksheet(title)
        except gspread.WorksheetNotFound:
            return self.doc.add_worksheet(title=title, rows=100, cols=10)

    def registrar_interes(self, telefono, busqueda):
        """Registra qué busca el cliente para análisis comercial"""
        if self.usando_backup: return
        try:
            sheet_interes = self._get_or_create_worksheet("Intereses")
            # Si está vacía, poner cabecera
            if not sheet_interes.get_all_values():
                sheet_interes.append_row(["Fecha", "Telefono", "Busqueda"])
            
            from datetime import datetime
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet_interes.append_row([fecha, telefono, busqueda])
        except Exception as e:
            print(f"Error registrando interés: {e}")

    def crear_orden(self, telefono, nombre, direccion, producto_info, total):
        """Crea una orden de venta en la hoja 'Ventas'"""
        if self.usando_backup: return False
        try:
            sheet_ventas = self._get_or_create_worksheet("Ventas")
            if not sheet_ventas.get_all_values():
                sheet_ventas.append_row(["Fecha", "Cliente", "Telefono", "Direccion", "Producto", "Total", "Estado"])
            
            from datetime import datetime
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet_ventas.append_row([fecha, nombre, telefono, direccion, producto_info, total, "Pendiente de Pago"])
            return True
        except Exception as e:
            print(f"Error creando orden: {e}")
            return False

# Prueba rápida
if __name__ == "__main__":
    s = InventarioService()
    print(s.buscar_producto("nevera"))
