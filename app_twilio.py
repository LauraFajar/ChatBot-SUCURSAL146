from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from src.cerebro import Brain

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Inicializar el cerebro del bot
bot = Brain()

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Recibe mensajes de WhatsApp vía Twilio y responde.
    """
    # Obtener el mensaje del usuario
    mensaje_entrante = request.values.get('Body', '').strip()
    telefono_usuario = request.values.get('From', '').replace('whatsapp:', '')
    
    print(f"📩 Mensaje de {telefono_usuario}: {mensaje_entrante}")
    
    # Procesar con el cerebro del bot
    respuesta_bot = bot.procesar_mensaje(mensaje_entrante, telefono_usuario)
    
    # Crear respuesta de Twilio
    resp = MessagingResponse()
    resp.message(respuesta_bot)
    
    print(f"🤖 Respuesta: {respuesta_bot}")
    
    return str(resp)

@app.route('/webhook', methods=['GET'])
def verificar():
    """
    Endpoint para verificar que el servidor está activo.
    """
    return "✅ Webhook activo", 200

@app.route('/', methods=['GET'])
def inicio():
    """
    Página de inicio simple.
    """
    return """
    <h1>🤖 ChatBot Almacén Oportunidades</h1>
    <p>El servidor está activo y listo para recibir mensajes de WhatsApp.</p>
    <p>Endpoint: <code>/webhook</code></p>
    """, 200

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Servidor Flask iniciado para WhatsApp (Twilio)")
    print("=" * 50)
    print("📱 Endpoint: http://localhost:5000/webhook")
    print("💡 No olvides ejecutar ngrok en otra terminal:")
    print("   ngrok http 5000")
    print("=" * 50)
    app.run(port=5000, debug=True)
