import socket
import threading
import os
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5555
CARPETA_ARCHIVOS = "archivos_recibidos"

if not os.path.exists(CARPETA_ARCHIVOS):
    os.makedirs(CARPETA_ARCHIVOS)

clientes = {}

def hora_actual():
    return datetime.now().strftime("%H:%M")

def manejar_cliente(conexion, direccion):
    print(f"[NUEVA CONEXIÓN] {direccion} se ha conectado.")
    
    conexion.send("NOMBRE".encode('utf-8'))
    nombre = conexion.recv(1024).decode('utf-8').strip()
    if not nombre:
        nombre = str(direccion)
    
    clientes[conexion] = nombre
    print(f"[NOMBRE] {nombre} ({direccion})")
    
    broadcast(f"*** {nombre} se ha unido al chat ***".encode('utf-8'), conexion)
    
    while True:
        try:
            encabezado = conexion.recv(1024).decode('utf-8', errors='ignore')
            if not encabezado:
                break
            
            # Si es un archivo
            if encabezado.startswith("ARCHIVO|"):
                partes = encabezado.split("|")
                nombre_archivo = partes[1]
                tamano = int(partes[2])
                
                # Recibir archivo en pedazos
                datos = b""
                recibido = 0
                while recibido < tamano:
                    pedazo = conexion.recv(min(4096, tamano - recibido))
                    if not pedazo:
                        break
                    datos += pedazo
                    recibido += len(pedazo)
                
                # Guardar archivo en el servidor
                ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo)
                with open(ruta, "wb") as f:
                    f.write(datos)
                
                hora = hora_actual()
                print(f"[{hora}] [{nombre}] envió archivo: {nombre_archivo}")
                
                # Notificar a los demás
                notificacion = f"[{hora}] {nombre} envió un archivo: {nombre_archivo}".encode('utf-8')
                for cliente in list(clientes.keys()):
                    if cliente != conexion:
                        try:
                            cliente.send(notificacion)
                            # Reenviar el archivo a los demás
                            cliente.send(f"ARCHIVO|{nombre_archivo}|{tamano}".encode('utf-8'))
                            cliente.send(datos)
                        except:
                            pass
            
            # Si es texto
            else:
                texto = encabezado
                hora = hora_actual()
                print(f"[{hora}] [{nombre}] {texto}")
                broadcast(f"[{hora}] {nombre}: {texto}".encode('utf-8'), conexion)
        
        except:
            break
    
    print(f"[DESCONEXIÓN] {nombre} ({direccion}) se ha desconectado.")
    if conexion in clientes:
        del clientes[conexion]
    conexion.close()
    broadcast(f"*** {nombre} ha salido del chat ***".encode('utf-8'), conexion)

def broadcast(mensaje, conexion_emisor):
    for cliente in list(clientes.keys()):
        if cliente != conexion_emisor:
            try:
                cliente.send(mensaje)
            except:
                pass

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()
    
    print("=" * 50)
    print("   SERVIDOR DE MENSAJERÍA - SYNTAXIS PRO")
    print("=" * 50)
    print(f"[ESCUCHANDO] Puerto {PORT}...")
    print("[ESPERANDO] Conexiones de clientes...")
    print("=" * 50)
    
    while True:
        conexion, direccion = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
