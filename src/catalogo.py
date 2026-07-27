# =============================================================================
# CATÁLOGO DE PRODUCTOS Y OPCIONES PARA EL CHATBOT LAGOBO
# =============================================================================
# Estructura: CATALOGO → categoría → subcategoría → producto específico
# =============================================================================

OPCIONES_FINANCIACION = [
    "Addi",
    "Sistecrédito",
    "Sumaspay",
    "Banco de Bogotá"
]

# =============================================================================
# CATÁLOGO PRINCIPAL
# Cada categoría tiene:
#   - nombre: nombre legible
#   - emoji: icono de la categoría
#   - alias: palabras clave para detectar la categoría
#   - subcategorias: dict con opciones de sub-categoría o tamaño
#     Cada subcategoría tiene:
#       - nombre: nombre legible
#       - productos: dict con productos específicos (claves "1", "2", ...)
#         Cada producto tiene:
#           - nombre, precio, precio_num, imagenes, descripcion_corta, descripcion_amplia
# =============================================================================

CATALOGO = {

    # ─────────────────────────────────────────────────────────────────────────
    # 1. TELEVISORES
    # ─────────────────────────────────────────────────────────────────────────
    "televisor": {
        "nombre": "Televisores",
        "emoji": "📺",
        "alias": ["televisor", "televisores", "tv", "tele", "television", "televisión", "1"],
        "subcategorias": {
            "1": {
                "nombre": "📺 Pequeños (hasta 43\")",
                "productos": {
                    "1": {
                        "nombre": "Televisor LG Full HD (32\")",
                        "precio": "$899.000 COP",
                        "precio_num": 899000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "📺 *Televisor LG Full HD*\n"
                            "• Pantalla LED Full HD con Active HDR\n"
                            "• Procesador Quad Core\n"
                            "• Virtual Surround Plus\n"
                            "• IA LG ThinQ AI integrada"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Televisor LG Full HD*\n"
                            "• Pantalla: LED Full HD con Active HDR para colores más reales\n"
                            "• Procesador: Quad Core para rendimiento fluido\n"
                            "• Sonido: Virtual Surround Plus envolvente\n"
                            "• Inteligencia Artificial: LG ThinQ AI con control por voz\n"
                            "• Conectividad: WiFi, Bluetooth, múltiples HDMI y USB\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "TV Challenger LED 40\" KG90 BT Google",
                        "precio": "$1.150.000 COP",
                        "precio_num": 1150000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "📺 *TV Challenger LED 40\" KG90 BT*\n"
                            "• Resolución Full HD\n"
                            "• Google TV con control por voz\n"
                            "• WiFi, Bluetooth y Chromecast integrado"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger LED 40\"*\n"
                            "• Pantalla: 40\" LED Full HD (1920x1080)\n"
                            "• Sistema: Google TV con asistente de voz integrado\n"
                            "• Conectividad: WiFi, Bluetooth y Chromecast built-in\n"
                            "• Acceso a apps de streaming (Netflix, YouTube, etc.)\n"
                            "• Control remoto con botón de voz dedicado\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "2": {
                "nombre": "📺 Medianos (50\" – 58\")",
                "productos": {
                    "1": {
                        "nombre": "TV LG 50\" 4K (50NU855BPSA)",
                        "precio": "$2.199.000 COP",
                        "precio_num": 2199000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "📺 *TV LG 50\" 4K*\n"
                            "• Pantalla 4K con Nano Detail Enhancer\n"
                            "• webOS con Google Gemini y Microsoft Copilot\n"
                            "• AI Hub protegido por LG Shield\n"
                            "• Diseño Linear Flow y LG Channels"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG 50\" 4K*\n"
                            "• Pantalla: 50\" 4K UHD con tecnología Nano Detail Enhancer\n"
                            "• Sistema: webOS con IA de Google Gemini y Microsoft Copilot\n"
                            "• Seguridad: AI Hub protegido por LG Shield\n"
                            "• Diseño: Linear Flow elegante y moderno\n"
                            "• Contenido: Acceso a LG Channels gratuitos\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "TV LG 55\" 4K (55NU855BPSA)",
                        "precio": "$2.599.000 COP",
                        "precio_num": 2599000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "📺 *TV LG 55\" 4K*\n"
                            "• Pantalla 4K con Nano Detail Enhancer\n"
                            "• webOS + Google Gemini + Microsoft Copilot\n"
                            "• AI Hub con LG Shield\n"
                            "• Diseño Linear Flow y LG Channels"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG 55\" 4K*\n"
                            "• Pantalla: 55\" 4K UHD con tecnología Nano Detail Enhancer\n"
                            "• Sistema: webOS impulsado por Google Gemini y Microsoft Copilot\n"
                            "• Seguridad: AI Hub con LG Shield\n"
                            "• Diseño: Linear Flow refinado\n"
                            "• Contenido: Acceso a LG Channels\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "3": {
                        "nombre": "TV Challenger 58\" QLED (58KG290 BT2)",
                        "precio": "$2.899.000 COP",
                        "precio_num": 2899000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "📺 *TV Challenger 58\" QLED 4K*\n"
                            "• QLED 4K UHD (3840x2160)\n"
                            "• Google TV con control por voz\n"
                            "• Bluetooth 5.1, Chromecast, WiFi dual\n"
                            "• 3 puertos HDMI y sonido Dolby"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger 58\" QLED*\n"
                            "• Pantalla: 58\" QLED 4K UHD (3840x2160) con colores brillantes\n"
                            "• Sistema: Google TV con asistente de voz\n"
                            "• Conectividad: Bluetooth 5.1, Chromecast integrado, WiFi dual band\n"
                            "• Puertos: 3 HDMI para conectar consolas, decodificadores y más\n"
                            "• Audio: Sonido Dolby envolvente\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "3": {
                "nombre": "📺 Grandes (60\" o más)",
                "productos": {
                    "1": {
                        "nombre": "TV Hyundai 60\" QLED 4K (HYLED6005QG)",
                        "precio": "$3.299.000 COP",
                        "precio_num": 3299000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "📺 *TV Hyundai 60\" QLED 4K*\n"
                            "• 60\" QLED 4K UHD con tecnología Quantum Dot\n"
                            "• Smart TV con Google TV\n"
                            "• 3 HDMI, 2 USB, WiFi y salida óptica\n"
                            "• Bisel delgado y base metálica"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Hyundai 60\" QLED*\n"
                            "• Pantalla: 60\" QLED 4K UHD (3840x2160) con Quantum Dot\n"
                            "• Sistema: Smart TV con Google TV integrado\n"
                            "• Puertos: 3 HDMI, 2 USB, salida óptica\n"
                            "• Conectividad: WiFi integrado\n"
                            "• Diseño: Bisel ultra delgado y base metálica premium\n"
                            "• Audio: Sonido envolvente potente\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "TV LG 65\" 4K (65UA8050PSA)",
                        "precio": "$3.799.000 COP",
                        "precio_num": 3799000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "📺 *TV LG 65\" 4K*\n"
                            "• 4K HDR10 Pro con Procesador Alpha 7 4K AI Gen8\n"
                            "• Superescalado 4K\n"
                            "• AI Magic Remote con botón de IA\n"
                            "• Control de voz y función arrastrar/soltar"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG 65\" 4K*\n"
                            "• Pantalla: 65\" 4K HDR10 Pro con colores ultra reales\n"
                            "• Procesador: Alpha 7 4K AI Gen8 con superescalado\n"
                            "• Control: AI Magic Remote con nuevo botón de IA dedicado\n"
                            "• Funciones: Control de voz avanzado y función arrastrar/soltar\n"
                            "• Conectividad: WiFi, Bluetooth, HDMI 2.1 y USB\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "3": {
                        "nombre": "TV LG 75\" Ultra Big 4K (75NU855BPSA)",
                        "precio": "$5.499.000 COP",
                        "precio_num": 5499000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1593359677879-a4bb92f829e1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "📺 *TV LG 75\" Ultra Big 4K*\n"
                            "• 75\" 4K con Nano Detail Enhancer\n"
                            "• webOS con IA (Google Gemini y Microsoft Copilot)\n"
                            "• AI Hub con LG Shield\n"
                            "• Diseño Linear Flow refinado"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG 75\" Ultra Big*\n"
                            "• Pantalla: Ultra Big TV 75\" 4K con Nano Detail Enhancer\n"
                            "• Sistema: webOS con IA (Google Gemini y Microsoft Copilot)\n"
                            "• Seguridad: AI Hub con LG Shield integrado\n"
                            "• Diseño: Finish Linear Flow refinado ultra moderno\n"
                            "• Contenido: LG Channels con miles de canales gratuitos\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # 2. NEVERAS
    # ─────────────────────────────────────────────────────────────────────────
    "nevera": {
        "nombre": "Neveras y Refrigeradores",
        "emoji": "❄️",
        "alias": ["nevera", "neveras", "refrigerador", "refrigeradores", "frigorifico", "nevecón", "congelador", "congeladores", "2"],
        "subcategorias": {
            "1": {
                "nombre": "❄️ Pequeñas (hasta 250L)",
                "productos": {
                    "1": {
                        "nombre": "Nevera Mabe RMU 235 NACU",
                        "precio": "$1.299.000 COP",
                        "precio_num": 1299000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevera Mabe RMU 235 NACU*\n"
                            "• Ahorro energético hasta el 67%\n"
                            "• Tecnología Home Energy Saver y compresor Eco Advance\n"
                            "• Refrigerante ecológico R600\n"
                            "• Dispensador de agua removible 2L"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Mabe RMU 235*\n"
                            "• Capacidad: 235 Litros\n"
                            "• Ahorro: Hasta 67% con compresor Eco Advance\n"
                            "• Tecnología: Home Energy Saver y refrigerante R600 ecológico\n"
                            "• Características: Sistema de escarcha inteligente\n"
                            "• Dispensador de agua removible de 2 Litros\n"
                            "• Cajón con topes de seguridad para mayor organización\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Nevera Haceb No Frost 243L Inverter Titanio",
                        "precio": "$1.450.000 COP",
                        "precio_num": 1450000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevera Haceb No Frost 243L Inverter*\n"
                            "• 243 Litros - Eficiencia energética Tipo A\n"
                            "• Motor Inverter silencioso\n"
                            "• Color titanio con manija integrada\n"
                            "• Ideal para espacios compactos"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Haceb No Frost 243L*\n"
                            "• Capacidad: 243 Litros No Frost (sin escarcha)\n"
                            "• Eficiencia: Clase energética Tipo A\n"
                            "• Motor: Inverter silencioso de bajo consumo\n"
                            "• Diseño: Acabado color titanio con manija integrada\n"
                            "• Perfecta para espacios compactos o cocinas pequeñas\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "2": {
                "nombre": "❄️ Medianas (250L – 350L)",
                "productos": {
                    "1": {
                        "nombre": "Nevera Mabe RMA247PJCG SMJ",
                        "precio": "$1.599.000 COP",
                        "precio_num": 1599000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevera Mabe RMA247PJCG*\n"
                            "• Ahorro hasta 56% con compresor Eco Advance\n"
                            "• Total Fresh Flow para distribución óptima del aire\n"
                            "• Espacios organizadores inteligentes"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Mabe RMA247*\n"
                            "• Capacidad: 247 Litros\n"
                            "• Ahorro: Hasta 56% con compresor Eco Advance\n"
                            "• Sistema de frío: Total Fresh Flow para mejor distribución\n"
                            "• Organización: Espacios organizadores inteligentes\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Nevera Challenger CR290L NF Titanium (Lúmina)",
                        "precio": "$1.799.000 COP",
                        "precio_num": 1799000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevera Challenger CR290L Lúmina*\n"
                            "• 290 Litros No Frost (clase tropical)\n"
                            "• Sistema multiflujo de refrigeración\n"
                            "• Refrigerante R600a ecológico\n"
                            "• Compartimento Smart Pocket"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger CR290L*\n"
                            "• Capacidad: 290 Litros brutos No Frost, clase tropical\n"
                            "• Sistema: Multiflujo de refrigeración para temperatura uniforme\n"
                            "• Refrigerante: R600a ecológico de bajo impacto ambiental\n"
                            "• Ruido: Bajo nivel de operación (funcionamiento silencioso)\n"
                            "• Extra: Compartimento Smart Pocket para acceso rápido\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "3": {
                        "nombre": "Nevera Smart Inverter 264L (MDRT385MTM28)",
                        "precio": "$1.999.000 COP",
                        "precio_num": 1999000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevera Smart Inverter 264L*\n"
                            "• 264 Litros con Tecnología Inverter Quattro\n"
                            "• Parrillas de cristal templado Xtreme Trust\n"
                            "• Filtros Active C-Fresh (evitan mezcla de olores)"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Smart Inverter 264L*\n"
                            "• Capacidad: 264 Litros con congelador superior\n"
                            "• Motor: Tecnología Inverter Quattro (ahorradora, rápida y silenciosa)\n"
                            "• Organización: Parrillas de cristal templado Xtreme Trust\n"
                            "• Higiene: Filtros de carbono Active C-Fresh anti-olores\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "4": {
                        "nombre": "Nevera Mabe RMA 313FXCT",
                        "precio": "$2.199.000 COP",
                        "precio_num": 2199000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevera Mabe RMA 313FXCT*\n"
                            "• Ahorro hasta 67% con compresor Eco Advance\n"
                            "• Sistema Total Fresh Flow\n"
                            "• Espacios inteligentes de distribución interna"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Mabe RMA 313*\n"
                            "• Capacidad: 313 Litros\n"
                            "• Ahorro: Hasta 67% con compresor Eco Advance\n"
                            "• Sistema de frío: Total Fresh Flow para distribución perfecta\n"
                            "• Interior: Espacios inteligentes bien distribuidos\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "3": {
                "nombre": "❄️ Grandes (más de 350L)",
                "productos": {
                    "1": {
                        "nombre": "Nevera Haceb ALC 404 SE DA MI Plomo",
                        "precio": "$2.599.000 COP",
                        "precio_num": 2599000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevera Haceb ALC 404 Plomo*\n"
                            "• Acabado gris plomo con manija integrada\n"
                            "• No Frost con sistema Haceb Himalaya\n"
                            "• Enfriamiento sectorizado que duplica la conservación"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Haceb ALC 404*\n"
                            "• Capacidad: 404 Litros No Frost\n"
                            "• Diseño: Acabado gris plomo con manija integrada moderna\n"
                            "• Tecnología: Sistema Haceb Himalaya con enfriamiento sectorizado\n"
                            "• Conservación: Duplica el tiempo de conservación de los alimentos\n"
                            "• Temperatura: Estable en todas las zonas de la nevera\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Nevera Mabe RMP 415 GCG",
                        "precio": "$2.899.000 COP",
                        "precio_num": 2899000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevera Mabe RMP 415 GCG*\n"
                            "• Tecnología Home Energy Saver con MultiAhorro\n"
                            "• Sistema Total Fresh Flow\n"
                            "• Distribución práctica para alimentos y bebidas"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Mabe RMP 415*\n"
                            "• Capacidad: 415 Litros\n"
                            "• Ahorro: Tecnología Home Energy Saver con sistema MultiAhorro\n"
                            "• Frescura: Total Fresh Flow para mantener alimentos frescos más tiempo\n"
                            "• Organización: Distribución práctica con compartimentos especializados\n"
                            "• Ideal: Familias grandes o negocios pequeños\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "4": {
                "nombre": "❄️ Nevecones y Refrigeradores Avanzados",
                "productos": {
                    "1": {
                        "nombre": "Nevecón Midea MDR700FGM45CO2",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevecón Midea MDR700FGM45CO2*\n"
                            "• Tecnología Plus Inverter con ahorro de energía\n"
                            "• Multi Air Flow para enfriamiento uniforme\n"
                            "• Parrillas ajustables de cristal templado Xtreme Trust"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Nevecón Midea MDR700FGM45CO2*\n"
                            "• Tecnología: Plus Inverter (enfriamiento rápido, bajo consumo y funcionamiento silencioso)\n"
                            "• Distribución de frío: Multi Air Flow en múltiples niveles\n"
                            "• Diseño interior: Parrillas ajustables de cristal templado Xtreme Trust con protección antiderrame"
                        )
                    },
                    "2": {
                        "nombre": "Nevecón LG 519 Litros (6551BPD.AHSCCLM)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Nevecón LG 519 Litros*\n"
                            "• Capacidad: 519 Litros\n"
                            "• Total No Frost y motor Inverter Compressor\n"
                            "• Pantalla LED táctil e iluminación LED"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Nevecón LG 519 Litros*\n"
                            "• Capacidad: 519 Litros\n"
                            "• Tecnología: Total No Frost sin escarcha y motor Inverter Compressor con 3 años de garantía\n"
                            "• Características: Flujo de aire múltiple, pantalla LED táctil, iluminación LED y estantes de vidrio templado de alta resistencia"
                        )
                    },
                    "3": {
                        "nombre": "Refrigerador Electrolux 421 Litros (ERQU4DE3HWS 421)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "❄️ *Refrigerador Electrolux 421 Litros*\n"
                            "• Capacidad: 421 Litros No Frost Efficient\n"
                            "• Tecnología AutoSense para mayor frescura\n"
                            "• Cajón SuperFresh con temperatura ajustable"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Refrigerador Electrolux 421 Litros*\n"
                            "• Capacidad: 421 Litros No Frost Efficient\n"
                            "• Inteligencia Artificial: AutoSense controla automáticamente la temperatura y prolonga la frescura hasta un 30% más\n"
                            "• Eficiencia: Inverter con ahorro energético y estabilidad térmica\n"
                            "• Flexibilidad: Cajón SuperFresh con temperatura ajustable y función Meat para carnes y pescados"
                        )
                    }
                }
            },
            "5": {
                "nombre": "❄️ Congeladores Horizontales",
                "productos": {
                    "1": {
                        "nombre": "Congelador Horizontal Challenger CH-100 (97L)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧊 *Congelador Horizontal Challenger CH-100*\n"
                            "• Capacidad: 97 Litros brutos\n"
                            "• Diseño compacto y eficiente\n"
                            "• Ideal para espacios reducidos"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger CH-100*\n"
                            "• Capacidad: 97 Litros brutos\n"
                            "• Diseño: Formato compacto horizontal ideal para espacios reducidos\n"
                            "• Enfoque: Eficiencia energética y durabilidad"
                        )
                    },
                    "2": {
                        "nombre": "Congelador Horizontal Mabe / Challenger Alaska 145 (142L)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧊 *Congelador Horizontal Alaska 145*\n"
                            "• Capacidad: 142 Litros\n"
                            "• Reserva térmica de hasta 150 horas\n"
                            "• Triple función: enfría, congela y mantiene"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Alaska 145*\n"
                            "• Capacidad: 142 Litros aprobado para uso comercial\n"
                            "• Reserva térmica: conserva el frío hasta por 150 horas sin energía eléctrica\n"
                            "• Funcionalidad: triple función y gas ecológico R600a"
                        )
                    },
                    "3": {
                        "nombre": "Congelador Horizontal Mabe Alaska 195 (198L)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧊 *Congelador Horizontal Alaska 195*\n"
                            "• Capacidad: 198 Litros\n"
                            "• Tecnología Cold Extra 150\n"
                            "• Triple función de enfriado y congelación"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Alaska 195*\n"
                            "• Capacidad: aproximadamente 198 Litros\n"
                            "• Reserva térmica: mantiene el frío hasta 150 horas durante cortes de luz\n"
                            "• Funcionalidad: triple función y refrigerante ecológico R600a"
                        )
                    },
                    "4": {
                        "nombre": "Congelador Horizontal Mabe Alaska 300 (320L)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧊 *Congelador Horizontal Alaska 300*\n"
                            "• Capacidad: 320 Litros\n"
                            "• Reserva térmica de 150 horas\n"
                            "• Triple función (enfría, congela y mantiene)"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Alaska 300*\n"
                            "• Capacidad: 320 Litros aprobado para uso comercial\n"
                            "• Reserva térmica: conserva el frío hasta por 150 horas sin electricidad\n"
                            "• Funcionalidad: triple función y gas refrigerante R600a"
                        )
                    },
                    "5": {
                        "nombre": "Congelador Horizontal Challenger CH-363 (387L)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧊 *Congelador Horizontal Challenger CH-363*\n"
                            "• Capacidad: 387 Litros\n"
                            "• Funciona como congelador o refrigerador\n"
                            "• Diseño resistente y fácil de limpiar"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger CH-363*\n"
                            "• Capacidad: 387 Litros\n"
                            "• Sistema dual: funciona como congelador o refrigerador según la necesidad\n"
                            "• Diseño: materiales de alta durabilidad, fácil limpieza y canastillas resistentes"
                        )
                    },
                    "6": {
                        "nombre": "Congelador Horizontal Challenger Doble Puerta (CH-396 / 535L)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧊 *Congelador Horizontal Doble Puerta*\n"
                            "• Capacidad: 535 Litros brutos\n"
                            "• Sistema dual y doble puerta\n"
                            "• Cerradura de seguridad y ruedas"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger Doble Puerta*\n"
                            "• Capacidad: 535 Litros brutos\n"
                            "• Sistema dual: opción para usar como refrigerador o congelador\n"
                            "• Diseño: doble puerta con cerradura de seguridad y ruedas para traslado"
                        )
                    },
                    "7": {
                        "nombre": "Congelador Horizontal Electrolux (EFH70S3CSAV)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧊 *Congelador Horizontal Electrolux*\n"
                            "• Versatilidad 3 en 1\n"
                            "• 7 niveles de temperatura ajustables\n"
                            "• Panel de control externo y función Turbo Congelador"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Electrolux EFH70S3CSAV*\n"
                            "• Versatilidad 3 en 1: enfría, conserva o congela\n"
                            "• Control: panel de un solo toque con bloqueo de seguridad\n"
                            "• Accesorios: canasta plástica organizadora, iluminación LED y ruedas para transporte"
                        )
                    },
                    "8": {
                        "nombre": "Congelador Horizontal Inducol Industrial (CH-DPB350BL1)",
                        "precio": "Consultar precio",
                        "precio_num": 0,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧊 *Congelador Horizontal Inducol Industrial*\n"
                            "• Capacidad: 300 a 350 Litros\n"
                            "• Rango de temperatura desde 0°C a 4°C hasta -22°C\n"
                            "• Construcción industrial con llave de seguridad"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Inducol Industrial CH-DPB350BL1*\n"
                            "• Capacidad: 300 a 350 Litros\n"
                            "• Rango de temperatura: refrigeración de 0°C a 4°C y congelación hasta -22°C\n"
                            "• Construcción: puerta abatible sólida, llave de seguridad, aislamiento industrial y evaporación estática"
                        )
                    }
                }
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # 3. LAVADORAS
    # ─────────────────────────────────────────────────────────────────────────
    "lavadora": {
        "nombre": "Lavadoras",
        "emoji": "🧺",
        "alias": ["lavadora", "lavadoras", "lavarropas", "3"],
        "subcategorias": {
            "1": {
                "nombre": "🧺 Pequeñas (hasta 13 kg)",
                "productos": {
                    "1": {
                        "nombre": "Lavadora Automática 11 Kg",
                        "precio": "$1.199.000 COP",
                        "precio_num": 1199000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧺 *Lavadora Automática 11 Kg*\n"
                            "• Capacidad: 11 Kg (24 lb)\n"
                            "• Puerta de vidrio templado y sistema One Touch\n"
                            "• 8 programas de lavado\n"
                            "• Función CARE+ y apagado automático"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Lavadora 11 Kg*\n"
                            "• Capacidad: 11 Kg (24 lb)\n"
                            "• Puerta: Vidrio templado resistente\n"
                            "• Sistema: One Touch para lavados rápidos\n"
                            "• Programas: 8 programas de lavado personalizados\n"
                            "• Tambor: Acero inoxidable con asistente anti-enredos\n"
                            "• Extras: Función CARE+ y apagado automático\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Lavadora LG WT13NVTB TurboDrum",
                        "precio": "$1.399.000 COP",
                        "precio_num": 1399000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧺 *Lavadora LG WT13NVTB*\n"
                            "• Tecnología TurboDrum (tina y pulsador en direcciones opuestas)\n"
                            "• Sistema Side Water Fall sin residuos de detergente\n"
                            "• Filtro de pelusa y diseño sofisticado"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG WT13NVTB*\n"
                            "• Capacidad: 13 Kg\n"
                            "• Tecnología: TurboDrum (tina y pulsador en direcciones opuestas)\n"
                            "• Sistema: Side Water Fall disuelve detergente sin dejar residuos\n"
                            "• Filtro: Atrapa pelusas eficientemente\n"
                            "• Diseño: Sofisticado y moderno\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "2": {
                "nombre": "🧺 Medianas (14 kg – 19 kg)",
                "productos": {
                    "1": {
                        "nombre": "Lavadora Haceb IVY 14KG D NE",
                        "precio": "$1.699.000 COP",
                        "precio_num": 1699000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧺 *Lavadora Haceb IVY 14KG*\n"
                            "• Panel intuitivo con orientación sensitiva\n"
                            "• Relieves, braille y señales auditivas (inclusiva)\n"
                            "• Ciclo ECO: reutiliza hasta 80L de agua del enjuague"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Haceb IVY 14KG*\n"
                            "• Capacidad: 14 Kg\n"
                            "• Inclusión: Panel con orientación sensitiva (relieves, braille y señales auditivas)\n"
                            "• Ahorro: Ciclo ECO que reutiliza hasta 80 litros del segundo enjuague\n"
                            "• Eficiente en agua y energía\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Lavadora Electrolux EWIX16F3ESG 16Kg Premium",
                        "precio": "$1.999.000 COP",
                        "precio_num": 1999000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧺 *Lavadora Electrolux 16Kg Premium Care*\n"
                            "• Filtro de nano cobre (inhibe el 99% de bacterias)\n"
                            "• Sistema Power Dilution para manchas difíciles\n"
                            "• Reducido consumo de agua y energía"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Electrolux 16Kg*\n"
                            "• Capacidad: 16 Kg (Top Load Premium Care)\n"
                            "• Higiene: Filtro de nano cobre inhibe pelusas y hasta el 99% de bacterias\n"
                            "• Tecnología: Power Dilution disuelve detergente/suavizante y elimina manchas\n"
                            "• Ahorro: Consumo reducido de agua y energía\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "3": {
                        "nombre": "Lavadora LG WT18MVTB Smart Inverter 18Kg",
                        "precio": "$2.299.000 COP",
                        "precio_num": 2299000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧺 *Lavadora LG 18Kg Smart Inverter*\n"
                            "• Motor Smart Inverter de alto rendimiento\n"
                            "• Smart Motion: 3 movimientos para optimizar el lavado\n"
                            "• TurboDrum para limpieza profunda"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG WT18MVTB*\n"
                            "• Capacidad: 18 Kg\n"
                            "• Motor: Smart Inverter de larga duración\n"
                            "• Tecnología: Smart Motion con 3 movimientos inteligentes\n"
                            "• TurboDrum: Tina y pulsador en direcciones opuestas para mayor limpieza\n"
                            "• Garantía: 10 años en motor Smart Inverter"
                        )
                    },
                    "4": {
                        "nombre": "Lavadora LG WT19MVTB Smart Inverter 19Kg",
                        "precio": "$2.499.000 COP",
                        "precio_num": 2499000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧺 *Lavadora LG 19Kg Smart Inverter*\n"
                            "• Motor Smart Inverter + Smart Motion + TurboDrum\n"
                            "• Filtro de pelusa ancho para mayor eficiencia\n"
                            "• Capacidad ideal para familias grandes"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG WT19MVTB*\n"
                            "• Capacidad: 19 Kg\n"
                            "• Motor: Smart Inverter de alto rendimiento y durabilidad\n"
                            "• Tecnología: Smart Motion y TurboDrum integrados\n"
                            "• Filtro de pelusa ancho para mayor captura de residuos\n"
                            "• Garantía: 10 años en motor Smart Inverter"
                        )
                    }
                }
            },
            "3": {
                "nombre": "🧺 Grandes (20 kg o más)",
                "productos": {
                    "1": {
                        "nombre": "Lavadora LG WT20NBXGT AI DD™",
                        "precio": "$2.899.000 COP",
                        "precio_num": 2899000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧺 *Lavadora LG AI DD™*\n"
                            "• IA DD™ ajusta el lavado según el tipo de tela\n"
                            "• Conectividad ThinQ™ desde tu smartphone\n"
                            "• EasyUnload™ y Motor Inverter Direct Drive™"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG WT20NBXGT*\n"
                            "• Tecnología: AI DD™ detecta el tipo de tela y ajusta el lavado\n"
                            "• Conectividad: ThinQ™ para controlar desde tu celular\n"
                            "• EasyUnload™: facilita la descarga de la ropa\n"
                            "• Motor: Inverter Direct Drive™ directo al tambor\n"
                            "• Filtro de pelusas ancho de alta eficiencia\n"
                            "• Garantía: 10 años en motor Inverter Direct Drive"
                        )
                    },
                    "2": {
                        "nombre": "Lavadora LG WT23EGTX6 TurboWash™ 23Kg",
                        "precio": "$3.499.000 COP",
                        "precio_num": 3499000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🧺 *Lavadora LG TurboWash™ 23Kg*\n"
                            "• Lavado completo en solo 39 minutos (TurboWash™)\n"
                            "• AI DD™ y conectividad ThinQ™\n"
                            "• Motor Inverter Direct Drive™ y EasyUnload™"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG WT23EGTX6*\n"
                            "• Capacidad: 23 Kg (ideal para edredones y ropa voluminosa)\n"
                            "• TurboWash™: Ciclo de lavado completo en solo 39 minutos\n"
                            "• AI DD™: Ajuste inteligente según tipo de tela\n"
                            "• Conectividad: ThinQ™ control desde smartphone\n"
                            "• EasyUnload™ para descarga fácil de la ropa\n"
                            "• Motor: Inverter Direct Drive™ de alta eficiencia\n"
                            "• Filtro de pelusas ancho\n"
                            "• Garantía: 10 años en motor"
                        )
                    }
                }
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # 4. ESTUFAS Y CUBIERTAS
    # ─────────────────────────────────────────────────────────────────────────
    "estufa": {
        "nombre": "Estufas y Cubiertas",
        "emoji": "🍳",
        "alias": ["estufa", "estufas", "cubierta", "cubiertas", "cocina", "4"],
        "subcategorias": {
            "1": {
                "nombre": "🍳 Cubiertas (encimeras)",
                "productos": {
                    "1": {
                        "nombre": "Cubierta Mabe PM6044ENA0 (Gas Natural)",
                        "precio": "$499.000 COP",
                        "precio_num": 499000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍳 *Cubierta Mabe 4 Quemadores (Gas Natural)*\n"
                            "• 4 quemadores en acero inoxidable\n"
                            "• Parrillas de alambrón resistentes\n"
                            "• Potencia: 7.6 kW/h\n"
                            "• Encendido manual/electrónico"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Cubierta Mabe PM6044*\n"
                            "• Combustible: Gas natural\n"
                            "• Quemadores: 4 con potencia de 7.6 kW/h total\n"
                            "• Superficie: Acero inoxidable fácil de limpiar\n"
                            "• Parrillas: Alambrón de alta durabilidad\n"
                            "• Encendido: Manual y electrónico\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Cubierta Mabe PM6054NS0 Ultimate Cooking",
                        "precio": "$699.000 COP",
                        "precio_num": 699000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍳 *Cubierta Mabe Ultimate Cooking*\n"
                            "• Tecnología Ultimate Cooking\n"
                            "• Quemadores italianos multitamaño de gran potencia\n"
                            "• Encendido electrónico automático en perillas\n"
                            "• Parrillas de hierro fundido"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Cubierta Mabe PM6054*\n"
                            "• Tecnología: Ultimate Cooking con quemadores italianos\n"
                            "• Quemadores: Multitamaño de gran potencia y precisión\n"
                            "• Encendido: Electrónico automático integrado en las perillas\n"
                            "• Parrillas: Hierro fundido de alta resistencia\n"
                            "• Superficie: Ultimate Cleaning en acero inoxidable (fácil limpieza)\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "3": {
                        "nombre": "Cubierta Challenger SP6043 (4 puestos)",
                        "precio": "$449.000 COP",
                        "precio_num": 449000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍳 *Cubierta Challenger 4 Puestos*\n"
                            "• 4 puestos en acero inoxidable\n"
                            "• Parrillas de alambrón con 8 puntos de apoyo\n"
                            "• Alta durabilidad"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Cubierta Challenger SP6043*\n"
                            "• Combustible: Gas\n"
                            "• Puestos: 4 quemadores en acero inoxidable\n"
                            "• Parrillas: Alambrón de alta durabilidad con 8 puntos de apoyo\n"
                            "• Diseño: Funcional y resistente\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "2": {
                "nombre": "🍳 Estufas de Mesa",
                "productos": {
                    "1": {
                        "nombre": "Estufa Mesa Haceb Avellana T 6N NE (Gas Natural)",
                        "precio": "$599.000 COP",
                        "precio_num": 599000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍳 *Estufa Mesa Haceb Avellana (Gas Natural)*\n"
                            "• Diseño negro en estructura torre\n"
                            "• Fácil limpieza\n"
                            "• Gas natural"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Haceb Avellana Gas Natural*\n"
                            "• Combustible: Gas natural\n"
                            "• Diseño: Color negro con estructura en torre para fácil limpieza\n"
                            "• Práctica y funcional para cocinas modernas\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Estufa Mesa Haceb Avellana T GP NE (Gas Propano)",
                        "precio": "$619.000 COP",
                        "precio_num": 619000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍳 *Estufa Mesa Haceb Avellana (Gas Propano)*\n"
                            "• Mesa en acero inoxidable\n"
                            "• 4 quemadores (3 semirápidos, 1 rápido)\n"
                            "• Parrillas con puntos de apoyo estables\n"
                            "• Perillas ergonómicas"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Haceb Avellana Gas Propano*\n"
                            "• Combustible: Gas propano\n"
                            "• Mesa: Acero inoxidable resistente\n"
                            "• Quemadores: 4 (3 semirápidos + 1 rápido)\n"
                            "• Seguridad: Parrillas de alambrón con puntos de apoyo estables\n"
                            "• Ergonomía: Perillas de fácil manejo\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "3": {
                "nombre": "🍳 Estufas de Piso",
                "productos": {
                    "1": {
                        "nombre": "Estufa Piso Mabe TX1G 7CON INOX (4 Quemadores)",
                        "precio": "$1.199.000 COP",
                        "precio_num": 1199000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍳 *Estufa Piso Mabe 4 Quemadores INOX*\n"
                            "• Acero inoxidable sellado con capelo de cristal templado\n"
                            "• 4 quemadores multitamaño con encendido electrónico\n"
                            "• Horno con recubrimiento Easy Clean Pro"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Mabe TX1G 4 Quemadores*\n"
                            "• Cubierta: Acero inoxidable sellado\n"
                            "• Capelo: Cristal templado resistente\n"
                            "• Quemadores: 4 multitamaño con encendido electrónico por botón\n"
                            "• Horno: Recubrimiento Easy Clean Pro de fácil limpieza\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Estufa Piso Mabe Ingenious EMC30KXX-6 (6 Quemadores)",
                        "precio": "$1.799.000 COP",
                        "precio_num": 1799000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍳 *Estufa Piso Mabe 6 Quemadores*\n"
                            "• 6 quemadores multitamaño en acero inoxidable\n"
                            "• 2 parrillas de hierro fundido\n"
                            "• Capelo de cristal templado\n"
                            "• Horno con Easy Clean Pro anti-grasa"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Mabe Ingenious 6 Quemadores*\n"
                            "• Cubierta: Acero inoxidable con 6 quemadores multitamaño\n"
                            "• Parrillas: 2 de hierro fundido resistentes\n"
                            "• Capelo: Cristal templado protector\n"
                            "• Horno: Recubrimiento Easy Clean Pro anti-grasa\n"
                            "• Ideal: Cocinas profesionales y familias numerosas\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "3": {
                        "nombre": "Estufa Piso Centrales CC20ANXN-6 (Gas Natural)",
                        "precio": "$999.000 COP",
                        "precio_num": 999000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍳 *Estufa Piso Centrales 4 Quemadores*\n"
                            "• 4 quemadores con encendido manual por chispa\n"
                            "• Horno de 63 litros\n"
                            "• Potencia: 7.8 kW - Clase B\n"
                            "• Apta para alturas de 300 a 2800 msnm"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Centrales CC20ANXN-6*\n"
                            "• Combustible: Gas natural\n"
                            "• Quemadores: 4 con encendido manual por chispa\n"
                            "• Horno: 63 litros de capacidad\n"
                            "• Potencia: 7.8 kW nominal\n"
                            "• Eficiencia: Clase B, apta para alturas de 300 a 2800 msnm\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # 5. ELECTRODOMÉSTICOS DE COCINA Y HOGAR
    # ─────────────────────────────────────────────────────────────────────────
    "cocina_hogar": {
        "nombre": "Electrodomésticos de Cocina y Hogar",
        "emoji": "🏠",
        "alias": ["licuadora", "freidora", "sanduchera", "plancha", "electrodomestico", "pequeños electrodomesticos", "5"],
        "subcategorias": {
            "1": {
                "nombre": "🏠 Licuadoras",
                "productos": {
                    "1": {
                        "nombre": "Licuadora Hamilton Beach 3 en 1 (5352) 825W",
                        "precio": "$349.000 COP",
                        "precio_num": 349000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1570197788417-0e82375c9371?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🥤 *Licuadora Hamilton Beach 3 en 1*\n"
                            "• Potencia: 825 W\n"
                            "• Sistema 3 en 1: licúa, exprime y vasos personales\n"
                            "• Sistema Wave~Action® con 12 funciones\n"
                            "• Jarra de vidrio de 1.42 L"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Hamilton Beach 3 en 1*\n"
                            "• Potencia: 825 W de alta potencia\n"
                            "• Funciones: Sistema 3 en 1 (licúa, exprime y vasos personales con tapa)\n"
                            "• Tecnología: Wave~Action® para mezcla uniforme\n"
                            "• Programas: 12 funciones de licuado\n"
                            "• Jarra: Vidrio inastillable de 1.42 L (48 oz)\n"
                            "• Extra: Vertedor antigoteo\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Licuadora Electrolux EBS20 400W TruFlow™",
                        "precio": "$279.000 COP",
                        "precio_num": 279000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1570197788417-0e82375c9371?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🥤 *Licuadora Electrolux EBS20 400W*\n"
                            "• Potencia: 400 W\n"
                            "• Tecnología TruFlow™ con cuchillas de acero inoxidable\n"
                            "• Múltiples velocidades y función Pulse\n"
                            "• Jarra de cristal de 1.5 L útil"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Electrolux EBS20*\n"
                            "• Potencia: 400 W eficiente\n"
                            "• Tecnología: TruFlow™ Experience para mezclas perfectas\n"
                            "• Cuchillas: Acero inoxidable de alta durabilidad\n"
                            "• Velocidades: Múltiples + función Pulse\n"
                            "• Jarra: Cristal de 1.5 L útil (1.95 L total)\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "2": {
                "nombre": "🏠 Freidoras de Aire",
                "productos": {
                    "1": {
                        "nombre": "Freidora de Aire Digital Hamilton Beach 5.5L",
                        "precio": "$449.000 COP",
                        "precio_num": 449000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1585515320310-259814833e62?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🍟 *Freidora de Aire Digital Hamilton Beach*\n"
                            "• Capacidad: 5.5 Litros\n"
                            "• Acero inoxidable con panel digital\n"
                            "• 8 funciones preestablecidas\n"
                            "• Temperatura: 175°F a 400°F"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Freidora Hamilton Beach 5.5L*\n"
                            "• Capacidad: 5.5 Litros (ideal para familias)\n"
                            "• Materiales: Acero inoxidable de alta calidad\n"
                            "• Panel: Digital con 8 funciones preestablecidas\n"
                            "• Temperatura: Control de 175°F a 400°F\n"
                            "• Cocina sin aceite o con muy poco aceite\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "3": {
                "nombre": "🏠 Sanducheras y Planchas",
                "productos": {
                    "1": {
                        "nombre": "Sanduchera Electrolux ESG20 Efficient Inox",
                        "precio": "$199.000 COP",
                        "precio_num": 199000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🥪 *Sanduchera Electrolux ESG20*\n"
                            "• Detalles en acero inoxidable cepillado\n"
                            "• Tecnología de calentamiento rápido\n"
                            "• 2 placas calefactoras antiadherentes"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Sanduchera Electrolux ESG20*\n"
                            "• Diseño: Acero inoxidable cepillado (Efficient Inox)\n"
                            "• Calentamiento: Tecnología de calentamiento rápido\n"
                            "• Placas: 2 placas calefactoras antiadherentes\n"
                            "• Fácil limpieza y mantenimiento\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Plancha de Vapor Hamilton Beach 1200W",
                        "precio": "$179.000 COP",
                        "precio_num": 179000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "👔 *Plancha de Vapor Hamilton Beach*\n"
                            "• Potencia: 1200 W\n"
                            "• Control de temperatura por tipo de tela\n"
                            "• Tecnología antigoteo\n"
                            "• Ventana visible para nivel de agua"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Plancha Hamilton Beach*\n"
                            "• Potencia: 1200 W para vapor potente\n"
                            "• Control: Temperatura ajustable por tipo de tela\n"
                            "• Antigoteo: Tecnología que evita manchas en la ropa\n"
                            "• Agua: Ventana visible para controlar nivel fácilmente\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # 6. EQUIPOS DE SONIDO Y PARLANTES
    # ─────────────────────────────────────────────────────────────────────────
    "sonido": {
        "nombre": "Equipos de Sonido y Parlantes",
        "emoji": "🔊",
        "alias": ["sonido", "parlante", "parlantes", "barra de sonido", "equipo de sonido", "bocina", "6"],
        "subcategorias": {
            "1": {
                "nombre": "🔊 Barras de Sonido",
                "productos": {
                    "1": {
                        "nombre": "Barra de Sonido Challenger SB30Y (30W)",
                        "precio": "$399.000 COP",
                        "precio_num": 399000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🔊 *Barra de Sonido Challenger SB30Y*\n"
                            "• Potencia: 30W RMS\n"
                            "• Bluetooth 5.3, HDMI ARC, Óptica, AUX y USB\n"
                            "• Modos EQ (Película, Música, Noticias)\n"
                            "• Diseño ultradelgado 80 cm"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger SB30Y*\n"
                            "• Potencia: 30W RMS\n"
                            "• Conectividad: Bluetooth 5.3, HDMI ARC, Óptica, AUX y USB\n"
                            "• Modos de sonido: EQ para Película, Música y Noticias\n"
                            "• Instalación: Soporte de pared incluido\n"
                            "• Diseño: Ultradelgado de 80 cm, elegante\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Barra de Sonido Challenger SB80Y + Subwoofer (80W)",
                        "precio": "$699.000 COP",
                        "precio_num": 699000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🔊 *Barra de Sonido Challenger SB80Y 2.1*\n"
                            "• Potencia: 80W RMS (40W barra + 40W subwoofer)\n"
                            "• Sistema 2.1 canales con bajos potentes\n"
                            "• Bluetooth 5.3, HDMI ARC, Óptica, AUX y USB"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger SB80Y 2.1*\n"
                            "• Potencia: 80W RMS total (40W barra + 40W subwoofer con cable)\n"
                            "• Sistema: 2.1 canales con bajos profundos\n"
                            "• Conectividad: Bluetooth 5.3, HDMI ARC, Óptica, AUX y USB\n"
                            "• Subwoofer: 14 cm x 36 cm x 22 cm\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "2": {
                "nombre": "🔊 Equipos de Sonido LG",
                "productos": {
                    "1": {
                        "nombre": "Equipo de Sonido LG RNC7 1000W",
                        "precio": "$1.499.000 COP",
                        "precio_num": 1499000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🔊 *Equipo de Sonido LG RNC7 1000W*\n"
                            "• Potencia: 1000W RMS\n"
                            "• Subwoofer + doble bocinas de medios + Tweeter\n"
                            "• Wireless Party Link, Karaoke Star y Radio FM\n"
                            "• Iluminación multicolor y DJ App/Pad"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG RNC7*\n"
                            "• Potencia: 1000W RMS de alto impacto\n"
                            "• Componentes: Subwoofer + doble bocinas de medios + Tweeter\n"
                            "• Funciones: Wireless Party Link para enlazar equipos\n"
                            "• Iluminación: Multicolor/Party Strobe\n"
                            "• Extras: DJ App/Pad, Karaoke Star y Radio FM\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Equipo de Sonido LG RNC9 1800W",
                        "precio": "$2.199.000 COP",
                        "precio_num": 2199000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🔊 *Equipo de Sonido LG RNC9 1800W*\n"
                            "• Potencia: 1800W RMS\n"
                            "• Doble subwoofer con potenciador de bajos\n"
                            "• Wireless Party Link y Karaoke Star\n"
                            "• Iluminación multicolor y Radio FM"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - LG RNC9*\n"
                            "• Potencia: 1800W RMS bestial\n"
                            "• Componentes: Doble subwoofer con potenciador de bajos\n"
                            "• Funciones: Wireless Party Link para conectar varios equipos\n"
                            "• Iluminación: Multicolor/Party Strobe para fiestas\n"
                            "• Extras: DJ App/Pad, Karaoke Star y Radio FM\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "3": {
                "nombre": "🔊 Parlantes Portátiles",
                "productos": {
                    "1": {
                        "nombre": "Parlante Portátil Challenger SC5 (5W IPX7)",
                        "precio": "$149.000 COP",
                        "precio_num": 149000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🔊 *Parlante Portátil Challenger SC5*\n"
                            "• Potencia: 5W RMS\n"
                            "• Impermeabilidad IPX7\n"
                            "• Bluetooth 5.3, USB-C, microSD, TWS\n"
                            "• Radio FM y manos libres"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger SC5*\n"
                            "• Potencia: 5W RMS\n"
                            "• Resistencia: IPX7 (sumergible hasta 1m)\n"
                            "• Conectividad: Bluetooth 5.3, USB Tipo-C, microSD, TWS\n"
                            "• Extras: Radio FM, manos libres e indicador LED\n"
                            "• Portátil y compacto para llevar a cualquier lugar\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "Parlante Inalámbrico Challenger SC100 (100W 360°)",
                        "precio": "$699.000 COP",
                        "precio_num": 699000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🔊 *Parlante Challenger SC100 360°*\n"
                            "• Potencia: 100W (sonido 360°)\n"
                            "• Batería: 7000 mAh\n"
                            "• Bluetooth 5.3, TWS y Modo Karaoke\n"
                            "• Resistencia IPX5 con iluminación LED RGB"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Challenger SC100*\n"
                            "• Potencia: 100W con sonido envolvente 360°\n"
                            "• Batería: 7000 mAh de larga duración\n"
                            "• Conectividad: Bluetooth 5.3, Modo TWS para doble parlante\n"
                            "• Extras: Modo Karaoke integrado\n"
                            "• Resistencia: IPX5 ante salpicaduras\n"
                            "• Iluminación: LED RGB para fiestas\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "3": {
                        "nombre": "Parlante Anker Soundcore Rave 3 Black",
                        "precio": "$849.000 COP",
                        "precio_num": 849000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "🔊 *Parlante Anker Soundcore Rave 3*\n"
                            "• Audio claro y potente de alta calidad\n"
                            "• Diseño compacto ideal para interiores y exteriores"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Anker Soundcore Rave 3*\n"
                            "• Marca: Anker (reconocida por calidad de audio)\n"
                            "• Audio: Claro, potente y envolvente\n"
                            "• Diseño: Compacto ideal para interiores y exteriores\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # 7. COMPUTADORES PORTÁTILES
    # ─────────────────────────────────────────────────────────────────────────
    "computador": {
        "nombre": "Computadores Portátiles",
        "emoji": "💻",
        "alias": ["computador", "computadores", "portátil", "portatil", "laptop", "pc", "asus", "lenovo", "7"],
        "subcategorias": {
            "1": {
                "nombre": "💻 ASUS Vivobook",
                "productos": {
                    "1": {
                        "nombre": "ASUS Vivobook Go 15 AMD Ryzen 3 (E1504FA)",
                        "precio": "$1.799.000 COP",
                        "precio_num": 1799000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "💻 *ASUS Vivobook Go 15 AMD Ryzen 3*\n"
                            "• Procesador: AMD Ryzen 3 7320U\n"
                            "• RAM: 8 GB LPDDR5\n"
                            "• Almacenamiento: 512 GB SSD\n"
                            "• Pantalla: 15.6\" Full HD\n"
                            "• Sistema: Windows 11 Home"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - ASUS Vivobook Go 15 AMD*\n"
                            "• Procesador: AMD Ryzen 3 7320U de alta eficiencia\n"
                            "• Memoria RAM: 8 GB LPDDR5 de alta velocidad\n"
                            "• Almacenamiento: 512 GB SSD (inicio ultrarrápido)\n"
                            "• Pantalla: 15.6\" Full HD (1920x1080)\n"
                            "• Sistema Operativo: Windows 11 Home\n"
                            "• Ideal para estudiantes y trabajo cotidiano\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    },
                    "2": {
                        "nombre": "ASUS Vivobook Go 15 Intel Core i3 (E1504GA)",
                        "precio": "$1.899.000 COP",
                        "precio_num": 1899000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "💻 *ASUS Vivobook Go 15 Intel Core i3*\n"
                            "• Procesador: Intel Core i3-N305 (8 núcleos)\n"
                            "• RAM: 8 GB\n"
                            "• Almacenamiento: 512 GB SSD\n"
                            "• Pantalla: 15.6\" Full HD\n"
                            "• Sistema: Windows 11"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - ASUS Vivobook Go 15 Intel*\n"
                            "• Procesador: Intel Core i3-N305 con 8 núcleos eficientes\n"
                            "• Memoria RAM: 8 GB\n"
                            "• Almacenamiento: 512 GB SSD\n"
                            "• Pantalla: 15.6\" Full HD nítida\n"
                            "• Sistema Operativo: Windows 11\n"
                            "• Multitarea fluida con 8 núcleos\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            },
            "2": {
                "nombre": "💻 Lenovo IdeaPad",
                "productos": {
                    "1": {
                        "nombre": "Lenovo IdeaPad Slim 3 14\" Intel Core i5",
                        "precio": "$2.299.000 COP",
                        "precio_num": 2299000,
                        "imagenes": [
                            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80"
                        ],
                        "descripcion_corta": (
                            "💻 *Lenovo IdeaPad Slim 3 14\"*\n"
                            "• Procesador: Intel Core i5-12450H\n"
                            "• RAM: 8 GB\n"
                            "• Almacenamiento: 512 GB SSD\n"
                            "• Pantalla: 14\" Full HD\n"
                            "• Diseño slim ultraportátil"
                        ),
                        "descripcion_amplia": (
                            "📋 *Descripción Detallada - Lenovo IdeaPad Slim 3*\n"
                            "• Procesador: Intel Core i5-12450H de alto rendimiento\n"
                            "• Memoria RAM: 8 GB\n"
                            "• Almacenamiento: 512 GB SSD ultrarrápido\n"
                            "• Pantalla: 14\" Full HD compacta y nítida\n"
                            "• Diseño: Slim ultraportátil, fácil de llevar\n"
                            "• Ideal para profesionales y estudiantes avanzados\n"
                            "• Garantía: 1 año de fábrica"
                        )
                    }
                }
            }
        }
    }
}


# =============================================================================
# FUNCIONES DE BÚSQUEDA
# =============================================================================

def obtener_categoria_por_alias(termino, catalogo=None):
    """Busca categoría en el catálogo indicado o en el catálogo de respaldo."""
    from src.catalogo_builder import obtener_categoria_por_alias as _buscar

    return _buscar(termino, catalogo or CATALOGO)


def obtener_producto_por_nombre_o_alias(termino):
    """Compatibilidad con código anterior: busca categoría por alias."""
    return obtener_categoria_por_alias(termino)
