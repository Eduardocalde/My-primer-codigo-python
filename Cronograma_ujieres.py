import random

UJIERES = [
    "Yendery Guerra", "Karelys de Rodriguez", "Jesus Rodriguez", 
    "Obdalis Martinez", "Jeniffer Guerra", "Merki Calderon", 
    "Nakary Torres", "Jenny Maurera"
]

PUESTOS_ESTANDAR = ["Puerta", "Agua", "Escalera", "Baños"]

def obtener_rotacion(lista, cantidad):
    """Mezcla la lista y devuelve la cantidad de personas solicitadas."""
    copia = lista.copy()
    random.shuffle(copia)
    return copia[:cantidad]

def generar_semana_completa():
    print("=== GENERADOR DE CRONOGRAMA SEMANAL ===")
    
    # Preguntar por el Sábado
    hay_sabado = input("¿Hay actividad el Sábado? (s/n): ").strip().lower() == 's'
    nota_sabado = ""
    if hay_sabado:
        actividad = input("Nombre de la actividad del Sábado (ej. Actividad en la cancha): ").strip()
        nota_sabado = input("Nota de vestimenta o aviso (ej. Sudadera vinotinto): ").strip()

    print("\n" + "="*40)
    print("   CRONOGRAMA DE LA SEMANA - UJIERES")
    print("="*40)

    # Días Regulares
    dias_regulares = ["Martes", "Jueves", "Viernes", "Domingo"]
    
    for dia in dias_regulares:
        print(f"\n📌 {dia}")
        print("-" * 20)
        asignados = obtener_rotacion(UJIERES, 4)
        for puesto, persona in zip(PUESTOS_ESTANDAR, asignados):
            print(f"{puesto}: {persona}")

    # Sábado si aplica
    if hay_sabado:
        print(f"\n📌 Sabado")
        print("-" * 20)
        if actividad:
            print(f"[{actividad}]")
        asignados_sab = obtener_rotacion(UJIERES, 2)
        print(f"Puerta: {asignados_sab[0]}")
        print(f"Agua: {asignados_sab[1]}")
        if nota_sabado:
            print(f"\n📝 NOTA: Para el sabado {nota_sabado}")

    print("\n" + "="*40)

if __name__ == "__main__":
    generar_semana_completa()
