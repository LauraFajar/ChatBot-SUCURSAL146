from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from src.cerebro import Brain

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# ── Configuración WhatsApp Business API (para producción futura) ───────────────
WHATSAPP_TOKEN  = os.getenv("WHATSAPP_TOKEN")
VERIFY_TOKEN    = os.getenv("VERIFY_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# ── Inicializar el cerebro una sola vez ───────────────────────────────────────
bot = Brain()
print("✅ Bot iniciado correctamente")

# =============================================================================
# ENDPOINT PARA WPPConnect (pruebas desde WhatsApp personal)
# =============================================================================

@app.route('/procesar', methods=['POST'])
def procesar_desde_wpp():
    """
    Recibe mensajes desde el servidor WPPConnect (wpp-server/server.js)
    y devuelve la respuesta del bot (texto + imágenes).
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Sin datos"}), 400

    telefono = data.get("telefono", "desconocido")
    mensaje  = data.get("mensaje", "")

    print(f"\n📩 [WPP] Mensaje de {telefono}: '{mensaje}'")

    res = bot.procesar_mensaje(mensaje, telefono)

    if isinstance(res, dict):
        texto = res.get("texto", "")
        imagenes = res.get("imagenes", [])
    else:
        texto = str(res)
        imagenes = []

    print(f"🤖 [WPP] Respuesta texto: '{texto}' | Imágenes: {len(imagenes)}\n")
    return jsonify({
        "respuesta": texto,
        "imagenes": imagenes
    })


# =============================================================================
# ENDPOINTS PARA WhatsApp Business API OFICIAL (producción)
# =============================================================================

def enviar_mensaje_whatsapp(telefono, texto):
    """Envía mensaje de texto usando la API oficial de Meta."""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("⚠️ Credenciales de WhatsApp API no configuradas en .env")
        return

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
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
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        print(f"✅ Mensaje de texto enviado a {telefono}")
    except Exception as e:
        print(f"❌ Error enviando texto a WhatsApp API: {e}")

def enviar_imagen_whatsapp(telefono, url_imagen):
    """Envía una imagen usando la API oficial de Meta."""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        return

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": telefono,
        "type": "image",
        "image": {"link": url_imagen}
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        print(f"📷 Imagen enviada a {telefono}")
    except Exception as e:
        print(f"❌ Error enviando imagen a WhatsApp API: {e}")


@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    """Verificación del webhook para la API oficial de Meta."""
    mode      = request.args.get('hub.mode')
    token     = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook verificado correctamente.")
        return challenge, 200
    return "Token incorrecto", 403


@app.route('/webhook', methods=['POST'])
def recibir_webhook():
    """Recibe mensajes e imágenes desde la API oficial de Meta."""
    body = request.get_json()

    try:
        if (
            body.get("object") == "whatsapp_business_account" and
            body.get("entry") and
            body["entry"][0].get("changes") and
            body["entry"][0]["changes"][0].get("value") and
            body["entry"][0]["changes"][0]["value"].get("messages")
        ):
            change   = body["entry"][0]["changes"][0]["value"]
            msg_info = change["messages"][0]
            telefono = msg_info["from"]

            msg_type = msg_info.get("type")
            if msg_type == "text":
                texto = msg_info["text"]["body"]
            elif msg_type == "image":
                texto = "[FOTO CÉDULA RECIBIDA]"
            else:
                texto = "[ADJUNTO RECIBIDO]"

            print(f"📩 [Meta] Mensaje de {telefono}: '{texto}'")

            res = bot.procesar_mensaje(texto, telefono)
            if isinstance(res, dict):
                texto_resp = res.get("texto", "")
                imgs = res.get("imagenes", [])
            else:
                texto_resp = str(res)
                imgs = []

            # Enviar texto
            if texto_resp:
                enviar_mensaje_whatsapp(telefono, texto_resp)
            # Enviar imágenes asociadas si existen
            for img in imgs:
                enviar_imagen_whatsapp(telefono, img)

            return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "ignored"}), 200


# =============================================================================
# PÁGINA DE ESTADO
# =============================================================================

@app.route('/', methods=['GET'])
def inicio():
    return """
    <html><body style="font-family:Arial; text-align:center; margin-top:50px;">
        <h1>🤖 ChatBot Almacén Oportunidades</h1>
        <p>✅ Servidor Flask activo</p>
        <ul style="list-style:none; padding:0;">
            <li>📌 <b>POST /procesar</b> → WPPConnect (pruebas WhatsApp personal)</li>
            <li>📌 <b>GET/POST /webhook</b> → WhatsApp Business API (producción)</li>
        </ul>
    </body></html>
    """, 200


if __name__ == '__main__':
    print("=" * 55)
    print("Servidor Flask - ChatBot Almacen Oportunidades (SUC146)")
    print("=" * 55)
    print("📌 Modo pruebas (WPPConnect): POST /procesar")
    print("📌 Modo producción (Meta API): POST /webhook")
    print("=" * 55)
    app.run(port=5000, debug=True)
