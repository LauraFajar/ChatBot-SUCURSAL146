import sys
import os
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from src.cerebro import Brain

def main():
    print("=============================================")
    print("🤖 CHATBOT DE VENTAS (MODO SIMULADOR)")
    print("=============================================")
    print("Escribe 'salir' para terminar o 'inicio' para reiniciar.")
    print("---------------------------------------------")

    bot = Brain()

    print("\nBot: ¡Hola! 👋 Escribe '1' o 'nevera' para comenzar las pruebas del flujo.\n")

    while True:
        try:
            usuario_input = input("Tú: ")

            if usuario_input.lower() in ['salir', 'exit', 'adios']:
                print("\nBot: ¡Gracias por visitarnos! 👋")
                break

            if not usuario_input.strip():
                continue

            res = bot.procesar_mensaje(usuario_input, "TEST_USER")

            if isinstance(res, dict):
                texto = res.get("texto", "")
                imagenes = res.get("imagenes", [])
            else:
                texto = str(res)
                imagenes = []

            print(f"\nBot: {texto}")

            if imagenes:
                print("\n📷 [ADJUNTOS ENVIADOS EN EL MENSAJE]:")
                for idx, img in enumerate(imagenes, 1):
                    print(f"   🖼️ Imagen {idx}: {img}")

            print("-" * 50 + "\n")

        except KeyboardInterrupt:
            print("\nBot: ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
