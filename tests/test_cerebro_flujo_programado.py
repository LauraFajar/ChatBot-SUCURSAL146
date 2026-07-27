from src.cerebro import Brain


def test_respuesta_fija_para_consultas_fuera_del_flujo(monkeypatch):
    brain = Brain()

    # Evitar que se intente conectar a MySQL en la prueba
    monkeypatch.setattr(brain.inventario, 'registrar_interes', lambda *args, **kwargs: None)
    monkeypatch.setattr(brain.inventario, 'crear_orden', lambda *args, **kwargs: True)

    # Iniciar flujo para dejar el bot en un estado conocido
    respuesta_inicial = brain.procesar_mensaje('hola', '3000000000')
    assert 'Bienvenido' in respuesta_inicial['texto']

    # Enviar una consulta fuera del flujo esperado
    respuesta = brain.procesar_mensaje('¿Cuánto cuesta el IVA?', '3000000000')

    assert 'no puedo resolver tu duda' in respuesta['texto'].lower()
    assert 'asesor' in respuesta['texto'].lower()
    assert 'pronto se comunicará' in respuesta['texto'].lower()
