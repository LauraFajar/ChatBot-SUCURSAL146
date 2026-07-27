const assert = require('assert');
const { extraerTextoMensaje, normalizarTelefono } = require('../wpp-server/message-utils');

const mensaje = {
  body: 'hola'
};

assert.strictEqual(extraerTextoMensaje(mensaje), 'hola');
assert.strictEqual(normalizarTelefono('573001234567'), '573001234567@c.us');
assert.strictEqual(normalizarTelefono('573001234567@c.us'), '573001234567@c.us');
console.log('message-utils tests passed');
