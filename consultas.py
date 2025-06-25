import customtkinter as ctk
import sqlite3
try:
    from facturar import abrir_facturacion
    from productos_nuevos import abrir_productos_nuevos
except ImportError as e:
    print(f"Error importing modules: {e}")
    raise

# Configuración visual
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def abrir_consultas(parent_window):
    """Open the product consultation window."""
    ventana_consulta = ctk.CTkToplevel(parent_window)
    ventana_consulta.title("Consulta de Producto")
    ventana_consulta.geometry("420x400")
    ventana_consulta.resizable(False, False)
    
    # Ensure parent window is re-enabled when consultation window closes
    ventana_consulta.protocol("WM_DELETE_WINDOW", 
                           lambda: cerrar_consulta(ventana_consulta, parent_window))

    # Title
    label_titulo = ctk.CTkLabel(
        ventana_consulta,
        text="CONSULTA DE PRODUCTO",
        font=("Arial", 20, "bold")
    )
    label_titulo.pack(pady=(20, 10))

    # Search label
    label_buscar = ctk.CTkLabel(
        ventana_consulta,
        text="BUSCAR POR CÓDIGO DE CATÁLOGO",
        font=("Arial", 14)
    )
    label_buscar.pack(pady=(5, 2))

    # Product code entry
    entry_codigo = ctk.CTkEntry(
        ventana_consulta,
        placeholder_text="Ingrese ID del producto",
        width=250,
        justify="center"
    )
    entry_codigo.pack(pady=(2, 10))

    # Result display
    label_resultado = ctk.CTkLabel(
        ventana_consulta,
        text="",
        font=("Arial", 16),
        wraplength=380
    )
    label_resultado.pack(pady=(10, 10))

    def buscar_producto():
        """Search for product by catalog code."""
        codigo = entry_codigo.get().strip().upper()
        if not codigo:
            label_resultado.configure(text="Por favor, ingrese un código válido.")
            return

        try:
            with sqlite3.connect("ARTE.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT SUM(EXIST) FROM PRODUCT WHERE ID_cat = ?", (codigo,))
                resultado = cursor.fetchone()
                
            cantidad = resultado[0]
            if cantidad is None or cantidad == 0:
                label_resultado.configure(text="PRODUCTO AGOTADO O NO FABRICADO")
            else:
                label_resultado.configure(text=f"Existencias: {cantidad}")

        except sqlite3.Error as e:
            label_resultado.configure(text=f"Error en la base de datos: {e}")
        except Exception as e:
            label_resultado.configure(text=f"Error inesperado: {e}")

    # Search button
    btn_buscar = ctk.CTkButton(
        ventana_consulta,
        text="Buscar producto",
        command=buscar_producto
    )
    btn_buscar.pack(pady=(5, 10))

    # Invoice button
    btn_facturar = ctk.CTkButton(
        ventana_consulta,
        text="Facturar producto",
        command=lambda: (ventana_consulta.destroy(), abrir_facturacion(parent_window))
    )
    btn_facturar.pack(pady=10)

    # New product request button
    def abrir_productos_nuevos_desde_consulta():
        """Open new products window and hide current window."""
        ventana_consulta.withdraw()
        abrir_productos_nuevos(ventana_consulta)

    btn_ingresar = ctk.CTkButton(
        ventana_consulta,
        text="Solicitar producto nuevo",
        command=abrir_productos_nuevos_desde_consulta,
        fg_color="#05af30",
        hover_color="#057521",
    )
    btn_ingresar.pack(pady=10)

    # Close button
    btn_cerrar = ctk.CTkButton(
        ventana_consulta,
        text="Cerrar ventana",
        fg_color="gray",
        hover_color="darkgray",
        command=lambda: cerrar_consulta(ventana_consulta, parent_window)
    )
    btn_cerrar.pack(pady=20)

def cerrar_consulta(ventana_consulta, ventana_anterior):
    """Close consultation window and restore parent window."""
    ventana_consulta.destroy()
    ventana_anterior.deiconify()