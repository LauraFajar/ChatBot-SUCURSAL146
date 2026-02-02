import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.inventario import InventarioService

# Cargar variables de entorno (API KEY)
load_dotenv()

class Brain:
    def __init__(self):
        self.inventario = InventarioService()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.sesiones = {} 
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def _get_session(self, telefono):
        if telefono not in self.sesiones:
            self.sesiones[telefono] = {'estado': 'normal', 'carrito': [], 'temp_producto': None}
        return self.sesiones[telefono]

    def procesar_mensaje(self, mensaje_usuario, telefono):
        session = self._get_session(telefono)
        mensaje = mensaje_usuario.lower().strip()
        estado = session.get('estado')

        # --- FLOW: FINALIZAR COMPRA (Captura de datos) ---
        if estado == 'pidiendo_datos':
            # Esperamos: "Nombre, Dirección"
            datos = mensaje_usuario 
            producto_interes = session.get('temp_producto', 'Varios productos')
            
            # Registramos la venta
            exito = self.inventario.crear_orden(telefono, datos, datos, producto_interes, "Por confirmar")
            
            session['estado'] = 'normal'
            session['temp_producto'] = None
            
            if exito:
                return "✅ ¡Pedido registrado! Un asesor revisará tu orden y te contactará para el pago y envío. ¡Gracias por elegir LAGOBO!"
            else:
                return "⚠️ Hubo un error registrando tu pedido. Por favor intenta más tarde o llama al 3209891720."

        if "comprar" in mensaje or "quiero llevar" in mensaje:
            session['estado'] = 'pidiendo_datos'
            return "🛒 ¡Listo para enviar! Por favor escribe tu **Nombre Completo y Dirección de Envío** en un solo mensaje para generar la orden."

        palabras_activacion = ["precio", "cuesta", "vale", "buscar", "busco", "quiero", "necesito", "tienes", "hay", "stock"]
        
        palabras_clave_productos = ["lavadora", "nevera", "licuadora", "televisor", "tv", "microondas", "sony", "samsung", "lg", "oster", "haceb", "estufa", "horno", "air fryer", "cafetera"]
        producto_detectado = next((p for p in palabras_clave_productos if p in mensaje), None)
        if not producto_detectado and len(mensaje.split()) < 6 and not any(x in mensaje for x in ["hola", "gracias", "adios"]):
             producto_detectado = mensaje

        if producto_detectado:
            # Registrar interés en Sheets
            self.inventario.registrar_interes(telefono, mensaje_usuario)
            
            print(f"DEBUG: Buscando '{producto_detectado}'...")
            resultados = self.inventario.buscar_producto(producto_detectado)
            
            if resultados:
                respuesta = f"🔍 **Resultados para '{producto_detectado}':**\n"
                for p in resultados:
                    precio = p.get('precio', 0)
                    nombre = p.get('nombre', 'Producto')
                    stock = p.get('stock', 0)
                    estado_prod = "✅ Disponible" if int(stock) > 0 else "❌ Agotado"
                    try:
                        respuesta += f"- {nombre}: ${float(precio):,.0f} ({estado_prod})\n"
                    except:
                        respuesta += f"- {nombre}: ${precio} ({estado_prod})\n"
                
                respuesta += "\n🛒 Si quieres alguno, responde **'Comprar [Nombre]'**."
                session['temp_producto'] = f"Interés en: {producto_detectado}"
                return respuesta

        if self.model:
            try:
                prompt_sistema = (
                    "Eres un asistente de ventas amable para 'Electrodomésticos LAGOBO'. "
                    "Tu objetivo es vender. Si te preguntan por productos, invítalos a buscar diciendo 'precio de x'. "
                    "Si quieren comprar, diles que escriban 'comprar'. "
                    "Sé conciso y usa emojis. El numero de contacto es 3209891720."
                )
                response = self.model.generate_content(f"{prompt_sistema}\nUsuario: {mensaje_usuario}")
                return response.text
            except Exception as e:
                print(f"⚠️ Error IA: {e}")
                return "Hola, soy el asistente de LAGOBO. ¿En qué puedo ayudarte hoy? Puedes buscar productos como 'nevera', 'lavadora', etc."
        
        return "👋 Hola, bienvenido a LAGOBO. Escribe el nombre del electrodoméstico que buscas (ej: 'Lavadora Samsung')."

