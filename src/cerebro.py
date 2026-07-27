import os
from dotenv import load_dotenv
from src.inventario import InventarioService
from src.catalogo import CATALOGO
from src.catalogo_builder import obtener_categoria_por_alias

# Cargar variables de entorno
load_dotenv()


class Brain:
    def __init__(self):
        self.inventario = InventarioService()
        self.sesiones = {}
        self.catalogo = self._cargar_catalogo()
        origen = "MySQL (articulos)" if self._catalogo_desde_bd else "respaldo local"
        print(f"Cerebro del Bot inicializado. Catalogo cargado desde {origen}.")

    def _cargar_catalogo(self):
        catalogo_bd = self.inventario.construir_catalogo_desde_bd()
        if catalogo_bd:
            self._catalogo_desde_bd = True
            return catalogo_bd

        self._catalogo_desde_bd = False
        print("BD sin articulos: usando catalogo de respaldo en src/catalogo.py")
        return CATALOGO

    def recargar_catalogo(self):
        """Recarga el catalogo desde MySQL (util al actualizar articulos)."""
        self.catalogo = self._cargar_catalogo()
        return self.catalogo

    def _get_session(self, telefono):
        if telefono not in self.sesiones:
            self.sesiones[telefono] = self._nueva_sesion()
        return self.sesiones[telefono]

    def _nueva_sesion(self):
        return {
            'estado': 'INICIO',
            'categoria_clave': None,
            'categoria_datos': None,
            'subcategoria_id': None,
            'subcategoria_datos': None,
            'producto_id': None,
            'producto_datos': None,
            'metodo_pago': None,
            'financiera': None,
            'cedula_correo': None
        }

    def reset_session(self, telefono):
        self.recargar_catalogo()
        self.sesiones[telefono] = self._nueva_sesion()
        return self.sesiones[telefono]

    # -------------------------------------------------------------------------
    # Helpers para construir mensajes de menú
    # -------------------------------------------------------------------------

    def _menu_bienvenida(self):
        """Genera el menú principal de categorías."""
        lineas = [
            "👋 ¡Hola! Bienvenido a *Almacén Oportunidades* 🏠\n",
            "¿En qué electrodoméstico estás interesado hoy?\n"
        ]
        for i, (clave, item) in enumerate(self.catalogo.items(), start=1):
            lineas.append(f"{i}. {item['emoji']} {item['nombre']}")
        lineas.append("\n📝 Responde con el *número* o el *nombre* del artículo que deseas.")
        return "\n".join(lineas)

    def _menu_subcategorias(self, categoria_datos):
        """Genera el menú de subcategorías de una categoría."""
        nombre = categoria_datos['nombre']
        subcats = categoria_datos['subcategorias']
        lineas = [f"Excelente elección. 👍 ¿Qué tipo de *{nombre}* estás buscando?\n"]
        for sid, scat in subcats.items():
            lineas.append(f"{sid}. {scat['nombre']}")
        lineas.append("\n📝 Responde con el *número* de la opción que prefieres.")
        return "\n".join(lineas)

    def _menu_productos(self, subcategoria_datos, categoria_nombre):
        """Genera el menú de productos específicos dentro de una subcategoría."""
        lineas = [f"🛍️ Estos son los modelos disponibles en *{subcategoria_datos['nombre']}*:\n"]
        for pid, prod in subcategoria_datos['productos'].items():
            lineas.append(f"{pid}. {prod['nombre']} — *{prod['precio']}*")
        lineas.append("\n📝 Responde con el *número* del modelo que te interesa.")
        return "\n".join(lineas)

    def _respuesta_no_puedo_resolver(self):
        """Respuesta programada para consultas fuera del flujo establecido."""
        return {
            "texto": (
                "Lo siento, no puedo resolver tu duda en este momento. 😔\n\n"
                "Un asesor pronto se comunicará contigo para ayudarte de forma personalizada."
            ),
            "imagenes": []
        }

    # -------------------------------------------------------------------------
    # Procesador principal de mensajes
    # -------------------------------------------------------------------------

    def procesar_mensaje(self, mensaje_usuario, telefono):
        session = self._get_session(telefono)
        mensaje = mensaje_usuario.lower().strip()
        estado = session.get('estado', 'INICIO')

        # Permite reiniciar el flujo en cualquier momento
        if mensaje in ["inicio", "reiniciar", "menu", "menú", "reset", "hola", "hi"]:
            session = self.reset_session(telefono)
            estado = 'INICIO'

        # Respuesta programada para consultas fuera del flujo esperado
        mensajes_fuera_flujo = [
            "precio", "cuanto", "cuánto", "cost", "costo", "iva", "garantia",
            "entrega", "envio", "envío", "descuento", "oferta", "stock",
            "disponibilidad", "pregunta", "ayuda", "información", "informacion",
            "duda", "cuando", "horario", "direccion", "ubicacion", "ubicación"
        ]

        if estado in ['SELECCIONANDO_CATEGORIA', 'SELECCIONANDO_SUBCATEGORIA', 'SELECCIONANDO_PRODUCTO', 'MOSTRANDO_PRODUCTO', 'SELECCIONANDO_FINANCIERA', 'SOLICITANDO_CEDULA_CORREO']:
            if any(palabra in mensaje for palabra in mensajes_fuera_flujo):
                texto = (
                    "Lo siento, no puedo resolver tu duda en este momento. 😔\n\n"
                    "Un asesor pronto se comunicará contigo para ayudarte de forma personalizada."
                )
                return {"texto": texto, "imagenes": []}

        # =====================================================================
        # 1. INICIO: Mostrar menú de categorías
        # =====================================================================
        if estado == 'INICIO':
            session['estado'] = 'SELECCIONANDO_CATEGORIA'
            return {"texto": self._menu_bienvenida(), "imagenes": []}

        # =====================================================================
        # 2. SELECCIONANDO_CATEGORIA
        # =====================================================================
        elif estado == 'SELECCIONANDO_CATEGORIA':
            # Intentar detectar la categoría por alias o por número de posición
            clave, item = obtener_categoria_por_alias(mensaje, self.catalogo)

            # Si no encontró por alias, intenta por número de posición
            if not clave:
                try:
                    idx = int(mensaje)
                    claves = list(self.catalogo.keys())
                    if 1 <= idx <= len(claves):
                        clave = claves[idx - 1]
                        item = self.catalogo[clave]
                except ValueError:
                    pass

            if clave and item:
                session['categoria_clave'] = clave
                session['categoria_datos'] = item
                session['estado'] = 'SELECCIONANDO_SUBCATEGORIA'

                # Registrar interés en MySQL
                try:
                    self.inventario.registrar_interes(telefono, f"Categoría: {item['nombre']}")
                except Exception as e:
                    print(f"⚠️ Error registrando interés: {e}")

                texto = self._menu_subcategorias(item)
                return {"texto": texto, "imagenes": []}
            else:
                return self._respuesta_no_puedo_resolver()

        # =====================================================================
        # 3. SELECCIONANDO_SUBCATEGORIA (tipo/tamaño)
        # =====================================================================
        elif estado == 'SELECCIONANDO_SUBCATEGORIA':
            categoria_datos = session['categoria_datos']
            subcats = categoria_datos['subcategorias']

            subcat_id = None
            # Primero intentar por número directo
            if mensaje in subcats:
                subcat_id = mensaje
            else:
                # Intentar búsqueda parcial por nombre
                for sid, scat in subcats.items():
                    if mensaje in scat['nombre'].lower():
                        subcat_id = sid
                        break

            if subcat_id and subcat_id in subcats:
                subcat = subcats[subcat_id]
                session['subcategoria_id'] = subcat_id
                session['subcategoria_datos'] = subcat
                session['estado'] = 'SELECCIONANDO_PRODUCTO'

                try:
                    self.inventario.registrar_interes(
                        telefono, f"Subcategoría: {subcat['nombre']}"
                    )
                except Exception as e:
                    print(f"⚠️ Error registrando interés: {e}")

                texto = self._menu_productos(subcat, categoria_datos['nombre'])
                return {"texto": texto, "imagenes": []}
            else:
                return self._respuesta_no_puedo_resolver()

        # =====================================================================
        # 4. SELECCIONANDO_PRODUCTO (modelo específico)
        # =====================================================================
        elif estado == 'SELECCIONANDO_PRODUCTO':
            subcat = session['subcategoria_datos']
            productos = subcat['productos']

            prod_id = None
            if mensaje in productos:
                prod_id = mensaje
            else:
                # Búsqueda parcial por nombre del producto
                for pid, prod in productos.items():
                    if mensaje in prod['nombre'].lower():
                        prod_id = pid
                        break

            if prod_id and prod_id in productos:
                producto = productos[prod_id]
                if producto.get("disponible") is False:
                    return {
                        "texto": (
                            f"El producto *{producto['nombre']}* no está disponible en este momento.\n\n"
                            "Elige otro modelo de la lista o escribe *inicio* para volver al menú principal."
                        ),
                        "imagenes": [],
                    }

                session['producto_id'] = prod_id
                session['producto_datos'] = producto
                session['estado'] = 'MOSTRANDO_PRODUCTO'

                try:
                    self.inventario.registrar_interes(
                        telefono, f"Producto: {producto['nombre']}"
                    )
                except Exception as e:
                    print(f"⚠️ Error registrando interés: {e}")

                texto = (
                    f"✨ Has seleccionado: *{producto['nombre']}*\n\n"
                    f"{producto['descripcion_corta']}\n\n"
                    f"ℹ️ Escribe *'más información'* para ver todos los detalles.\n\n"
                    f"💳 ¿Deseas adquirirlo de *Contado* o *Financiado*?"
                )
                imagenes = producto.get('imagenes', [])
                return {"texto": texto, "imagenes": imagenes}
            else:
                return self._respuesta_no_puedo_resolver()

        # =====================================================================
        # 5. MOSTRANDO_PRODUCTO (más info, contado o financiado)
        # =====================================================================
        elif estado == 'MOSTRANDO_PRODUCTO':
            producto = session['producto_datos']

            # Pide más información
            if any(x in mensaje for x in [
                "mas info", "más info", "mas informacion", "más información",
                "detalles", "informacion", "amplia", "información"
            ]):
                texto = (
                    f"ℹ️ {producto['descripcion_amplia']}\n\n"
                    f"💳 ¿Deseas adquirirlo de *Contado* o *Financiado*?"
                )
                return {"texto": texto, "imagenes": []}

            # Volver al menú principal o a subcategorías
            elif any(x in mensaje for x in ["volver", "atras", "atrás", "regresar", "otro"]):
                session['estado'] = 'SELECCIONANDO_SUBCATEGORIA'
                texto = self._menu_subcategorias(session['categoria_datos'])
                return {"texto": texto, "imagenes": []}

            # Contado
            elif "contado" in mensaje or mensaje == "1":
                session['metodo_pago'] = 'Contado'
                session['estado'] = 'SOLICITANDO_CEDULA_CORREO'
                texto = (
                    f"💰 Precio de contado para *{producto['nombre']}*: *{producto['precio']}*\n\n"
                    f"📄 Para proceder con tu compra, por favor envíanos:\n"
                    f"1. *Foto de tu cédula de ciudadanía* (legible por ambos lados).\n"
                    f"2. Tu *correo electrónico*."
                )
                return {"texto": texto, "imagenes": []}

            # Financiado
            elif any(x in mensaje for x in ["financia", "credito", "crédito", "cuotas"]) or mensaje == "2":
                session['estado'] = 'SELECCIONANDO_FINANCIERA'
                texto = (
                    f"🏦 Opciones de financiación para *{producto['nombre']}*:\n\n"
                    f"1. 🟦 Addi\n"
                    f"2. 🟩 Sistecrédito\n"
                    f"3. 🟨 Sumaspay\n"
                    f"4. 🟥 Banco de Bogotá\n\n"
                    f"Responde con el número o nombre de la entidad financiera de tu preferencia."
                )
                return {"texto": texto, "imagenes": []}

            else:
                return self._respuesta_no_puedo_resolver()

        # =====================================================================
        # 6. SELECCIONANDO_FINANCIERA
        # =====================================================================
        elif estado == 'SELECCIONANDO_FINANCIERA':
            producto = session['producto_datos']
            entidad = None

            if "1" in mensaje or "addi" in mensaje:
                entidad = "Addi"
            elif "2" in mensaje or "sistecredito" in mensaje or "sistecrédito" in mensaje:
                entidad = "Sistecrédito"
            elif "3" in mensaje or "sumaspay" in mensaje or "sumas pay" in mensaje:
                entidad = "Sumaspay"
            elif "4" in mensaje or "banco" in mensaje or "bogota" in mensaje or "bogotá" in mensaje:
                entidad = "Banco de Bogotá"

            if entidad:
                session['financiera'] = entidad
                session['metodo_pago'] = f"Financiado ({entidad})"
                session['estado'] = 'SOLICITANDO_CEDULA_CORREO'
                texto = (
                    f"✅ Has seleccionado financiación con *{entidad}* para *{producto['nombre']}*.\n\n"
                    f"📄 Para gestionar la aprobación de tu crédito, por favor envíanos:\n"
                    f"1. *Foto de tu cédula de ciudadanía* (legible por ambos lados).\n"
                    f"2. Tu *correo electrónico*."
                )
                return {"texto": texto, "imagenes": []}
            else:
                return self._respuesta_no_puedo_resolver()

        # =====================================================================
        # 7. SOLICITANDO_CEDULA_CORREO
        # =====================================================================
        elif estado == 'SOLICITANDO_CEDULA_CORREO':
            session['cedula_correo'] = mensaje_usuario
            producto = session.get('producto_datos', {})
            metodo = session.get('metodo_pago', 'No especificado')
            prod_nombre = producto.get('nombre', 'Electrodoméstico')
            monto_total = producto.get('precio_num', 0)

            # Registrar orden en MySQL
            try:
                self.inventario.crear_orden(
                    telefono=telefono,
                    cliente=f"WA-{telefono}",
                    direccion=mensaje_usuario,
                    producto_info=f"{prod_nombre} | Metodo: {metodo}",
                    total=monto_total,
                    nombre_producto=prod_nombre,
                    id_articulo=producto.get("id_articulo"),
                )
            except Exception as e:
                print(f"⚠️ Error al registrar venta: {e}")

            session['estado'] = 'FINALIZADO'
            texto = (
                f"✅ *¡Pedido registrado exitosamente!*\n\n"
                f"📋 *Resumen de tu solicitud:*\n"
                f"• Producto: *{prod_nombre}*\n"
                f"• Precio: *{producto.get('precio', 'N/A')}*\n"
                f"• Método de pago: *{metodo}*\n\n"
                f"👨‍💼 *Un asesor comercial se comunicará contigo a la brevedad* "
                f"para verificar tu documento de identidad, correo electrónico y coordinar la entrega.\n\n"
                f"¡Gracias por preferir *Almacén Oportunidades*! 🌟\n\n"
                f"Si deseas hacer otra consulta, escribe *'inicio'*."
            )
            return {"texto": texto, "imagenes": []}

        # =====================================================================
        # 8. FINALIZADO
        # =====================================================================
        elif estado == 'FINALIZADO':
            texto = (
                f"👨‍💼 Tu solicitud ya está registrada y en proceso con uno de nuestros asesores.\n\n"
                f"Si deseas realizar otra cotización o ver más productos, escribe *'inicio'*."
            )
            return {"texto": texto, "imagenes": []}

        # Fallback por defecto
        return {
            "texto": "👋 Hola, bienvenido a *Almacén Oportunidades*. Escribe *'inicio'* para comenzar.",
            "imagenes": []
        }
