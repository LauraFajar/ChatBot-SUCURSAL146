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
const { extraerTextoMensaje, normalizarTelefono, destinosParaEnviar, destinosParaResponder } = require('./message-utils');

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
    // Primero intentamos 'from', ya que es el remitente REAL (y si tiene @lid, queremos
    // responderle por ese @lid, no adivinar). Para el resto de candidatos (@c.us, id de
    // chat, etc.) expandimos usando destinosParaResponder solo si el candidato viene formateado.
    const principal = mensaje?.from;
    const expandidos = [];
    if (principal) for (const d of destinosParaResponder(principal)) expandidos.push(d);
    const secundarios = [
        mensaje?.chatId,
        mensaje?.chat?.id,
        mensaje?.sender?.id,
        mensaje?.sender?.phone,
        mensaje?.remoteJid,
        mensaje?.id?.remote,
    ];
    for (const c of secundarios) {
        if (!c) continue;
        if (String(c).includes('@')) for (const d of destinosParaResponder(c)) expandidos.push(d);
        else for (const d of destinosParaEnviar(c)) expandidos.push(d);
    }
    return [...new Set(expandidos)];
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

            // =========== FILTROS (ahora CON LOGS para poder depurar por QUÉ se ignora) ===========

            // 1) Ignorar mensajes propios (yo envié desde el mismo celular del bot)
            if (mensaje.fromMe) {
                console.log(`⏭️  Ignorado (fromMe=true - yo mismo lo escribí): ${telefonoUsuario}`);
                return;
            }
            if (mensaje.sender?.isMe === true || mensaje.sender?.formattedName === 'Tú') {
                console.log(`⏭️  Ignorado: sender.isMe=true / "Tú" (yo soy el destinatario o remitente). from=${mensaje.from}`);
                return;
            }

            // 2) Ignorar GRUPOS (explicitamente @g.us)
            if (mensaje.isGroupMsg || (mensaje.from && mensaje.from.includes('@g.us'))) {
                console.log(`⏭️  Ignorado: es un grupo (from=${mensaje.from})`);
                return;
            }

            // 3) Ignorar Estados
            if (mensaje.from === 'status@broadcast') {
                console.log('⏭️  Ignorado: estado / status@broadcast');
                return;
            }

            // 4) Ignorar NOTIFICACIONES DEL SISTEMA
            if (['notification_template', 'e2e_notification', 'gp2'].includes(mensaje.type)) {
                console.log(`⏭️  Ignorado: notificación del sistema (type=${mensaje.type})`);
                return;
            }

            // 5) Newsletters / Canales / Comunidades
            //    - Formato newsletter@lid explicito
            //    - Formato 11 + 12 digitos + @lid (comunidades/canales sin telefono real).
            //      El @lid de usuarios NORMALES suele ser largo (no siempre), pero los IDs
            //      "newsletter" empiezan por 11 y no tienen "sender" real.
            if (
                mensaje.from && (
                    mensaje.from.includes('newsletter@lid') ||
                    (mensaje.from.startsWith('11') && mensaje.from.endsWith('@lid') && !mensaje.sender) ||
                    (mensaje.from.startsWith('11') && mensaje.from.endsWith('@lid') && mensaje.sender?.id && mensaje.sender.id.startsWith('11') && mensaje.sender?.isMe === true)
                )
            ) {
                console.log(`⏭️  Ignorado: newsletter / canal / comunidad (from=${mensaje.from})`);
                return;
            }

            // 6) Ignorar mensajes HISTÓRICOS (anteriores a cuando inició el bot)
            if (mensaje.timestamp && mensaje.timestamp < botStartTime) {
                console.log(`⏭️  Ignorado: histórico (ts=${mensaje.timestamp} < botStart=${botStartTime})`);
                return;
            }

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
        const destinos = destinosParaEnviar(String(telefono));
        const enviado = await intentarEnviarTexto(clienteWpp, destinos, mensaje);
        if (!enviado) return res.status(500).json({ error: 'No se pudo enviar por @c.us ni @lid', destinos_probadoss: destinos });
        res.json({ ok: true, destinos_probadoss: destinos });
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

