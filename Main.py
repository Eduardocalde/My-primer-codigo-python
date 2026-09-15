import datetime

def saludar_usuario(nombre):
    """Muestra un mensaje de bienvenida personalizado."""
    print("---------------------------------------")
    print(f"   ¡HOLA, {nombre.upper()}! BIENVENIDO   ")
    print("---------------------------------------")

def calcular_experiencia(año_inicio):
    """Calcula cuántos años llevas explorando el código."""
    año_actual = datetime.date.today().year
    años = año_actual - año_inicio
    return años

def mostrar_menu():
    """Despliega un menú interactivo en la consola."""
    print("\n--- MENÚ DE OPCIONES ---")
    print("1. Ver recomendación del día")
    print("2. Calcular tiempo en programación")
    print("3. Salir")

# --- PROGRAMA PRINCIPAL ---
def ejecutar_programa():
    usuario = input("¿Cuál es tu nombre? ")
    saludar_usuario(usuario)

    continuar = True
    while continuar:
        mostrar_menu()
        opcion = input("\nElige una opción (1-3): ")

        if opcion == "1":
            print("\n💡 Consejo Open Source: La clave para aprender es leer código de otros y practicar a diario.")
        elif opcion == "2":
            año = int(input("¿En qué año empezaste o piensas empezar a programar? "))
            tiempo = calcular_experiencia(año)
            if tiempo == 0:
                print(f"\n🚀 ¡Este es tu año de inicio ({datetime.date.today().year})! Estás comenzando un excelente camino.")
            else:
                print(f"\n📈 Llevas aproximadamente {tiempo} año(s) en el mundo de la tecnología.")
        elif opcion == "3":
            print(f"\n¡Hasta luego, {usuario}! Sigue practicando.")
            continuar = False
        else:
            print("\n⚠️ Opción no válida. Intenta de nuevo.")

# Iniciar el programa
if __name__ == "__main__":
    ejecutar_programa()
