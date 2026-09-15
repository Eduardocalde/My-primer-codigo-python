import random
import string

def generar_contraseña(longitud, incluir_mayus, incluir_num, incluir_simb):
    """Crea una contraseña aleatoria según los criterios seleccionados."""
    caracteres = string.ascii_lowercase  # Letras minúsculas siempre incluidas
    
    if incluir_mayus:
        caracteres += string.ascii_uppercase
    if incluir_num:
        caracteres += string.digits
    if incluir_simb:
        caracteres += string.punctuation
        
    # Selección aleatoria de caracteres
    clave = ''.join(random.choice(caracteres) for _ in range(longitud))
    return clave

def ejecutar_generador():
    print("=== GENERADOR DE CONTRASEÑAS SEGURAS (OPEN SOURCE) ===")
    
    try:
        longitud = int(input("\n📏 ¿De cuántos caracteres deseas la contraseña? (Mínimo recomendado: 8): "))
        if longitud < 4:
            print("⚠️ Por seguridad, la longitud mínima debe ser de al menos 4 caracteres.")
            return

        print("\nConfigura las opciones (Responde 's' para sí, 'n' para no):")
        inc_mayus = input("¿Incluir letras MAYÚSCULAS? (s/n): ").strip().lower() == 's'
        inc_num = input("¿Incluir NÚMEROS? (s/n): ").strip().lower() == 's'
        inc_simb = input("¿Incluir SÍMBOLOS (!@#$)? (s/n): ").strip().lower() == 's'

        # Generar clave
        clave_final = generar_contraseña(longitud, inc_mayus, inc_num, inc_simb)
        
        print("\n-------------------------------------------")
        print(f"🔐 Tu contraseña generada es: {clave_final}")
        print("-------------------------------------------")

        # Opción para guardar la clave generada
        guardar = input("\n¿Deseas guardar esta clave en un archivo local? (s/n): ").strip().lower()
        if guardar == 's':
            servicio = input("¿Para qué servicio o cuenta es esta clave? (ej. Correo, Wifi): ").strip()
            with open("claves_guardadas.txt", "a", encoding="utf-8") as archivo:
                archivo.write(f"Servicio: {servicio} | Clave: {clave_final}\n")
            print("✅ ¡Clave guardada en 'claves_guardadas.txt' de forma local!")

    except ValueError:
        print("⚠️ Error: Debes ingresar un número válido para la longitud.")

if __name__ == "__main__":
    ejecutar_generador()