// =============================================================================
// 🔧 ENDPOINT DE PRUEBA MANUAL - ENVÍA UN MENSAJE SIN QUE NADIE ESCRIBA
// Sirve para VERIFICAR que WPPConnect SÍ puede enviar mensajes por WhatsApp.
// Uso en Insomnia / navegador:
//   POST http://127.0.0.1:3000/debug/probar-envio
//   body JSON: {"telefono": "573001234567", "mensaje": "✅ Prueba de envío manual"}
// =============================================================================
app.post('/debug/probar-envio', async (req, res) => {
    const { telefono, mensaje } = req.body || {};
    if (!clienteWpp) {
        return res.status(503).json({
            ok: false,
            paso: 0,
            error: 'WhatsApp NO conectado. Aún no has escaneado el QR o la sesión expiró.'
        });
    }
    if (!telefono || !mensaje) {
        return res.status(400).json({
            ok: false,
            paso: 0,
            error: 'Faltan campos "telefono" (ej: 573001234567) y "mensaje" en el body JSON.'
        });
    }
    try {
        const destinos = destinosParaEnviar(String(telefono));
        console.log(`🔧 DEBUG: destinos a probar (${destinos.length}):`, destinos.join(', '));

        // ====== DETECCIÓN ANTI-AUTO-ENVÍO (antes de llamar sendText) ======
        // Obtenemos nuestro propio numero (WPP lo guarda internamente en varios lugares)
        const miId = String(
            clienteWpp?.config?.session ||
            clienteWpp?.wid?._serialized ||
            clienteWpp?.client?.info?.wid?._serialized ||
            clienteWpp?.pool?.wid ||
            ''
        );
        let miNumeroSinSufijo = '';
        if (miId && miId.includes('@')) miNumeroSinSufijo = miId.split('@')[0];

        // También si sendText devuelve sender.isMe=true y sendFailure=true, lo pillamos
        let enviadoOk = false;
        let ultimoResult = null;
        let ultimoErr = null;
        for (const dest of destinos) {
            const destSinSufijo = dest.includes('@') ? dest.split('@')[0] : dest;
            if (miNumeroSinSufijo && miNumeroSinSufijo === destSinSufijo) {
                ultimoErr = new Error(
                    `🛑 NO PUEDES ENVIAR AL NUMERO DEL PROPIO BOT (${destSinSufijo}). Usa un número DIFERENTE al que escaneaste el QR. Destino=${dest}. Mi ID=${miId}`
                );
                console.error('🔧 DEBUG:', ultimoErr.message);
                continue;
            }
            try {
                console.log(`🔧 DEBUG: intentando enviar a ${dest} el mensaje: "${mensaje.slice(0, 60)}"`);
                ultimoResult = await clienteWpp.sendText(dest, mensaje);
                console.log(
                    `🔧 DEBUG: sendText(${dest}) OK. sendFailure=${ultimoResult?.isSendFailure} ack=${ultimoResult?.ack} sender.isMe=${ultimoResult?.sender?.isMe} sender.formattedName=${ultimoResult?.sender?.formattedName}`
                );
                if (ultimoResult?.sender?.isMe === true && ultimoResult?.isSendFailure) {
                    const mensaje =
                        `🛑 El destinatario ${dest} resultó ser YO MISMO (sender.isMe=true, sendFailure=true). ` +
                        `No puedes usar debug/probar-envio contra el NÚMERO DEL PROPIO BOT. Usa un número familiar/amigo diferente.`;
                    console.error('🔧 DEBUG:', mensaje);
                    ultimoErr = new Error(mensaje);
                    continue;
                }
                if (!ultimoResult?.isSendFailure) {
                    enviadoOk = true;
                    break;
                } else {
                    console.warn(`🔧 DEBUG: ${dest} devolvió isSendFailure=true - probando siguiente formato...`);
                }
            } catch (e) {
                ultimoErr = e;
                console.warn(`🔧 DEBUG: ERROR sendText(${dest}):`, e.message);
            }
        }
        if (enviadoOk) {
            return res.json({ ok: true, destinos_probadoss: destinos, mi_id: miId || null, result: ultimoResult });
        }
        return res.status(500).json({
            ok: false,
            paso: 1,
            error: 'Todos los formatos fallaron. Ultimo error: ' + (ultimoErr?.message || 'sendFailure=true'),
            stack: (ultimoErr?.stack || '').toString().slice(0, 500),
            ultimo_result: ultimoResult,
            destinos_probadoss: destinos,
            mi_id: miId || null,
            mi_numero: miNumeroSinSufijo || null,
            sugerencia: [
                '1. Verifica que el teléfono destino TENGA WhatsApp y esté activo.',
                '2. Teléfono debe ser con código país sin ceros a la izquierda: ej 573209891720, NO 0320...',
                '3. Abre la ventana Chrome de WPPConnect y revisa que WhatsApp Web diga "Conectado".',
                '4. NUNCA envies al NÚMERO DEL PROPIO BOT (el que usaste para escanear el QR). Usa OTRO número.',
                '5. Si estás seguro que es otro número: envía desde Insomnia un GET http://127.0.0.1:3000/estado y pega el JSON.'
            ].join('\n')
        });
    } catch (e) {
        console.error('🔧 DEBUG: ERROR general en probar-envio:', e.stack || e.message);
        return res.status(500).json({
            ok: false,
            paso: 0,
            error: e.message,
            stack: (e.stack || '').toString().slice(0, 500),
        });
    }
});

