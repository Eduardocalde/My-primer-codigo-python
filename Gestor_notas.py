import os

NOMBRE_ARCHIVO = "notas.txt"

def cargar_notas():
    """Lee el archivo de texto y devuelve una lista con las tareas guardadas."""
    notas = []
    if os.path.exists(NOMBRE_ARCHIVO):
        with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as archivo:
            notas = [linea.strip() for linea in archivo.readlines()]
    return notas

def guardar_notas(notas):
    """Escribe la lista de tareas dentro del archivo de texto."""
    with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as archivo:
        for nota in notas:
            archivo.write(f"{nota}\n")

def mostrar_notas(notas):
    """Muestra todas las tareas registradas con su número de índice."""
    print("\n--- TUS NOTAS Y TAREAS ---")
    if not notas:
        print("📌 No tienes tareas registradas actualmente.")
    else:
        for i, nota in enumerate(notas, 1):
            print(f"{i}. {nota}")
    print("--------------------------")

def agregar_nota(notas):
    """Solicita una nueva tarea y la añade a la lista."""
    nueva_nota = input("\n✍️ Escribe la nueva nota o tarea: ").strip()
    if nueva_nota:
        notas.append(nueva_nota)
        guardar_notas(notas)
        print("✅ ¡Nota guardada exitosamente!")
    else:
        print("⚠️ No ingresaste ningún texto.")

def eliminar_nota(notas):
    """Elimina una tarea según el número seleccionado por el usuario."""
    mostrar_notas(notas)
    if not notas:
        return

    try:
        numero = int(input("\n❌ Ingrese el número de la tarea a eliminar: "))
        if 1 <= numero <= len(notas):
            eliminada = notas.pop(numero - 1)
            guardar_notas(notas)
            print(f"🗑️ Se ha eliminado: '{eliminada}'")
        else:
            print("⚠️ Número fuera de rango.")
    except ValueError:
        print("⚠️ Ingresa un número válido.")

def ejecutar_gestor():
    """Bucle principal de ejecución de la aplicación."""
    notas = cargar_notas()

    while True:
        print("\n=== GESTOR DE NOTAS (OPEN SOURCE) ===")
        print("1. Ver todas las notas")
        print("2. Agregar nueva nota")
        print("3. Eliminar una nota")
        print("4. Salir")

        opcion = input("\nElige una opción (1-4): ").strip()

        if opcion == "1":
            mostrar_notas(notas)
        elif opcion == "2":
            agregar_nota(notas)
        elif opcion == "3":
            eliminar_nota(notas)
        elif opcion == "4":
            print("\n👋 ¡Gracias por usar el Gestor de Notas! Tus cambios se guardaron automáticamente.")
            break
        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    ejecutar_gestor()
