import os
from dotenv import load_dotenv

load_dotenv()

# Intentar importar conectores MySQL
mysql_driver = None
try:
    import pymysql
    mysql_driver = 'pymysql'
except ImportError:
    try:
        import mysql.connector
        mysql_driver = 'mysql.connector'
    except ImportError:
        mysql_driver = None


class DatabaseService:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "almacen_oportunidades")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.driver = mysql_driver

    def _get_connection(self):
        if not self.driver:
            return None

        try:
            if self.driver == 'pymysql':
                import pymysql
                conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    autocommit=True,
                    cursorclass=pymysql.cursors.DictCursor
                )
                return conn
            elif self.driver == 'mysql.connector':
                import mysql.connector
                conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    autocommit=True,
                )
                return conn
        except Exception as e:
            # print(f"⚠️ Error conectando a MySQL: {e}")
            return None

    def _cursor(self, conn):
        if self.driver == 'mysql.connector':
            return conn.cursor(dictionary=True)
        return conn.cursor()

    def obtener_o_crear_cliente(self, telefono, nombre=None, direccion=None):
        """Busca un cliente por teléfono o lo crea en la tabla 'clientes'."""
        conn = self._get_connection()
        if not conn:
            return None

        try:
            with self._cursor(conn) as cursor:
                # Buscar cliente por teléfono
                cursor.execute("SELECT * FROM clientes WHERE telefono = %s", (telefono,))
                cliente = cursor.fetchone()

                if cliente:
                    # Actualizar si se proveen nombre o dirección
                    if nombre or direccion:
                        nombre_final = nombre or cliente.get('nombre')
                        direccion_final = direccion or cliente.get('direccion')
                        cursor.execute(
                            "UPDATE clientes SET nombre = %s, direccion = %s WHERE id_cliente = %s",
                            (nombre_final, direccion_final, cliente['id_cliente'])
                        )
                    return cliente.get('id_cliente')
                else:
                    # Crear nuevo cliente
                    nombre_val = nombre or f"Cliente WhatsApp {telefono}"
                    direccion_val = direccion or "Por especificar"
                    cursor.execute(
                        "INSERT INTO clientes (telefono, nombre, direccion) VALUES (%s, %s, %s)",
                        (telefono, nombre_val, direccion_val)
                    )
                    return cursor.lastrowid
        except Exception as e:
            print(f"❌ Error DB en obtener_o_crear_cliente: {e}")
            return None
        finally:
            conn.close()

    def registrar_interes(self, telefono, termino_busqueda):
        """Inserta la búsqueda de un cliente en la tabla 'intereses'."""
        conn = self._get_connection()
        if not conn:
            return False

        try:
            id_cliente = self.obtener_o_crear_cliente(telefono)
            if not id_cliente:
                return False

            with self._cursor(conn) as cursor:
                cursor.execute(
                    "INSERT INTO intereses (id_cliente, termino_busqueda, fecha_busqueda) VALUES (%s, %s, NOW())",
                    (id_cliente, termino_busqueda)
                )
                print(f"✅ Interés registrado en MySQL para cliente ID {id_cliente}: '{termino_busqueda}'")
                return True
        except Exception as e:
            print(f"❌ Error DB en registrar_interes: {e}")
            return False
        finally:
            conn.close()

    def obtener_articulos(self, termino=None):
        """Consulta productos de la tabla 'articulos'."""
        conn = self._get_connection()
        if not conn:
            return []

        try:
            with self._cursor(conn) as cursor:
                if termino:
                    query = "SELECT * FROM articulos WHERE LOWER(nombre) LIKE %s OR LOWER(categoria) LIKE %s OR LOWER(referencia) LIKE %s"
                    param = f"%{termino.lower()}%"
                    cursor.execute(query, (param, param, param))
                else:
                    cursor.execute("SELECT * FROM articulos")
                
                rows = cursor.fetchall()
                return rows
        except Exception as e:
            print(f"❌ Error DB en obtener_articulos: {e}")
            return []
        finally:
            conn.close()

    def crear_venta(self, telefono, datos_cliente, producto_nombre, total_monto, id_articulo=None):
        """Crea un registro en la tabla 'ventas' y opcionalmente en 'detalle_ventas'."""
        conn = self._get_connection()
        if not conn:
            return False

        try:
            id_cliente = self.obtener_o_crear_cliente(telefono, direccion=datos_cliente)
            if not id_cliente:
                return False

            with self._cursor(conn) as cursor:
                # 1. Insertar en tabla 'ventas'
                cursor.execute(
                    "INSERT INTO ventas (id_cliente, fecha_venta, total) VALUES (%s, NOW(), %s)",
                    (id_cliente, total_monto)
                )
                id_venta = cursor.lastrowid

                # 2. Insertar en tabla 'detalle_ventas' si se tiene el id_articulo
                if id_articulo:
                    cursor.execute(
                        "INSERT INTO detalle_ventas (id_venta, id_articulo, cantidad, precio_item) VALUES (%s, %s, %s, %s)",
                        (id_venta, id_articulo, 1, total_monto)
                    )

                print(f"✅ Venta ID {id_venta} creada exitosamente en MySQL para cliente ID {id_cliente}")
                return True
        except Exception as e:
            print(f"❌ Error DB en crear_venta: {e}")
            return False
        finally:
            conn.close()
