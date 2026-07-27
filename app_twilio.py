from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from src.cerebro import Brain

load_dotenv()

app = Flask(__name__)
bot = Brain()


def _extraer_texto_respuesta(respuesta):
    if isinstance(respuesta, dict):
        return respuesta.get("texto", "")
    return str(respuesta)


@app.route('/webhook', methods=['POST'])
def webhook():
    """Recibe mensajes de WhatsApp via Twilio y responde."""
    mensaje_entrante = request.values.get('Body', '').strip()
    telefono_usuario = request.values.get('From', '').replace('whatsapp:', '')

    print(f"Mensaje de {telefono_usuario}: {mensaje_entrante}")

    respuesta_bot = bot.procesar_mensaje(mensaje_entrante, telefono_usuario)
    texto = _extraer_texto_respuesta(respuesta_bot)

    resp = MessagingResponse()
    resp.message(texto)

    print(f"Respuesta: {texto}")
    return str(resp)


@app.route('/webhook', methods=['GET'])
def verificar():
    return "Webhook activo", 200


@app.route('/', methods=['GET'])
def inicio():
    return """
    <h1>ChatBot Almacen Oportunidades</h1>
    <p>El servidor esta activo y listo para recibir mensajes de WhatsApp.</p>
    <p>Endpoint: <code>/webhook</code></p>
    """, 200


if __name__ == '__main__':
    print("=" * 50)
    print("Servidor Flask - WhatsApp via Twilio")
    print("=" * 50)
    print("Endpoint: http://localhost:5000/webhook")
    print("=" * 50)
    app.run(port=5000, debug=True)
