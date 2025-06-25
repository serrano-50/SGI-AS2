#sistema desarrollado por Edwin Serrano & Antonio Mejía
#ANALISIS DE SISEMAS 2 - EUS 2025 - INFORMATICA EDUCATIVA

import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from PIL import Image
import modulo_ventas
import modulo_administracion
import sesion
import os  # <- Importante para rutas dinámicas

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Verifica el rol del usuario desde la base de datos
def verificar_codigo(codigo_usuario):
    conn = sqlite3.connect('ARTE.db')
    cursor = conn.cursor()
    cursor.execute("SELECT carg FROM RRHH WHERE user = ?", (codigo_usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0].lower() if resultado else None

# Abre el módulo correspondiente según el rol
def abrir_modulo_generico(rol):
    if rol == "vendedor":
        root.withdraw()
        entry_codigo.delete(0, 'end')
        modulo_ventas.abrir_ventas(root)
    elif rol == "administrador":
        root.withdraw()
        entry_codigo.delete(0, 'end')
        modulo_administracion.abrir_administracion(root)
    else:
        messagebox.showinfo("Info", f"Rol '{rol}' no implementado aún.")

# Lógica de inicio de sesión
def login():
    codigo_usuario = entry_codigo.get()
    rol = verificar_codigo(codigo_usuario)
    entry_codigo.delete(0, 'end')
    if rol:
        sesion.codigo_usuario = codigo_usuario
        sesion.rol_usuario = rol
        abrir_modulo_generico(rol)
    else:
        messagebox.showerror("Error", "Código de usuario no válido.")

# Cierra la aplicación
def cerrar_sistema():
    root.destroy()

# UI principal
root = ctk.CTk()
root.title("Gestión de Artesanías - Login")
root.geometry("400x450")

# Ruta dinámica para cargar imagen
script_dir = os.path.dirname(os.path.abspath(__file__))  # Carpeta actual del script
imagen_path = os.path.join(script_dir, "assets", "port.png")

# Mostrar imagen del logo
try:
    imagen_logo = ctk.CTkImage(light_image=Image.open(imagen_path), size=(200, 150))
    logo_label = ctk.CTkLabel(root, image=imagen_logo, text="")
    logo_label.pack(pady=(20, 10))
except Exception as e:
    print(f"No se pudo cargar el logo: {e}")
    logo_label = ctk.CTkLabel(root, text="[Logo]", font=("Arial", 24))
    logo_label.pack(pady=(20, 10))

# Campo para ingresar el código de usuario
label_codigo = ctk.CTkLabel(root, text="Ingrese su código de usuario:", font=("Arial", 16))
label_codigo.pack(pady=(10, 5))

entry_codigo = ctk.CTkEntry(root, width=200, justify="center", show="●")
entry_codigo.pack(pady=(0, 10))

# Botón para iniciar sesión
btn_login = ctk.CTkButton(root, text="Ingresar", command=login)
btn_login.pack(pady=10)

# Botón para cerrar sistema
btn_cerrar = ctk.CTkButton(
    root,
    text="Cerrar sistema",
    command=cerrar_sistema,
    fg_color="#CC7722",
    hover_color="#B8641E",
    text_color="white"
)
btn_cerrar.pack(pady=15)

# Ejecutar interfaz
root.mainloop()
