import os
from google import genai
from google.genai import types
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
            try:
                self.client = genai.Client(api_key=self.api_key)
                self.model = None  # Se usará client.models.generate_content directamente
                print("✅ Cliente Gemini inicializado")
            except Exception as e:
                print(f"⚠️ Error cargando Gemini: {e}")
                self.client = None
        else:
            self.client = None

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
                return "✅ ¡Pedido registrado! Un asesor revisará tu orden y te contactará para el pago y envío. ¡Gracias por elegir Almacén Oportunidades!"
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
                respuesta = f"🔍 **Encontré estos productos:**\n\n"
                for p in resultados[:5]:  # Limitar a 5 resultados
                    referencia = p.get('referencia', 'N/A')
                    nombre = p.get('nombre', 'Producto')
                    estado = p.get('estado', 'Consultar')
                    
                    # Icono según disponibilidad
                    icono = "✅"
                    if any(x in estado.lower() for x in ['no', 'agotado', '0']):
                        icono = "❌"
                    
                    respuesta += f"{icono} *{nombre}*\n   Ref: {referencia}\n   Estado: {estado}\n\n"
                
                respuesta += "💰 Para consultar precios y comprar, escribe *'Comprar [nombre del producto]'* o llama al 3209891720."
                session['temp_producto'] = f"{producto_detectado}"
                return respuesta
            else:
                # No se encontró, dejar que la IA responda
                pass

        if self.client:
            try:
                prompt_sistema = (
                    "Eres un asistente virtual de ventas amable y profesional de 'Almacén Oportunidades'. "
                    "Responde siempre en español, de forma concisa y usando emojis cuando sea apropiado. "
                    "\n\n"
                    "=== INFORMACIÓN OFICIAL DEL ALMACÉN (usa SOLO esta información, nunca inventes datos) ===\n"
                    "📍 Dirección: Calle 7 # 5-45 Centro, Almacén Oportunidades, Pitalito.\n"
                    "📞 Teléfono: 3185216489\n"
                    "🕐 Horarios de atención:\n"
                    "   - Lunes y Martes: 8:00 a.m. - 6:00 p.m.\n"
                    "   - Miércoles a Sábado: 9:00 a.m. - 6:00 p.m.\n"
                    "   - Domingos: Cerrado.\n"
                    "💳 Métodos de pago: Contado o convenio (Addi, Sistecredito, Sumas Pay).\n"
                    "🚚 Envíos:\n"
                    "   - A nivel nacional.\n"
                    "   - En Pitalito (zona urbana): entrega a domicilio con transportadores propios del almacén.\n"
                    "=== FIN DE INFORMACIÓN OFICIAL ===\n\n"
                    "Tu objetivo principal es ayudar a los clientes a encontrar productos y concretar ventas. "
                    "Si preguntan por un producto, invítalos a buscarlo escribiendo el nombre (ej: 'nevera', 'lavadora'). "
                    "Si quieren comprar, diles que escriban 'comprar'. "
                    "Si te preguntan algo que no sabes o no está en la información oficial, di que se comuniquen al 3185216489."
                )
                response = self.client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=f"{prompt_sistema}\nUsuario: {mensaje_usuario}"
                )
                return response.text
            except Exception as e:
                print(f"⚠️ Error IA: {e}")
                return "Hola, soy el asistente de Almacén Oportunidades. ¿En qué puedo ayudarte hoy? Puedes buscar productos como 'nevera', 'lavadora', etc."
        
        return "👋 Hola, bienvenido a Almacén Oportunidades. Escribe el nombre del electrodoméstico que buscas (ej: 'Lavadora Samsung')."

