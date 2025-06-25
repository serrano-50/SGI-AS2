import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def abrir_facturacion(parent_window):
    parent_window.withdraw()

    ventana = ctk.CTkToplevel(parent_window)
    ventana.title("Facturación")
    ventana.geometry("900x600")
    ventana.minsize(800, 600)

    def al_cerrar():
        ventana.destroy()
        parent_window.deiconify()

    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

    # --- Encabezado ---
    frame_header = ctk.CTkFrame(ventana, fg_color="white")
    frame_header.grid(row=0, column=0, columnspan=7, sticky="ew", padx=10, pady=10)
    frame_header.columnconfigure(3, weight=1)

    # Logo 50x50
    try:
        img = Image.open("C:/py_cod/SIST2/SGI/lo_fact.png").resize((50, 50))
        logo_img = ImageTk.PhotoImage(img)
        label_logo = ctk.CTkLabel(frame_header, image=logo_img, text="", fg_color="white")
        label_logo.image = logo_img
    except Exception:
        label_logo = ctk.CTkLabel(frame_header, text="LOGO", fg_color="white", width=50, height=50)
    label_logo.grid(row=0, column=0, sticky="w")

    # Texto FACTURA
    label_factura = ctk.CTkLabel(frame_header, text="FACTURA", font=("Arial", 24, "bold"), fg_color="white")
    label_factura.grid(row=0, column=1, padx=10, sticky="w")

    # Monto (valor grande y color distinto)
    label_monto = ctk.CTkLabel(frame_header, text="TOTAL: $0.00", font=("Arial", 28, "bold"), text_color="#007ACC", fg_color="white")
    label_monto.grid(row=0, column=2, padx=10, sticky="w")

    # --- Datos Cliente y Vendedor ---
    frame_cliente = ctk.CTkFrame(ventana)
    frame_cliente.grid(row=1, column=0, columnspan=7, sticky="ew", padx=10, pady=10)
    frame_cliente.columnconfigure(7, weight=1)

    label_nombre = ctk.CTkLabel(frame_cliente, text="Nombre Cliente:", font=("Arial", 14))
    label_nombre.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_nombre = ctk.CTkEntry(frame_cliente, width=220)
    entry_nombre.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    def nombre_mayus(event=None):
        texto = entry_nombre.get()
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, texto.upper())
    entry_nombre.bind("<KeyRelease>", nombre_mayus)

    label_telefono = ctk.CTkLabel(frame_cliente, text="Teléfono:", font=("Arial", 14))
    label_telefono.grid(row=0, column=2, sticky="e", padx=5, pady=5)
    entry_telefono = ctk.CTkEntry(frame_cliente, width=180)
    entry_telefono.grid(row=0, column=3, sticky="w", padx=5, pady=5)
    def telefono_limite(event=None):
        texto = entry_telefono.get()
        texto = ''.join(filter(str.isdigit, texto))[:8]
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, texto)
    entry_telefono.bind("<KeyRelease>", telefono_limite)

    label_vendedor = ctk.CTkLabel(frame_cliente, text="Vendedor:", font=("Arial", 14))
    label_vendedor.grid(row=0, column=4, sticky="e", padx=5, pady=5)
    def cargar_vendedores():
        try:
            conn = sqlite3.connect("ARTE.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT NOMB FROM RRHH WHERE CARG = 'Vendedor'")
            vendedores = [row[0] for row in cursor.fetchall()]
            conn.close()
            return vendedores
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los vendedores:\n{e}")
            return []
    vendedores_list = cargar_vendedores()
    combo_vendedores = ctk.CTkComboBox(frame_cliente, values=vendedores_list, width=180)
    combo_vendedores.grid(row=0, column=5, sticky="w", padx=5, pady=5)
    combo_vendedores.set("")  # Sin selección inicial

    # --- Detalles Producto y acciones ---
    frame_producto = ctk.CTkFrame(ventana)
    frame_producto.grid(row=2, column=0, columnspan=7, sticky="ew", padx=10, pady=10)
    frame_producto.columnconfigure(7, weight=1)

    label_codigo = ctk.CTkLabel(frame_producto, text="Código Producto:", font=("Arial", 14))
    label_codigo.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_codigo = ctk.CTkEntry(frame_producto, width=120)
    entry_codigo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    def codigo_mayus(event=None):
        texto = entry_codigo.get().upper()
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, texto)
    entry_codigo.bind("<KeyRelease>", codigo_mayus)

    btn_encontrar = ctk.CTkButton(frame_producto, text="ENCONTRAR")
    btn_encontrar.grid(row=0, column=2, sticky="w", padx=5, pady=5)

    label_cantidad = ctk.CTkLabel(frame_producto, text="Cantidad:", font=("Arial", 14))
    label_cantidad.grid(row=0, column=3, sticky="e", padx=5, pady=5)
    entry_cantidad = ctk.CTkEntry(frame_producto, width=80)
    entry_cantidad.grid(row=0, column=4, sticky="w", padx=5, pady=5)

    btn_agregar = ctk.CTkButton(frame_producto, text="AGREGAR")
    btn_agregar.grid(row=0, column=5, sticky="w", padx=5, pady=5)
    btn_eliminar = ctk.CTkButton(frame_producto, text="ELIMINAR")
    btn_eliminar.grid(row=0, column=6, sticky="w", padx=5, pady=5)

    label_detalles = ctk.CTkLabel(frame_producto, text="", font=("Arial", 16))
    label_detalles.grid(row=1, column=0, columnspan=7, sticky="w", padx=5, pady=5)

    # --- Tabla productos agregados con scroll ---
    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.grid(row=3, column=0, columnspan=7, sticky="nsew", padx=10, pady=10)
    ventana.grid_rowconfigure(3, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    columnas = ("Cantidad", "Código", "Nombre", "Categoría", "Material", "Precio", "Valor")
    treeview = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
    treeview.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=treeview.yview)
    scrollbar.pack(side="right", fill="y")
    treeview.configure(yscrollcommand=scrollbar.set)

    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center")

    # --- Funciones ---
    def buscar_producto():
        codigo = entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Ingrese un código de producto.")
            return
        try:
            conn = sqlite3.connect("ARTE.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Categ, N_prod, Mater, PrecioV, Exist FROM PRODUCT WHERE ID_cat = ?", (codigo,))
            res = cursor.fetchone()
            conn.close()
            if res:
                categ, nprod, mater, precio, exist = res
                detalles_text = f"{nprod} |   {categ} |   {mater} |     Precio: ${precio:.2f} | En Stock: {exist}"
                label_detalles.configure(text=detalles_text,font=("Arial", 22))
                ventana.producto_actual = {
                    "codigo": codigo,
                    "categ": categ,
                    "nombre": nprod,
                    "material": mater,
                    "precio": precio,
                    "exist": exist
                }
            else:
                messagebox.showinfo("No encontrado", "Producto no encontrado.")
                label_detalles.configure(text="")
                ventana.producto_actual = None
        except Exception as e:
            messagebox.showerror("Error", f"Error consultando producto:\n{e}")
            ventana.producto_actual = None

    btn_encontrar.configure(command=buscar_producto)

    def agregar_producto():
        if not hasattr(ventana, "producto_actual") or ventana.producto_actual is None:
            messagebox.showwarning("Atención", "Busque un producto válido antes de agregar.")
            return
        cantidad_text = entry_cantidad.get().strip()
        if not cantidad_text.isdigit() or int(cantidad_text) <= 0:
            messagebox.showwarning("Atención", "Ingrese una cantidad válida mayor que cero.")
            return
        cantidad = int(cantidad_text)
        prod = ventana.producto_actual
        valor = cantidad * prod["precio"]
        treeview.insert("", "end", values=(
            cantidad,
            prod["codigo"],
            prod["nombre"],
            prod["categ"],
            prod["material"],
            f"${prod['precio']:.2f}",
            f"${valor:.2f}"
        ))
        actualizar_monto_total()
        entry_codigo.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        label_detalles.configure(text="")
        ventana.producto_actual = None

    btn_agregar.configure(command=agregar_producto)

    def eliminar_producto():
        selected = treeview.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return
        for sel in selected:
            treeview.delete(sel)
        actualizar_monto_total()

    btn_eliminar.configure(command=eliminar_producto)

    def actualizar_monto_total():
        total = 0.0
        for child in treeview.get_children():
            valor_str = treeview.item(child)["values"][6]  # Valor en formato $xx.xx
            valor = float(valor_str.replace("$", ""))
            total += valor
        label_monto.configure(text=f"TOTAL: ${total:,.2f}")

    # --- VALIDAR Y GENERAR TICKET ---
    def ticket_y_validar():
        nombre_cliente = entry_nombre.get().strip()
        telefono_cliente = entry_telefono.get().strip()
        vendedor = combo_vendedores.get().strip()
        productos = [treeview.item(child)["values"] for child in treeview.get_children()]
        total_text = label_monto.cget("text")
        monto = float(total_text.replace("TOTAL: $", "").replace(",", ""))

        # Validaciones estrictas
        if not nombre_cliente:
            messagebox.showwarning("Atención", "Ingrese el nombre del cliente.")
            return
        if not telefono_cliente or not telefono_cliente.isdigit() or len(telefono_cliente) < 8:
            messagebox.showwarning("Atención", "Ingrese un teléfono válido de 8 dígitos.")
            return
        if not vendedor:
            messagebox.showwarning("Atención", "Seleccione un vendedor.")
            return
        if not productos:
            messagebox.showwarning("Atención", "No hay productos agregados.")
            return

        try:
            conn = sqlite3.connect("ARTE.db")
            cursor = conn.cursor()
            for values in productos:
                codigo = values[1]
                cantidad = int(values[0])
                cursor.execute("SELECT Exist FROM PRODUCT WHERE ID_cat = ?", (codigo,))
                exist_actual = cursor.fetchone()
                if exist_actual is None:
                    messagebox.showerror("Error", f"Producto {codigo} no encontrado en base de datos.")
                    conn.close()
                    return
                exist_actual = int(exist_actual[0])
                nuevo_exist = exist_actual - cantidad
                if nuevo_exist < 0:
                    messagebox.showwarning("Advertencia", f"Stock insuficiente para producto {codigo}. Existencia actual: {exist_actual}")
                    conn.close()
                    return
                cursor.execute("UPDATE PRODUCT SET Exist = ? WHERE ID_cat = ?", (nuevo_exist, codigo))
            # Obtener número de factura
            cursor.execute("SELECT MAX(FACT) FROM CLIENTE")
            max_fact = cursor.fetchone()[0]
            factura_num = (max_fact or 0) + 1
            # Guardar venta en CLIENTE (nombre, contacto, vendedor, monto, prod)
            descripcion = "; ".join([f"{p[0]} x {p[2]} (Código: {p[1]})" for p in productos])
            cursor.execute("INSERT INTO CLIENTE (NOMBRE, contacto, vendedor, monto, prod) VALUES (?, ?, ?, ?, ?)",
                          (nombre_cliente, telefono_cliente, vendedor, monto, descripcion))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron actualizar las existencias o registrar la venta:\n{e}")
            return

        # Ocultar la ventana de facturación
        ventana.withdraw()

        # --- Ventana media carta con scroll ---
        carta_win = ctk.CTkToplevel(ventana)
        carta_win.title("Ticket de Compra")
        carta_win.geometry("900x480")
        carta_win.minsize(900, 410)
        carta_win.resizable(False, False)

        # Frame para scroll
        frame_scroll = ctk.CTkFrame(carta_win)
        frame_scroll.pack(fill="both", expand=True, padx=10, pady=(10,0))

        # Canvas y Scrollbar
        canvas_widget = tk.Canvas(frame_scroll, borderwidth=0, background="#f8f8f8")
        frame_in_canvas = ctk.CTkFrame(canvas_widget, fg_color="#f8f8f8")
        vscroll = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas_widget.yview)
        canvas_widget.configure(yscrollcommand=vscroll.set)

        vscroll.pack(side="right", fill="y")
        canvas_widget.pack(side="left", fill="both", expand=True)
        canvas_widget.create_window((0,0), window=frame_in_canvas, anchor="nw")

        def on_frame_configure(event):
            canvas_widget.configure(scrollregion=canvas_widget.bbox("all"))
        frame_in_canvas.bind("<Configure>", on_frame_configure)

        # --- Contenido del ticket en tabla ---
        col_headers = ["Cant", "Código", "Nombre", "Categoría", "Material", "Precio", "Valor"]
        col_widths = [6, 10, 32, 12, 12, 10, 10]
        def wrap_text(text, width):
            lines = []
            while len(text) > width:
                split_pos = text.rfind(" ", 0, width)
                if split_pos == -1:
                    split_pos = width
                lines.append(text[:split_pos])
                text = text[split_pos:].lstrip()
            lines.append(text)
            return lines

        text_ticket = tk.Text(frame_in_canvas, font=("Consolas", 11), wrap="none", height=18, width=110, background="#f8f8f8", borderwidth=0)
        text_ticket.pack(fill="both", expand=True)
        detalle = f"FACTURA N°: {factura_num}\n\nCliente: {nombre_cliente}\nTeléfono: {telefono_cliente}\nVendedor: {vendedor}\n\n"
        header_line = "".join([h.ljust(w) for h, w in zip(col_headers, col_widths)])
        detalle += header_line + "\n"
        detalle += "-" * (sum(col_widths)+2) + "\n"
        for p in productos:
            nombre_lines = wrap_text(str(p[2]), col_widths[2])
            first_line = True
            for line in nombre_lines:
                if first_line:
                    row = [
                        str(p[0]).ljust(col_widths[0]),
                        str(p[1]).ljust(col_widths[1]),
                        line.ljust(col_widths[2]),
                        str(p[3]).ljust(col_widths[3]),
                        str(p[4]).ljust(col_widths[4]),
                        str(p[5]).ljust(col_widths[5]),
                        str(p[6]).ljust(col_widths[6]),
                    ]
                    detalle += "".join(row) + "\n"
                    first_line = False
                else:
                    detalle += " " * (col_widths[0] + col_widths[1]) + line.ljust(col_widths[2]) + "\n"
        detalle += "\n" + total_text

        text_ticket.insert("1.0", detalle)
        text_ticket.config(state="disabled")

        # --- FUNCIONES BOTONES PDF Y CERRAR ---
        def guardar_como_pdf():
            archivo = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf")],
                title="Guardar ticket como PDF"
            )
            if not archivo:
                return
            try:
                c = canvas.Canvas(archivo, pagesize=letter)
                width, height = letter
                y = height - 40
                for line in detalle.split('\n'):
                    c.drawString(40, y, line)
                    y -= 15
                    if y < 40:
                        c.showPage()
                        y = height - 40
                c.save()
                messagebox.showinfo("Éxito", "Ticket guardado como PDF correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el PDF:\n{e}")

        def cerrar_ticket():
            carta_win.destroy()
            ventana.deiconify()

        # --- BOTONES PDF Y CERRAR ---
        frame_botones_ticket = ctk.CTkFrame(frame_in_canvas, fg_color="#f8f8f8")
        frame_botones_ticket.pack(fill="x", pady=10)
        btn_pdf = ctk.CTkButton(frame_botones_ticket, text="GUARDAR COMO PDF", command=guardar_como_pdf)
        btn_pdf.pack(side="left", padx=10)
        btn_cerrar = ctk.CTkButton(frame_botones_ticket, text="CERRAR", fg_color="#888", hover_color="#555", command=cerrar_ticket)
        btn_cerrar.pack(side="right", padx=10)

    # --- Botones validar y cerrar ---
    frame_botones = ctk.CTkFrame(ventana)
    frame_botones.grid(row=4, column=0, columnspan=7, pady=15)

    btn_validar = ctk.CTkButton(frame_botones, text="VALIDAR Y GENERAR TICKET", command=ticket_y_validar)
    btn_validar.pack(side="left", padx=20)

    btn_cerrar = ctk.CTkButton(frame_botones, text="CERRAR", fg_color="#888", hover_color="#555", command=al_cerrar)
    btn_cerrar.pack(side="right", padx=20)

# Ejemplo de uso:
# root = ctk.CTk()
# abrir_facturacion(root)
# root.mainloop()
