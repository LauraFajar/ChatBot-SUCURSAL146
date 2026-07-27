// =============================================================================
// WPP-BRIDGE ChatBot Almacén Oportunidades - server.js
// Puente entre WhatsApp Web (WPPConnect) y el cerebro del bot (Flask /procesar)
// =============================================================================
// Novedades:
// - Semaforo POR USUARIO (no global) para no bloquear clientes concurrentes
// - Si Flask está caído, responde POR WHATSAPP "servicio temporalmente no disponible"
//   en lugar de fallo SILENCIOSO
// - import de node-fetch cacheado al inicio con fallback a http
// - logs mas explicitos en cada paso para depurar
// =============================================================================

let fetchCached = null;
(async () => {
    try {
        const mod = await import('node-fetch');
        fetchCached = mod.default || mod.fetch || mod;
    } catch (e) {
        console.warn('⚠️ node-fetch no disponible, usando fallback http(s).', e.message);
        const http = require('http');
        fetchCached = (url, opts) => new Promise((resolve, reject) => {
            const u = new URL(url);
            const data = opts.body || '';
            const req = http.request({
                hostname: u.hostname,
                port: u.port,
                path: u.pathname,
                method: opts.method || 'GET',
                headers: { ...(opts.headers || {}), 'Content-Length': Buffer.byteLength(data) }
            }, (res) => {
                let body = '';
                res.on('data', c => body += c);
                res.on('end', () => resolve({
                    ok: res.statusCode >= 200 && res.statusCode < 300,
                    status: res.statusCode,
                    json: () => Promise.resolve(JSON.parse(body || '{}'))
                }));
            });
            req.on('error', reject);
            if (data) req.write(data);
            req.end();
        });
    }
})();

const wppconnect = require('@wppconnect-team/wppconnect');
const express = require('express');
const path = require('path');
const { extraerTextoMensaje, normalizarTelefono } = require('./message-utils');

const app = express();
app.use(express.json());

let clienteWpp = null;
const botStartTime = Math.floor(Date.now() / 1000);
const ultimosMensajes = new Map();
const usuariosProcesando = new Map();     // ← Semáforo POR USUARIO

const SESSION_NAME = process.env.WPP_SESSION || 'chatbot-suc146';
const FLASK_URL = process.env.FLASK_URL || 'http://127.0.0.1:5000/procesar';
const puppeteerOptions = {
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
};

if (process.env.CHROME_PATH) {
    puppeteerOptions.executablePath = process.env.CHROME_PATH;
}

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

async function intentarEnviarTexto(client, destinatarios, texto) {
    const lista = destinatarios && destinatarios.length ? destinatarios : [];
    for (const destino of lista) {
        try {
            console.log(`📤 Intentando enviar texto a ${destino}`);
            await client.sendText(destino, texto);
            console.log(`✅ Texto enviado a ${destino}`);
            return true;
        } catch (errEnvio) {
            console.warn(`⚠️ Falló el envío a ${destino}:`, errEnvio.message);
        }
    }
    return false;
}

