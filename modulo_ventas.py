import customtkinter as ctk
import sesion
import sqlite3
from datetime import datetime
import consultas  # Asegúrate de que consultas.py está en el mismo directorio
import facturar  # Importamos el módulo facturar.py para usarlo en el botón Facturar
from productos_nuevos import NuevoProductoWindow  # Importar ventana nuevo producto

# Estilo coherente
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def abrir_ventas(ventana_login):
    registrar_acceso_en_bd()

    ventana_ventas = ctk.CTkToplevel(ventana_login)
    ventana_ventas.title("Módulo de Ventas")
    ventana_ventas.geometry("400x450")

    # Título
    label_titulo = ctk.CTkLabel(
        ventana_ventas,
        text="VENTAS",
        font=("Arial", 22, "bold")
    )
    label_titulo.pack(pady=(10, 10))

    # Función para abrir módulo de consultas y ocultar esta ventana
    def abrir_consulta_producto():
        ventana_ventas.withdraw()
        consultas.abrir_consultas(ventana_ventas)

    # Botón: Consulta de producto
    btn_consulta = ctk.CTkButton(
        ventana_ventas,
        text="Consulta de producto",
        width=200,
        command=abrir_consulta_producto
    )
    btn_consulta.pack(pady=10)

    # Botón: Facturar
    btn_facturar = ctk.CTkButton(
        ventana_ventas,
        text="Facturar",
        width=200,
        command=lambda: facturar.abrir_facturacion(ventana_ventas)
    )
    btn_facturar.pack(pady=10)

    # Función para abrir ventana productos nuevos
    def abrir_producto_nuevo():
        ventana_ventas.withdraw()
        NuevoProductoWindow(ventana_ventas)

    # Botón: Pedido (ahora abre ventana productos nuevos)
    btn_pedido = ctk.CTkButton(
        ventana_ventas,
        text="Solicitar producto nuevo",
        width=200,
        command=abrir_producto_nuevo,
        fg_color="#05af30",
        hover_color="#057521",
    )
    btn_pedido.pack(pady=10)

    # Separador visual
    ctk.CTkLabel(ventana_ventas, text="").pack(pady=5)

    # Botón: Cerrar sesión
    btn_logout = ctk.CTkButton(
        ventana_ventas,
        text="Cerrar sesión",
        width=200,
        fg_color="gray",
        hover_color="darkgray",
        command=lambda: cerrar_sesion(ventana_ventas, ventana_login)
    )
    btn_logout.pack(pady=20)

def cerrar_sesion(ventana_ventas, ventana_login):
    ventana_ventas.destroy()
    ventana_login.deiconify()

def registrar_acceso_en_bd():
    try:
        conn = sqlite3.connect('ARTE.db')
        cursor = conn.cursor()
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO CONSULT (User, rol, f_cons) VALUES (?, ?, ?)",
            (sesion.codigo_usuario, sesion.rol_usuario, fecha_hora)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] No se pudo registrar acceso en CONSULT: {e}")
