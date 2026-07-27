const test = require('node:test');
const assert = require('node:assert/strict');
const { extraerTextoMensaje } = require('../message-utils');

test('extrae texto de body', () => {
  assert.equal(extraerTextoMensaje({ body: 'hola' }), 'hola');
});

test('extrae texto de extendedTextMessage', () => {
  assert.equal(extraerTextoMensaje({ message: { extendedTextMessage: { text: 'hola desde texto' } } }), 'hola desde texto');
});

test('extrae texto de content', () => {
  assert.equal(extraerTextoMensaje({ content: 'mensaje' }), 'mensaje');
});

test('extrae caption de imagen', () => {
  assert.equal(extraerTextoMensaje({ message: { imageMessage: { caption: 'foto' } } }), 'foto');
});
