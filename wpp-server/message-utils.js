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

  const valor = String(telefono).trim();
  if (!valor) return '';
  if (valor.includes('@')) return valor;

  return `${valor}@c.us`;
}

module.exports = { extraerTextoMensaje, normalizarTelefono };
