const wppconnect = require('@wppconnect-team/wppconnect');
const express = require('express');
const path = require('path');
const { extraerTextoMensaje, normalizarTelefono } = require('./message-utils');
const app = express();
app.use(express.json());

let clienteWpp = null;
const botStartTime = Math.floor(Date.now() / 1000);
const ultimosMensajes = new Map();
let procesandoMensaje = false;

const SESSION_NAME = process.env.WPP_SESSION || 'chatbot-suc146';
const puppeteerOptions = {
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
};

if (process.env.CHROME_PATH) {
    puppeteerOptions.executablePath = process.env.CHROME_PATH;
}

// ─── Iniciar WPPConnect ───────────────────────────────────────────────────────
wppconnect.create({
    session: SESSION_NAME,
    catchQR: (base64Qr, asciiQR) => {
        console.log('\n');
        console.log('='.repeat(60));
        console.log('📱 ESCANEA ESTE QR CON TU WHATSAPP:');
        console.log('   (WhatsApp > Menú > Dispositivos vinculados > Vincular dispositivo)');
        console.log('='.repeat(60));
        console.log(asciiQR);
        console.log('='.repeat(60));
    },
    statusFind: (statusSession, session) => {
        console.log('📌 Estado sesión:', statusSession);
    },
    headless: false,
    devtools: false,
    useChrome: true,
    debug: false,
    logQR: true,
    browserWS: '',
    browserArgs: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
    puppeteerOptions,
    disableWelcome: true,
    updatesLog: false,
    autoClose: 0,
    tokenStore: 'file',
    folderNameToken: path.join(__dirname, 'tokens'),
})
    .then((client) => {
        clienteWpp = client;
        console.log('\n✅ ¡WhatsApp conectado exitosamente!');
        console.log('🤖 El bot está listo para recibir mensajes...\n');
        iniciarBot(client);
    })
    .catch((error) => {
        console.error('❌ Error al iniciar WPPConnect:', error);
    });

// ─── Lógica principal: recibir mensajes y enviar a Flask ──────────────────────
function obtenerDestinatarios(mensaje) {
    const candidatos = [
        mensaje?.from,
        mensaje?.chatId,
        mensaje?.chat?.id,
        mensaje?.sender?.id,
        mensaje?.sender?.phone,
        mensaje?.remoteJid,
        mensaje?.id?.remote,
    ];

    const valores = candidatos.filter(Boolean).map((valor) => normalizarTelefono(valor));
    return [...new Set(valores)];
}

