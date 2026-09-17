import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import os

HOST = '127.0.0.1'
PORT = 5555

CARPETA_DESCARGAS = "descargas"
if not os.path.exists(CARPETA_DESCARGAS):
    os.makedirs(CARPETA_DESCARGAS)

ventana_nombre = tk.Tk()
ventana_nombre.withdraw()
nombre = simpledialog.askstring("SYNTAXIS PRO", "Ingresa tu nombre:")
if not nombre:
    nombre = "Anónimo"

colores_usuarios = {}
paleta_colores = ["#00ffcc", "#ff6b6b", "#feca57", "#48dbfb", "#ff9ff3", "#54a0ff", "#5f27cd", "#01a3a4"]

def obtener_color(nombre_usuario):
    if nombre_usuario not in colores_usuarios:
        indice = len(colores_usuarios) % len(paleta_colores)
        colores_usuarios[nombre_usuario] = paleta_colores[indice]
    return colores_usuarios[nombre_usuario]

ventana = tk.Tk()
ventana.title(f"SYNTAXIS PRO - Chat ({nombre})")
ventana.geometry("600x700")
ventana.configure(bg="#1e1e2e")

area_mensajes = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, state='disabled',
                                          bg="#2a2a3e", fg="#ffffff", font=("Arial", 11))
area_mensajes.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
area_mensajes.tag_config("sistema", foreground="#888888", font=("Arial", 10, "italic"))

marco_inferior = tk.Frame(ventana, bg="#1e1e2e")
marco_inferior.pack(padx=10, pady=5, fill=tk.X)

entrada = tk.Entry(marco_inferior, font=("Arial", 12), bg="#2a2a3e", fg="#ffffff", insertbackground="white")
entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

boton_archivo = tk.Button(marco_inferior, text="📎", font=("Arial", 14),
                          bg="#2a2a3e", fg="#ffffff", command=lambda: enviar_archivo())
boton_archivo.pack(side=tk.RIGHT)

def agregar_mensaje(mensaje, tag=None):
    area_mensajes.config(state='normal')
    if tag:
        area_mensajes.insert(tk.END, mensaje + "\n", tag)
    else:
        area_mensajes.insert(tk.END, mensaje + "\n")
    area_mensajes.config(state='disabled')
    area_mensajes.see(tk.END)

def enviar_mensaje(event=None):
    mensaje = entrada.get()
    if mensaje.strip() == "":
        return
    try:
        cliente.send(mensaje.encode('utf-8'))
        entrada.delete(0, tk.END)
    except:
        messagebox.showerror("Error", "No se pudo enviar el mensaje.")

def enviar_archivo():
    ruta = filedialog.askopenfilename(title="Selecciona un archivo")
    if not ruta:
        return
    try:
        nombre_archivo = os.path.basename(ruta)
        tamano = os.path.getsize(ruta)
        encabezado = f"ARCHIVO|{nombre_archivo}|{tamano}"
        cliente.send(encabezado.encode('utf-8'))
        with open(ruta, "rb") as f:
            while True:
                pedazo = f.read(4096)
                if not pedazo:
                    break
                cliente.send(pedazo)
        agregar_mensaje(f"Tú enviaste un archivo: {nombre_archivo}", "sistema")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el archivo: {e}")

def guardar_archivo(nombre_archivo, datos):
    try:
        ruta = os.path.join(CARPETA_DESCARGAS, nombre_archivo)
        with open(ruta, "wb") as f:
            f.write(datos)
        agregar_mensaje(f"Archivo guardado en descargas: {nombre_archivo}", "sistema")
    except Exception as e:
        agregar_mensaje(f"Error al guardar archivo: {e}", "sistema")

def recibir_mensajes():
    while True:
        try:
            encabezado = cliente.recv(1024).decode('utf-8', errors='ignore')
            if not encabezado:
                break
            
            if encabezado == "NOMBRE":
                cliente.send(nombre.encode('utf-8'))
            
            elif encabezado.startswith("ARCHIVO|"):
                partes = encabezado.split("|")
                nombre_archivo = partes[1]
                tamano = int(partes[2])
                
                datos = b""
                recibido = 0
                while recibido < tamano:
                    pedazo = cliente.recv(min(4096, tamano - recibido))
                    if not pedazo:
                        break
                    datos += pedazo
                    recibido += len(pedazo)
                
                guardar_archivo(nombre_archivo, datos)
            
            elif encabezado.startswith("***"):
                agregar_mensaje(encabezado, "sistema")
            
            elif "envió un archivo" in encabezado:
                agregar_mensaje(encabezado, "sistema")
            
            elif encabezado.startswith("[") and "]" in encabezado:
                try:
                    hora_fin = encabezado.index("]") + 1
                    hora = encabezado[:hora_fin]
                    resto = encabezado[hora_fin:].strip()
                    if ":" in resto:
                        nombre_emisor, texto = resto.split(":", 1)
                        nombre_emisor = nombre_emisor.strip()
                        color = obtener_color(nombre_emisor)
                        if nombre_emisor not in area_mensajes.tag_names():
                            area_mensajes.tag_config(nombre_emisor, foreground=color, font=("Arial", 11, "bold"))
                        area_mensajes.config(state='normal')
                        area_mensajes.insert(tk.END, f"{hora} {nombre_emisor}:", nombre_emisor)
                        area_mensajes.insert(tk.END, f"{texto}\n")
                        area_mensajes.config(state='disabled')
                        area_mensajes.see(tk.END)
                    else:
                        agregar_mensaje(encabezado)
                except:
                    agregar_mensaje(encabezado)
            else:
                agregar_mensaje(encabezado)
        except Exception as e:
            print(f"Error: {e}")
            break

try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))
    agregar_mensaje("*** Conectado al servidor SYNTAXIS PRO ***", "sistema")
    hilo = threading.Thread(target=recibir_mensajes, daemon=True)
    hilo.start()
except:
    messagebox.showerror("Error", "No se pudo conectar al servidor.")
    ventana.destroy()
    exit()

entrada.bind("<Return>", enviar_mensaje)
ventana.mainloop()
