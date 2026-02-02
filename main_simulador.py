from src.cerebro import Brain
import os

def main():
    print("=============================================")
    print("🤖 CHATBOT DE VENTAS (MODO SIMULADOR)")
    print("=============================================")
    print("Escribe 'salir' para terminar.")
    print("---------------------------------------------")
    
    bot = Brain()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("ℹ️  Tip: Para activar la IA real, crea un archivo .env con GEMINI_API_KEY=tu_clave")
        print("   Por ahora funcionará en modo 'Reglas Básicas'. Pruebe buscando 'nevera' o 'lavadora'.")
    
    print("\nBot: ¡Hola! 👋 Bienvenido a ElectroHogar. Soy tu asistente virtual. ¿Qué estás buscando hoy?\n")

    while True:
        try:
            usuario_input = input("Tú: ")
            
            if usuario_input.lower() in ['salir', 'exit', 'adios']:
                print("\nBot: ¡Gracias por visitarnos! 👋")
                break
                
            if not usuario_input.strip():
                continue
                
            respuesta = bot.procesar_mensaje(usuario_input, "TEST_USER")
            
            print(f"Bot: {respuesta}\n")
            
        except KeyboardInterrupt:
            print("\nBot: ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