function iniciarBot(client) {
    const manejarMensaje = async (mensaje) => {
        if (!mensaje || procesandoMensaje) return;
        procesandoMensaje = true;

        try {
            console.log('📨 Evento WPP recibido', {
                type: mensaje.type,
                from: mensaje.from,
                fromMe: mensaje.fromMe,
                hasBody: Boolean(mensaje.body),
                hasContent: Boolean(mensaje.content),
                keys: Object.keys(mensaje || {})
            });
            // 🔒 FILTROS DE SEGURIDAD CRÍTICOS (ANTI-SPAM Y ANTI-BUCLE):

            // 1. Ignorar mensajes propios (enviados por el bot o desde tu mismo celular)
            if (mensaje.fromMe) return;

            // 2. Ignorar grupos, estados, identificadores @lid y notificaciones del sistema
            if (mensaje.isGroupMsg || mensaje.from === 'status@broadcast' || (mensaje.from && (mensaje.from.includes('@g.us') || mensaje.from.includes('@lid')))) return;
            if (mensaje.type === 'notification_template' || mensaje.type === 'e2e_notification' || mensaje.type === 'gp2') return;

            // 3. Ignorar mensajes antiguos cargados del historial al iniciar la sesión
            if (mensaje.timestamp && mensaje.timestamp < botStartTime) {
                return;
            }

            // 4. Control de frecuencia / Anti-bucle (mínimo 2 segundos entre mensajes del mismo usuario)
            const ahora = Date.now();
            const ultimoEnvio = ultimosMensajes.get(mensaje.from) || 0;
            if (ahora - ultimoEnvio < 2000) {
                console.log(`⚠️ Mensaje de ${mensaje.from} omitido por control de frecuencia.`);
                return;
            }
            ultimosMensajes.set(mensaje.from, ahora);

            let textoUsuario = '';
            try {
                textoUsuario = extraerTextoMensaje(mensaje);
            } catch (error) {
                console.warn('⚠️ No fue posible extraer texto del mensaje:', error.message);
                textoUsuario = '';
            }

            const telefonoUsuario = normalizarTelefono(mensaje.from || mensaje.chatId || mensaje.chat?.id);
            const destinatarios = obtenerDestinatarios(mensaje);

            if (!textoUsuario || textoUsuario.trim() === '') {
                console.log('ℹ️ Mensaje sin texto útil, se ignora.');
                return;
            }

            console.log(`\n📩 Mensaje recibido de ${telefonoUsuario}: "${textoUsuario}"`);

            // Enviar al cerebro del bot (Flask)
            const fetch = (await import('node-fetch')).default;
            const respuesta = await fetch('http://127.0.0.1:5000/procesar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    telefono: telefonoUsuario,
                    mensaje: textoUsuario
                })
            });

            if (!respuesta.ok) {
                console.error(`❌ Servidor Flask devolvió status ${respuesta.status}`);
                return;
            }

            const datos = await respuesta.json();
            const textoRespuesta = datos.respuesta || '';
            const imagenes = datos.imagenes || [];

            console.log(`🤖 Respuesta del bot preparada para ${telefonoUsuario}: "${textoRespuesta}"`);

            // 1. Enviar texto principal
            if (textoRespuesta) {
                let enviado = false;
                let ultimoError = null;

                for (const destino of destinatarios.length ? destinatarios : [telefonoUsuario]) {
                    try {
                        console.log(`📤 Intentando enviar texto a ${destino}`);
                        await client.sendText(destino, textoRespuesta);
                        console.log(`✅ Texto enviado a ${destino}`);
                        enviado = true;
                        break;
                    } catch (errEnvio) {
                        ultimoError = errEnvio;
                        console.warn(`⚠️ Falló el envío a ${destino}:`, errEnvio.message);
                    }
                }

                if (!enviado && ultimoError) {
                    throw ultimoError;
                }
            }

            // 2. Enviar imágenes asociadas si existen
            for (let i = 0; i < imagenes.length; i++) {
                const imgUrl = imagenes[i];
                try {
                    console.log(`📷 Enviando imagen ${i + 1}/${imagenes.length}: ${imgUrl}`);
                    await client.sendImage(telefonoUsuario, imgUrl, `imagen_${i+1}.jpg`, `Imagen ${i+1}`);
                } catch (errImg) {
                    console.error(`⚠️ No se pudo enviar imagen ${imgUrl}:`, errImg.message);
                }
            }

            console.log('✅ Proceso finalizado para este mensaje\n');
        } catch (error) {
            // NUNCA enviar mensaje por WhatsApp dentro del catch para evitar bucles si falla Flask o el envío
            console.error('❌ Error al procesar mensaje con Flask:', error.message);
        } finally {
            procesandoMensaje = false;
        }
    };

    if (typeof client.onAnyMessage === 'function') {
        client.onAnyMessage(manejarMensaje);
        console.log('🧩 Evento onAnyMessage registrado');
    }

    if (typeof client.onMessage === 'function') {
        client.onMessage(manejarMensaje);
        console.log('🧩 Evento onMessage registrado');
    }
}

// ─── Endpoint para enviar mensajes desde Flask (opcional) ────────────────────
app.post('/enviar', async (req, res) => {
    const { telefono, mensaje } = req.body;
    if (!clienteWpp) {
        return res.status(503).json({ error: 'WhatsApp no conectado aún' });
    }
    try {
        await clienteWpp.sendText(`${telefono}@c.us`, mensaje);
        res.json({ ok: true });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// ─── Endpoint de salud ────────────────────────────────────────────────────────
app.get('/estado', (req, res) => {
    res.json({ conectado: !!clienteWpp, mensaje: clienteWpp ? '✅ WhatsApp activo' : '⏳ Esperando conexión...' });
});

app.listen(3000, () => {
    console.log('='.repeat(60));
    console.log('🚀 Servidor WPP-Bridge corriendo en puerto 3000');
    console.log('⏳ Iniciando conexión con WhatsApp...');
    console.log('='.repeat(60));
});
