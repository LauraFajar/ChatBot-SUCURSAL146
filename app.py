from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from src.cerebro import Brain

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de WhatsApp desde .env
# Necesitarás agregar estas variables a tu archivo .env
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# Inicializar el cerebro una sola vez
bot = Brain()

def enviar_mensaje_whatsapp(telefono, texto):
    """
    Envía un mensaje de texto a un número de WhatsApp usando la API oficial.
    """
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("ERROR: Faltan credenciales de WhatsApp en .env")
        return

    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "text",
        "text": {"body": texto}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        # print("Mensaje enviado:", response.json())
    except Exception as e:
        print(f"Error enviando mensaje a WhatsApp: {e}")
        if 'response' in locals():
            print(response.text)

@app.route('/webhook', methods=['GET'])
def verificar_token():
    """
    Verificación del webhook para WhatsApp.
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("Webhook verificado correctamente.")
            return challenge, 200
        else:
            return "Token de verificación incorrecto", 403
    return "Faltan parámetros", 400

@app.route('/webhook', methods=['POST'])
def recibir_mensaje():
    """
    Recibe mensajes de WhatsApp y responde usando el cerebro del bot.
    """
    body = request.get_json()

    print("Evento recibido:", body) # Debug

    try:
        # Verificar si es un mensaje de WhatsApp válido
        if (
            body.get("object") == "whatsapp_business_account" and
            body.get("entry") and
            body["entry"][0].get("changes") and
            body["entry"][0]["changes"][0].get("value") and
            body["entry"][0]["changes"][0]["value"].get("messages")
        ):
            change = body["entry"][0]["changes"][0]["value"]
            mensaje_info = change["messages"][0]
            
            # Solo procesamos mensajes de texto por ahora
            if mensaje_info["type"] == "text":
                telefono_usuario = mensaje_info["from"]
                texto_usuario = mensaje_info["text"]["body"]
                
                print(f"Mensaje de {telefono_usuario}: {texto_usuario}")

                # Procesar con el cerebro
                respuesta_bot = bot.procesar_mensaje(texto_usuario, telefono_usuario)
                
                # Responder a WhatsApp
                enviar_mensaje_whatsapp(telefono_usuario, respuesta_bot)
            
            return jsonify({"status": "ok"}), 200
            
    except Exception as e:
        print(f"Error procesando webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    # Retornar 200 para eventos que no son mensajes (ej. status update)
    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    print("🚀 Servidor Flask iniciado para WhatsApp...")
    app.run(port=5000, debug=True)
