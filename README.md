# 🤖 ChatBot Almacén Oportunidades Pitalito - Asistente de Ventas

**ChatBot Almacén Oportunidades** es un asistente virtual  
diseñado para automatizar la atención al cliente y el cierre de ventas de un almacén de electrodomésticos.

Todo el inventario, clientes, ventas e intereses se gestionan directamente en la base de datos MySQL **`almacen_oportunidades`**.

---

## 🚀 Características Principales

*   **🧠 Flujo programado por estados**: Respuestas siguiendo una secuencia definida:
    ```
    Bienvenida → Categoría → Subcategoría/Marca → Producto →
    Contado / Financiado → Cédula+Correo → ✅ Venta registrada
    ```
*   **📊 Inventario en tiempo real desde MySQL**: Lee la tabla `articulos` y agrupa por categoría y marca al iniciar.
*   **💰 Cierre de ventas automático**: Registra clientes, ventas y detalle de ventas en las tablas `clientes`, `ventas`, `detalle_ventas`.
*   **📈 Registro de intereses (Leads)**: Guarda cada búsqueda del cliente en la tabla `intereses` para analizar demanda.
*   **🛒 Carrito por sesión**: Maneja múltiples conversaciones simultáneas sin mezclar pedidos.
*   **💬 3 vías de integración con WhatsApp**: WPPConnect (pruebas rápidas), Meta Cloud API (producción), Twilio (alternativa).

---

## 🛠️ Tecnologías Utilizadas

**Backend (Cerebro del bot):**
*   **Python 3.10+**
*   **Flask** — Servidor web con 2 endpoints principales:
    *   `POST /procesar` → Recibe mensajes del puente WPPConnect (pruebas)
    *   `GET/POST /webhook` → Integración oficial con WhatsApp Business API
*   **PyMySQL / mysql-connector-python** — Conexión a MySQL

**Puente WhatsApp (pruebas locales sin cuenta Business):**
*   **Node.js 18+**
*   **@wppconnect-team/wppconnect** — Emula WhatsApp Web, escanea QR y reenvía mensajes a Flask.
*   **Express** — Endpoint de estado y envío manual de mensajes.

---

## 🗄️ Base de Datos MySQL Requerida

La BD **`almacen_oportunidades`** debe tener estas 5 tablas (coincidentes con tu diagrama ER):

| Tabla | Columnas clave | Uso en el bot |
|---|---|---|
| `clientes` | `id_cliente`, `telefono`, `nombre`, `direccion` | Registrar/actualizar clientes por teléfono |
| `articulos` | `id_articulo`, `referencia`, `nombre`, `marca`, `categoria`, `estado`, `precio` | **Inventario principal**. Si no hay filas, se usa catálogo de respaldo (`src/catalogo.py`) |
| `intereses` | `id_interes`, `id_cliente`, `termino_busqueda`, `fecha_busqueda` | Qué busca cada cliente |
| `ventas` | `id_venta`, `id_cliente`, `fecha_venta`, `total` | Pedido confirmado |
| `detalle_ventas` | `id_detalle`, `id_venta`, `id_articulo`, `cantidad`, `precio_item` | Productos específicos del pedido |

---

## ⚙️ Configuración e Instalación

### 1. Prerrequisitos
*   Python 3.10+ y `pip`
*   Node.js 18+ y `npm`
*   MySQL con la BD `almacen_oportunidades` creada y la tabla `articulos` alimentada.

### 2. Instalación de dependencias

**Python (Backend):**
```bash
pip install -r requirements.txt
```

**Node.js (WPPConnect - puente WhatsApp):**
```bash
cd wpp-server
npm install
```

### 3. Configurar variables de entorno (`.env`)
Edita el archivo `.env` en la raíz y completa **solo** las credenciales MySQL:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña     
DB_NAME=almacen_oportunidades
DB_PORT=3306
```
> Las credenciales de Meta Cloud API (WHATSAPP_TOKEN, etc.) se dejan vacías si usas WPPConnect.

---

## ▶️ Ejecución

### Modo Simulador (prueba lógica sin WhatsApp)
Valida el flujo completo directamente en terminal:
```bash
python main_simulador.py
```
Escribe `hola`, `1`, `nevera`, etc. para probar el menú, categorías y registro de venta.

---

### Modo Pruebas con WhatsApp (RECOMENDADO para empezar)
Usa tu WhatsApp personal vinculado con WPPConnect. Necesitas **2 terminales**:

**Terminal 1 — Iniciar Cerebro (Flask):**
```bash
python app.py
```
→ Espera el mensaje: `✅ Bot iniciado correctamente` y `Servidor Flask en puerto 5000`

**Terminal 2 — Iniciar puente WPPConnect:**
```bash
cd wpp-server
$env:WPP_SESSION="chatbot-suc146"; npm start
```
1.  Se abrirá una ventana de Chrome con un código QR.
2.  Desde tu WhatsApp → Menú → **Dispositivos vinculados** → **Vincular un dispositivo**.
3.  Escanea el QR.
4.  Espera el mensaje `✅ ¡WhatsApp conectado exitosamente!`.
5.  Desde **otro WhatsApp**, envía un mensaje al número vinculado y responde con el menú.

> 💡 Si quieres ejecutar Chrome oculto, cambia `headless: false` a `true` en `wpp-server/server.js` línea 15.

---

### Modo Producción (WhatsApp Business API / Meta)
Cuando tengas cuenta oficial:
1.  Configura `WHATSAPP_TOKEN`, `PHONE_NUMBER_ID`, `VERIFY_TOKEN` en `.env`.
2.  Configura el webhook en Meta Developers apuntando a tu servidor HTTPS con la ruta `/webhook`.
3.  Ejecuta:
    ```bash
    python app.py
    ```

---

## 📂 Estructura del Proyecto

```
ChatBot SUC146/
├── src/
│   ├── database.py        # Conexión MySQL + CRUD (clientes/articulos/intereses/ventas)
│   ├── inventario.py      # InventarioService: prioriza BD → luego CSV respaldo
│   ├── catalogo_builder.py# Construye catálogo agrupado (categoria → marca → producto)
│   ├── catalogo.py        # Catálogo hardcodeado de respaldo
│   └── cerebro.py         # MAQUINA DE ESTADOS (8 estados) - procesa todos los mensajes
├── wpp-server/
│   ├── server.js          # WPPConnect bridge - QR + escucha mensajes + POST a Flask
│   ├── message-utils.js   # Helpers: extraer texto, normalizar teléfono
│   ├── package.json
│   └── tests/             # Tests unitarios Node
├── data/
│   └── inventario.csv     # (Opcional) Inventario CSV si MySQL está vacío
├── tests/                 # Tests Python de cerebro y catálogo
├── app.py                 # Flask: endpoints /procesar y /webhook (Meta API)
├── app_twilio.py          # Alternativa Twilio
├── main_simulador.py      # Prueba en consola sin WhatsApp
├── requirements.txt
├── .env                   # Variables de entorno (NO subir a git)
└── README.md
```

## 📝 Autor
Desarrollado para **Almacén Oportunidades - SUC146**.
