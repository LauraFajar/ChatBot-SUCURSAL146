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
 * Dado un sufijo (ej: 57300...), genera los 2 formatos de destino que WhatsApp puede
 * necesitar, para intentar enviar por el que funcione.
 * @param {string} telefono  Número puro o ya formateado
 * @returns {string[]}       Array con 1 o 2 destinos posibles, sin duplicados
 */
function destinosParaEnviar(telefono) {
  const base = normalizarTelefono(telefono);
  if (!base) return [];
  const sinSufijo = base.split('@')[0];
  if (!sinSufijo) return [base];
  // Devuelve ambos formatos (@c.us tradicional y @lid multi-device)
  const cUs = `${sinSufijo}@c.us`;
  const lid = `${sinSufijo}@lid`;
  if (base === cUs || base.endsWith('@c.us')) return [cUs, lid];
  if (base === lid || base.endsWith('@lid')) return [lid, cUs];
  return [cUs, lid];
}

module.exports = { extraerTextoMensaje, normalizarTelefono, destinosParaEnviar };