function iniciarBot(client) {
    const manejarMensaje = async (mensaje) => {
        if (!mensaje) return;

        const telefonoUsuario = normalizarTelefono(
            mensaje.from || mensaje.chatId || mensaje.chat?.id || ''
        );

        if (!telefonoUsuario) {
            console.warn('⚠️ Mensaje sin teléfono identificable. Ignorado.');
            return;
        }

        if (usuariosProcesando.get(telefonoUsuario)) {
            console.log(`⏳ ${telefonoUsuario} ya tiene un mensaje en curso - se ignora este.`);
            return;
        }
        usuariosProcesando.set(telefonoUsuario, true);

        try {
            console.log('📨 Evento WPP recibido', {
                type: mensaje.type,
                from: mensaje.from,
                fromMe: mensaje.fromMe,
                hasBody: Boolean(mensaje.body),
                hasContent: Boolean(mensaje.content),
            });

            // Filtros
            if (mensaje.fromMe) return;
            if (mensaje.isGroupMsg) return;
            if (mensaje.from === 'status@broadcast') return;
            if (mensaje.from && (mensaje.from.includes('@g.us') || mensaje.from.includes('@lid'))) return;
            if (['notification_template', 'e2e_notification', 'gp2'].includes(mensaje.type)) return;
            if (mensaje.timestamp && mensaje.timestamp < botStartTime) return;

            const ahora = Date.now();
            const ultimoEnvio = ultimosMensajes.get(telefonoUsuario) || 0;
            if (ahora - ultimoEnvio < 1500) {
                console.log(`⚠️ ${telefonoUsuario} omitido (anti-frecuencia).`);
                return;
            }
            ultimosMensajes.set(telefonoUsuario, ahora);

            let textoUsuario = '';
            try {
                textoUsuario = extraerTextoMensaje(mensaje);
            } catch (e) {
                console.warn('⚠️ No se pudo extraer texto:', e.message);
            }

            const destinatarios = obtenerDestinatarios(mensaje);
            if (!textoUsuario || textoUsuario.trim() === '') {
                console.log('ℹ️ Mensaje sin texto útil - ignorado.');
                return;
            }

            console.log(`\n📩 [${telefonoUsuario}] "${textoUsuario}"`);

            // =========== LLAMAR A FLASK ===========
            let datos = null;
            let flaskFallo = false;
            try {
                if (!fetchCached) {
                    throw new Error('fetch aún no inicializado - espera 2s y reintenta');
                }
                const respuesta = await fetchCached(FLASK_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        telefono: telefonoUsuario,
                        mensaje: textoUsuario,
                    }),
                });
                if (!respuesta.ok) {
                    console.error(`❌ Flask status ${respuesta.status}`);
                    flaskFallo = true;
                } else {
                    datos = await respuesta.json();
                }
            } catch (errFetch) {
                console.error(`❌ No se pudo conectar a Flask: ${errFetch.message}`);
                flaskFallo = true;
            }

            if (flaskFallo) {
                const fallback = '⚠️ Hola! El bot se está preparando. Por favor intenta de nuevo en 1 minuto. Si el problema persiste, comunícate con soporte.';
                const enviado = await intentarEnviarTexto(client, destinatarios.concat([telefonoUsuario]), fallback);
                if (!enviado) console.error('🚨 Ni siquiera pudo enviar el mensaje de fallback. Revisa la conexión de WhatsApp Web.');
                return;
            }

            const textoRespuesta = (datos && datos.respuesta) || '';
            const imagenes = (datos && datos.imagenes) || [];

            if (!textoRespuesta) {
                console.warn('⚠️ Flask respondió 200 pero sin texto - no envía nada al usuario.');
                return;
            }

            console.log(`🤖 [${telefonoUsuario}] respuesta lista: "${textoRespuesta.slice(0, 80)}${textoRespuesta.length > 80 ? '...' : ''}"`);

            // 1) Enviar texto
            const enviado = await intentarEnviarTexto(client, destinatarios.concat([telefonoUsuario]), textoRespuesta);
            if (!enviado) {
                console.error(`🚨 No se pudo entregar la respuesta a ${telefonoUsuario} por ningún canal.`);
            }

            // 2) Imágenes si existen
            for (let i = 0; i < imagenes.length; i++) {
                const imgUrl = imagenes[i];
                try {
                    console.log(`📷 Enviando imagen ${i + 1}/${imagenes.length}: ${imgUrl}`);
                    await client.sendImage(telefonoUsuario, imgUrl, `imagen_${i + 1}.jpg`, `Imagen ${i + 1}`);
                } catch (errImg) {
                    console.error(`⚠️ No se pudo enviar imagen ${imgUrl}:`, errImg.message);
                }
            }

            console.log(`✅ Mensaje de ${telefonoUsuario} procesado.\n`);
        } catch (error) {
            console.error('❌ Error NO MANEJADO procesando mensaje:', error.stack || error.message);
        } finally {
            usuariosProcesando.delete(telefonoUsuario);
        }
    };

    if (typeof client.onAnyMessage === 'function') {
        client.onAnyMessage(manejarMensaje);
        console.log('🧩 onAnyMessage registrado');
    }
    if (typeof client.onMessage === 'function') {
        client.onMessage(manejarMensaje);
        console.log('🧩 onMessage registrado');
    }
}

// Iniciar WPPConnect
wppconnect.create({
    session: SESSION_NAME,
    catchQR: (base64Qr, asciiQR) => {
        console.log('\n' + '='.repeat(60));
        console.log('📱 ESCANEA ESTE QR CON TU WHATSAPP:');
        console.log('   Menú → Dispositivos vinculados → Vincular un dispositivo');
        console.log('='.repeat(60));
        console.log(asciiQR);
        console.log('='.repeat(60));
    },
    statusFind: (statusSession, session) => {
        console.log('📌 Estado sesión:', statusSession);
    },
    headless: puppeteerOptions.headless,
    devtools: false,
    useChrome: true,
    debug: false,
    logQR: true,
    browserWS: '',
    browserArgs: puppeteerOptions.args,
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
        console.error('❌ Error al iniciar WPPConnect:');
        console.error('   Si dice "Cannot find module": ejecuta >>> npm install <<< DENTRO de wpp-server/');
        console.error('   Si dice Chrome/Chromium missing: instala Google Chrome o define CHROME_PATH');
        console.error(error.stack || error.message || error);
        process.exit(1);
    });

// Endpoint para enviar mensajes manualmente desde fuera
app.post('/enviar', async (req, res) => {
    const { telefono, mensaje } = req.body || {};
    if (!clienteWpp) {
        return res.status(503).json({ error: 'WhatsApp no conectado aún - espera al QR' });
    }
    if (!telefono || !mensaje) {
        return res.status(400).json({ error: 'Faltan campos "telefono" y/o "mensaje"' });
    }
    try {
        await clienteWpp.sendText(normalizarTelefono(telefono), mensaje);
        res.json({ ok: true });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// Health check
app.get('/estado', (req, res) => {
    res.json({
        conectado: !!clienteWpp,
        procesando_usuarios: usuariosProcesando.size,
        flask_url: FLASK_URL,
        mensaje: clienteWpp ? '✅ WhatsApp activo' : '⏳ Esperando QR / conexión...',
    });
});

app.listen(3000, () => {
    console.log('='.repeat(60));
    console.log('🚀 Servidor WPP-Bridge corriendo en puerto 3000');
    console.log('   Estado: GET  http://127.0.0.1:3000/estado');
    console.log('   Enviar msj manual: POST http://127.0.0.1:3000/enviar');
    console.log(`   Endpoint Flask: ${FLASK_URL}`);
    console.log('⏳ Iniciando conexión con WhatsApp (esperando QR en consola)...');
    console.log('='.repeat(60));
});
