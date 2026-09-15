import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def convertir_almacenamiento(valor, unidad_origen, unidad_destino):
    # Factores de conversión basados en el sistema binario (1024)
    unidades = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    
    u_origen = unidad_origen.upper()
    u_destino = unidad_destino.upper()
    
    if u_origen not in unidades or u_destino not in unidades:
        return None
    
    # Convertir primero a Bytes y luego a la unidad destino
    bytes_totales = valor * unidades[u_origen]
    resultado = bytes_totales / unidades[u_destino]
    return resultado

def mostrar_menu():
    limpiar_pantalla()
    print("=" * 45)
    print("   CONVERSOR DE UNIDADES DE ALMACENAMIENTO   ")
    print("=" * 45)
    print(" Unidades soportadas: B, KB, MB, GB, TB")
    print("-" * 45)

def ejecutar_conversor():
    while True:
        mostrar_menu()
        
        try:
            cantidad = float(input("\nIngrese la cantidad a convertir: "))
            origen = input("Unidad de origen (B, KB, MB, GB, TB): ").strip()
            destino = input("Unidad de destino (B, KB, MB, GB, TB): ").strip()
            
            resultado = convertir_almacenamiento(cantidad, origen, destino)
            
            if resultado is not None:
                print("\n" + "=" * 45)
                print(f" RESULTADO: {cantidad} {origen.upper()} = {resultado:,.4f} {destino.upper()}")
                print("=" * 45)
            else:
                print("\n Error: Una de las unidades ingresadas no es válida.")
                
        except ValueError:
            print("\n Error: Por favor, ingrese un número válido.")
        
        opcion = input("\n¿Desea realizar otra conversión? (s/n): ").lower()
        if opcion != 's':
            print("\n¡Gracias por usar el conversor! Hasta luego.\n")
            break

if __name__ == "__main__":
    ejecutar_conversor()
