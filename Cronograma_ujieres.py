import random
import json
import os

UJIERES = [
    "Yendery Guerra", "Karelys de Rodriguez", "Jesus Rodriguez", 
    "Obdalis Martinez", "Jeniffer Guerra", "Merki Calderon", 
    "Nakary Torres", "Jenny Maurera"
]

PUESTOS_HABITUALES = ["Puerta", "Agua", "Escalera", "Baños"]
ARCHIVO_HISTORIAL = "historial_ujieres.json"
ARCHIVO_SALIDA = "cronograma_generado.txt"

def cargar_historial():
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_historial(historial):
    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

def seleccionar_puesto(disponibles, historial, puesto, preferidos=[]):
    """Busca asignar prioritariamente a alguien preferido o que no haya repetido el puesto."""
    candidatos = [p for p in preferidos if p in disponibles]
    if not candidatos:
        candidatos = [p for p in disponibles if historial.get(p) != puesto]
    if not candidatos:
        candidatos = disponibles.copy()
    
    elegido = random.choice(candidatos)
    disponibles.remove(elegido)
    historial[elegido] = puesto
    return elegido

def obtener_disponibles_dia(dia_nombre, ausentes_generales):
    """Filtra la lista de ujieres según la disponibilidad fija por día de la semana."""
    disponibles = [u for u in UJIERES if u not in ausentes_generales]
    
    if dia_nombre == "Domingo":
        # Yendery y Karelys libran los Domingos
        disponibles = [u for u in disponibles if u not in ["Yendery Guerra", "Karelys de Rodriguez"]]
    else:
        # Nakary solo asiste los Domingos (libre los demás días)
        disponibles = [u for u in disponibles if u != "Nakary Torres"]
        
    return disponibles

def generar_dia(dia_nombre, ausentes_generales, historial):
    disponibles_dia = obtener_disponibles_dia(dia_nombre, ausentes_generales)
    asignacion = {}
    
    # Asignaciones preferenciales para el área de Agua (Martes, Jueves, Viernes)
    if dia_nombre in ["Martes", "Jueves", "Viernes"]:
        preferidos_agua = [p for p in ["Jenny Maurera", "Jeniffer Guerra"] if p in disponibles_dia]
        if preferidos_agua:
            asignacion["Agua"] = seleccionar_puesto(disponibles_dia, historial, "Agua", preferidos_agua)

    for puesto in PUESTOS_HABITUALES:
        if puesto not in asignacion:
            asignacion[puesto] = seleccionar_puesto(disponibles_dia, historial, puesto)
            
    return asignacion

def ejecutar_sistema():
    print("=== SISTEMA AVANZADO DE CRONOGRAMA DE UJIERES ===")
    historial = cargar_historial()
    
    # 1. Control de Inasistencias
    print("\n📋 CONTROL DE ASISTENCIA")
    ausentes_input = input("Ingresa los nombres de ausentes adicionales separados por coma (o Enter si no hay): ").strip()
    
    ausentes_generales = []
    if ausentes_input and ausentes_input.lower() not in ["no", "ninguno", "ninguna", "si", "sí"]:
        ausentes_generales = [nom.strip() for nom in ausentes_input.split(",")]
    
    # 2. Configuración de Viernes y Sábado
    print("\n⚙️ CONFIGURACIÓN DE DÍAS")
    tipo_viernes = input("¿El VIERNES es (1) Servicio Normal o (2) Vigilia?: ").strip()
    
    hay_sabado = input("¿Hay actividad el SÁBADO? (s/n): ").strip().lower() == 's'
    tipo_sabado = "1"
    if hay_sabado:
        tipo_sabado = input("  ↳ ¿El SÁBADO es (1) Servicio Normal / Corto o (2) Evento Especial?: ").strip()

    salida_texto = "=========================================\n"
    salida_texto += "   CRONOGRAMA DE LA SEMANA - UJIERES\n"
    salida_texto += "=========================================\n"

    dias_semana = ["Martes", "Jueves", "Viernes", "Domingo"]
    
    for dia in dias_semana:
        salida_texto += f"\n📌 {dia}\n" + "-"*20 + "\n"
        
        if dia == "Viernes" and tipo_viernes in ["2", "vigilia", "Vigilia"]:
            disp_viernes = obtener_disponibles_dia("Viernes", ausentes_generales)
            salida_texto += "[ EVENTO ESPECIAL / VIGILIA ]\n"
            salida_texto += f"• Turnos asignados para los {len(disp_viernes)} disponibles.\n"
        else:
            res = generar_dia(dia, ausentes_generales, historial)
            for puesto, persona in res.items():
                salida_texto += f"{puesto}: {persona}\n"

    if hay_sabado:
        salida_texto += f"\n📌 Sábado\n" + "-"*20 + "\n"
        if tipo_sabado == "2":
            salida_texto += "[ EVENTO ESPECIAL ]\n"
        else:
            res = generar_dia("Sábado", ausentes_generales, historial)
            salida_texto += f"Puerta: {res['Puerta']}\nAgua: {res['Agua']}\n"

    print("\n" + salida_texto)
    
    # 3. Exportar a Archivo .txt e Historial
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write(salida_texto)
    guardar_historial(historial)
    
    print(f"✅ Cronograma guardado en '{ARCHIVO_SALIDA}'")
    print(f"✅ Historial de rotación actualizado en '{ARCHIVO_HISTORIAL}'")

if __name__ == "__main__":
    ejecutar_sistema()
