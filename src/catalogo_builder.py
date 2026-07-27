"""
Construye la estructura de catálogo del bot a partir de la tabla `articulos`.
"""
import re
import unicodedata
from collections import defaultdict


EMOJI_POR_CATEGORIA = {
    "televisor": "📺",
    "televisores": "📺",
    "nevera": "❄️",
    "neveras": "❄️",
    "refrigerador": "❄️",
    "refrigeradores": "❄️",
    "lavadora": "🧺",
    "lavadoras": "🧺",
    "estufa": "🍳",
    "estufas": "🍳",
    "cubierta": "🍳",
    "cubiertas": "🍳",
    "cocina": "🏠",
    "hogar": "🏠",
    "sonido": "🔊",
    "parlante": "🔊",
    "parlantes": "🔊",
    "computador": "💻",
    "computadores": "💻",
    "portatil": "💻",
    "portátil": "💻",
    "laptop": "💻",
    "congelador": "🧊",
    "congeladores": "🧊",
    "nevecon": "❄️",
    "nevecones": "❄️",
}

ESTADOS_NO_DISPONIBLES = {
    "agotado",
    "sin stock",
    "no disponible",
    "inactivo",
    "vendido",
}


def _slugify(texto):
    if not texto:
        return "general"
    normalizado = unicodedata.normalize("NFKD", str(texto))
    ascii_text = normalizado.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_text.lower()).strip("_")
    return slug or "general"


def _emoji_para_categoria(nombre_categoria):
    clave = _slugify(nombre_categoria).replace("_", " ")
    for palabra, emoji in EMOJI_POR_CATEGORIA.items():
        if palabra in clave or palabra in nombre_categoria.lower():
            return emoji
    return "📦"


def _formato_precio(precio):
    try:
        valor = float(precio or 0)
    except (TypeError, ValueError):
        return "Consultar precio", 0.0

    if valor <= 0:
        return "Consultar precio", 0.0

    entero = int(round(valor))
    texto = f"${entero:,}".replace(",", ".")
    return f"{texto} COP", valor


def _producto_disponible(estado):
    if not estado:
        return True
    return str(estado).lower().strip() not in ESTADOS_NO_DISPONIBLES


def _descripcion_corta(articulo, precio_texto, disponible):
    lineas = [
        f"*{articulo.get('nombre', 'Producto')}*",
        f"• Marca: {articulo.get('marca') or 'N/D'}",
        f"• Referencia: {articulo.get('referencia') or 'N/D'}",
        f"• Precio: *{precio_texto}*",
    ]
    if articulo.get("estado"):
        lineas.append(f"• Estado: {articulo['estado']}")
    if not disponible:
        lineas.append("• ⚠️ Producto temporalmente no disponible")
    return "\n".join(lineas)


def _descripcion_amplia(articulo, precio_texto, disponible):
    lineas = [
        f"📋 *Detalle del producto*",
        f"• Nombre: {articulo.get('nombre', 'Producto')}",
        f"• Marca: {articulo.get('marca') or 'N/D'}",
        f"• Referencia: {articulo.get('referencia') or 'N/D'}",
        f"• Categoría: {articulo.get('categoria') or 'General'}",
        f"• Precio: *{precio_texto}*",
    ]
    if articulo.get("estado"):
        lineas.append(f"• Estado en inventario: {articulo['estado']}")
    if not disponible:
        lineas.append("• Este artículo no está disponible para compra en este momento.")
    else:
        lineas.append("• Producto sujeto a confirmación de stock con un asesor.")
    return "\n".join(lineas)


def _articulo_a_producto(articulo):
    precio_texto, precio_num = _formato_precio(articulo.get("precio"))
    disponible = _producto_disponible(articulo.get("estado"))

    return {
        "id_articulo": articulo.get("id_articulo"),
        "nombre": articulo.get("nombre") or "Producto sin nombre",
        "referencia": articulo.get("referencia"),
        "marca": articulo.get("marca"),
        "categoria": articulo.get("categoria"),
        "estado": articulo.get("estado"),
        "disponible": disponible,
        "precio": precio_texto,
        "precio_num": precio_num,
        "imagenes": [],
        "descripcion_corta": _descripcion_corta(articulo, precio_texto, disponible),
        "descripcion_amplia": _descripcion_amplia(articulo, precio_texto, disponible),
    }


def construir_catalogo_desde_articulos(articulos):
    """
    Agrupa artículos por categoría y marca para el flujo conversacional del bot.
    Retorna None si no hay artículos.
    """
    if not articulos:
        return None

    por_categoria = defaultdict(list)
    for articulo in articulos:
        categoria = (articulo.get("categoria") or "General").strip()
        por_categoria[categoria].append(articulo)

    catalogo = {}

    for nombre_categoria, items_categoria in sorted(por_categoria.items(), key=lambda x: x[0].lower()):
        clave_categoria = _slugify(nombre_categoria)
        if clave_categoria in catalogo:
            clave_categoria = f"{clave_categoria}_{len(catalogo)}"

        por_marca = defaultdict(list)
        for articulo in sorted(items_categoria, key=lambda a: (a.get("nombre") or "").lower()):
            marca = (articulo.get("marca") or "Varios").strip()
            por_marca[marca].append(articulo)

        subcategorias = {}
        for idx_marca, (marca, productos_marca) in enumerate(sorted(por_marca.items(), key=lambda x: x[0].lower()), start=1):
            productos = {}
            for idx_prod, articulo in enumerate(productos_marca, start=1):
                productos[str(idx_prod)] = _articulo_a_producto(articulo)

            subcategorias[str(idx_marca)] = {
                "nombre": marca,
                "productos": productos,
            }

        alias = {
            clave_categoria,
            nombre_categoria.lower(),
            _slugify(nombre_categoria).replace("_", " "),
        }
        alias.update(p.lower() for p in nombre_categoria.split() if len(p) > 2)

        catalogo[clave_categoria] = {
            "nombre": nombre_categoria,
            "emoji": _emoji_para_categoria(nombre_categoria),
            "alias": sorted(alias),
            "subcategorias": subcategorias,
        }

    return catalogo or None


def obtener_categoria_por_alias(termino, catalogo):
    """Busca categoría por clave, alias o coincidencia parcial."""
    if not catalogo:
        return None, None

    t = termino.lower().strip()
    for clave, item in catalogo.items():
        if t == clave or t in item.get("alias", []):
            return clave, item

    for clave, item in catalogo.items():
        nombre = item.get("nombre", "").lower()
        if t in nombre or nombre in t:
            return clave, item

    return None, None
