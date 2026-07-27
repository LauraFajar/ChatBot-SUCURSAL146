function extraerTextoMensaje(mensaje) {
  if (!mensaje) return '';

  if (typeof mensaje.body === 'string' && mensaje.body.trim()) {
    return mensaje.body.trim();
  }

  if (mensaje.content && typeof mensaje.content === 'string' && mensaje.content.trim()) {
    return mensaje.content.trim();
  }

  if (mensaje.message) {
    if (mensaje.message.extendedTextMessage && mensaje.message.extendedTextMessage.text) {
      return mensaje.message.extendedTextMessage.text.trim();
    }

    if (mensaje.message.imageMessage && mensaje.message.imageMessage.caption) {
      return mensaje.message.imageMessage.caption.trim();
    }

    if (mensaje.message.conversation) {
      return mensaje.message.conversation.trim();
    }
  }

  return '';
}

function normalizarTelefono(telefono) {
  if (!telefono) return '';

  let valor = String(telefono).trim();
  if (!valor) return '';

  // Acepta IDs ya formateados (WhatsApp Web Multi-Device 2024+ usa @lid, anterior usaba @c.us)
  if (valor.includes('@')) return valor;

  // Si llega como número puro, usamos @c.us por compatibilidad
  // (server.js enviará a ambos formatos por si acaso)
  return `${valor}@c.us`;
}

/**
 * Dado un sufijo (ej: 57300...), genera los formatos DESTINO para ENVIAR un mensaje
 * de SALIDA (no para responder uno entrante).
 *
 * IMPORTANTE: NO usamos @lid en envíos salientes.
 * @lid lo asigna WhatsApp de forma INTERNA para cada chat; si lo adivinamos mal
 * terminamos enviándonos a nosotros mismos (isSendFailure=true) o a un canal/newsletter.
 * @lid SÓLO se usa al RESPONDER un mensaje entrante: ahí el 'from' ya nos da el @lid correcto.
 *
 * @param {string} telefono  Número puro o ya formateado
 * @returns {string[]}       Array con destinos válidos (solo @c.us o el que viniera formateado)
 */
function destinosParaEnviar(telefono) {
  const base = normalizarTelefono(telefono);
  if (!base) return [];
  const sinSufijo = base.split('@')[0];
  if (!sinSufijo) return [base];

  // Si el usuario ya pasó un ID formateado (ej: nos llegó un mensaje con @lid y
  // queremos responder a ese mismo formato exacto), lo respetamos.
  if (base.endsWith('@lid') || base.endsWith('@g.us')) return [base];

  // Caso por defecto: envío saliente a número -> solo @c.us.
  return [`${sinSufijo}@c.us`];
}

/**
 * Dado el remitente original de un mensaje entrante (from), genera los formatos
 * para RESPONDER a ESE remitente. AQUÍ SÍ usamos tanto @c.us como @lid si el
 * mensaje original venía con @lid, o viceversa — porque tenemos certeza del ID.
 */
function destinosParaResponder(originalFrom) {
  if (!originalFrom) return [];
  const base = normalizarTelefono(originalFrom);
  if (!base) return [];
  const sinSufijo = base.split('@')[0];
  if (!sinSufijo) return [base];
  if (base.endsWith('@c.us')) return [`${sinSufijo}@c.us`, `${sinSufijo}@lid`];
  if (base.endsWith('@lid')) return [`${sinSufijo}@lid`, `${sinSufijo}@c.us`];
  return [base];
}

module.exports = { extraerTextoMensaje, normalizarTelefono, destinosParaEnviar, destinosParaResponder };