// =============================================================================
// 🔧 ENDPOINT DE PRUEBA - SIMULA QUE LLEGA UN MENSAJE A WPPCONNECT
// Hace todo el flujo completo como si un usuario REAL hubiera escrito.
// POST http://127.0.0.1:3000/debug/simular-mensaje
//   body JSON: {"from": "573001234567@c.us", "body": "hola"}
// =============================================================================
app.post('/debug/simular-mensaje', async (req, res) => {
    const { from, body } = req.body || {};
    if (!clienteWpp) {
        return res.status(503).json({ ok: false, error: 'WhatsApp no conectado' });
    }
    if (!from || !body) {
        return res.status(400).json({ ok: false, error: 'Faltan "from" y "body" en JSON.' });
    }
    // Construimos un objeto de mensaje "falso" igual que el que envía WPPConnect
    const falsoMensaje = {
        id: { id: 'debug-' + Date.now(), remote: from, fromMe: false, self: 'in', _serialized: `false_${from}@c.us_debug` },
        from,
        to: 'me@c.us',
        author: undefined,
        fromMe: false,
        isGroupMsg: false,
        chatId: from,
        body,
        type: 'chat',
        timestamp: Math.floor(Date.now() / 1000),
        content: body,
        chat: { id: { user: from.split('@')[0], server: 'c.us', _serialized: from } },
        sender: { id: from.split('@')[0] + '@c.us', phone: from.split('@')[0] },
    };
    try {
        // Llamamos DIRECTAMENTE al manejador interno. No podemos acceder a manejarMensaje
        // porque está dentro de iniciarBot(). Pero podemos emitir el evento si existe.
        if (typeof clienteWpp.emit === 'function') {
            // Enviamos el evento por los 2 caminos que escucha iniciarBot()
            clienteWpp.emit('message', falsoMensaje);
            clienteWpp.emit('any_message', falsoMensaje);
            return res.json({ ok: true, mensaje_enviado_por_evento: true, telefono: from, texto: body });
        } else {
            return res.status(500).json({ ok: false, error: 'clienteWpp no tiene método emit()' });
        }
    } catch (e) {
        return res.status(500).json({ ok: false, error: e.message });
    }
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
