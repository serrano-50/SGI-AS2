
#EdSerrano
import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk
import datetime

def add_placeholder(entry, placeholder):
    """Add placeholder text to an entry widget."""
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, ctk.END)
            entry.configure(text_color="black")
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(text_color="gray75")
    entry.insert(0, placeholder)
    entry.configure(text_color="gray75")
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

class VerificarAsignacionWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Verificar Asignación de Precios")
        self.geometry("900x400")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self)
        frame_tabla.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Estilo para Treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=80)  # Ajuste para ~4 líneas

        # Treeview con columnas solicitadas, incluyendo Código Producto y Contacto
        self.tree = ttk.Treeview(frame_tabla, columns=("Código", "Cliente", "Contacto", "Observaciones", "Precio"), show="headings", style="Treeview")
        self.tree.heading("Código", text="Código Producto")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Contacto", text="Contacto")
        self.tree.heading("Observaciones", text="Observaciones")
        self.tree.heading("Precio", text="Precio")
        self.tree.column("Código", width=100)
        self.tree.column("Cliente", width=150)
        self.tree.column("Contacto", width=100)
        self.tree.column("Observaciones", width=350)
        self.tree.column("Precio", width=100)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Botón cerrar
        btn_cerrar = ctk.CTkButton(self, text="Cerrar", command=self.destroy)
        btn_cerrar.grid(row=1, column=0, pady=(0, 10), sticky="e", padx=10)

        self.cargar_datos()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def cargar_datos(self):
        """Cargar datos desde la base de datos a la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            with sqlite3.connect('ARTE.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT cod_prod_, cliente_, contacto_, observ_, prec_est_ FROM NUEVOS")
                for cod_prod_, cliente_, contacto_, observ_, prec_est_ in cursor.fetchall():
                    precio_str = f"${prec_est_:.2f}" if prec_est_ is not None else ""
                    self.tree.insert("", "end", values=(cod_prod_, cliente_, contacto_, observ_, precio_str))
        except sqlite3.Error as e:
            messagebox.showerror("Error BD", f"No se pudo cargar la información:\n{e}")

class NuevoProductoWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Nuevo Producto")
        self.geometry("600x650")
        self.resizable(False, False)
        self.verificar_window = None  # Referencia a la ventana de verificación

        # Conexión a base de datos
        self.conn = sqlite3.connect('ARTE.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS NUEVOS 
                              (cod_prod_ TEXT, cliente_ TEXT, contacto_ TEXT, prod_ TEXT, 
                               unidades_ TEXT, observ_ TEXT, tiempo_ TEXT,
                               categoria_ TEXT, material_ TEXT, prec_est_ REAL)''')
        self.conn.commit()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        # Título
        ctk.CTkLabel(self, text="Productos Nuevos", font=("Arial", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 10), sticky="ew"
        )

        # Botón Verificar Asignación de Precios
        btn_verificar = ctk.CTkButton(self, 
            text="Verificar Asignación de Precios",
            width=200,
            fg_color="#05af30",
            hover_color="#057521", 
            command=self.abrir_verificar)
        btn_verificar.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="ew", padx=20)

        # Código Producto
        """ctk.CTkLabel(self, text="Código Producto:").grid(row=2, column=0, padx=20, pady=5, sticky="e")
        self.cod_prod_ = ctk.CTkEntry(self, width=150)
        self.cod_prod_.grid(row=2, column=1, padx=20, pady=5, sticky="w")"""

        # Cliente
        ctk.CTkLabel(self, text="Cliente:").grid(row=3, column=0, padx=20, pady=5, sticky="e")
        self.cliente_ = ctk.CTkEntry(self, width=300)
        self.cliente_.grid(row=3, column=1, padx=20, pady=5, sticky="w")

        # Contacto con validación max 8 caracteres
        vcmd_contacto = (self.register(lambda P: len(P) <= 8), '%P')
        ctk.CTkLabel(self, text="Contacto:").grid(row=4, column=0, padx=20, pady=5, sticky="e")
        self.contacto_ = ctk.CTkEntry(self, width=100, validate="key", validatecommand=vcmd_contacto)
        self.contacto_.grid(row=4, column=1, padx=20, pady=5, sticky="w")

        # Producto
        ctk.CTkLabel(self, text="Producto:").grid(row=5, column=0, padx=20, pady=5, sticky="e")
        self.prod_ = ctk.CTkEntry(self, width=300)
        self.prod_.grid(row=5, column=1, padx=20, pady=5, sticky="w")

        # Cantidad
        ctk.CTkLabel(self, text="Cantidad:").grid(row=6, column=0, padx=20, pady=5, sticky="e")
        self.unidades_ = ctk.CTkEntry(self, width=100)
        self.unidades_.grid(row=6, column=1, padx=20, pady=5, sticky="w")

        # Alto y Ancho en la misma línea
        frame_dimensiones = ctk.CTkFrame(self)
        frame_dimensiones.grid(row=7, column=1, padx=20, pady=5, sticky="w")

        ctk.CTkLabel(self, text="Alto (cm):").grid(row=7, column=0, padx=20, pady=5, sticky="e")
        self.alto_entry = ctk.CTkEntry(frame_dimensiones, width=100)
        self.alto_entry.grid(row=0, column=0, padx=(0, 15), pady=0, sticky="w")

        ctk.CTkLabel(frame_dimensiones, text="Ancho (cm):").grid(row=0, column=1, padx=(0, 5), pady=0, sticky="e")
        self.ancho_entry = ctk.CTkEntry(frame_dimensiones, width=100)
        self.ancho_entry.grid(row=0, column=2, padx=0, pady=0, sticky="w")

        # Observaciones
        ctk.CTkLabel(self, text="Observaciones:").grid(row=8, column=0, padx=20, pady=5, sticky="ne")
        self.observ_ = ctk.CTkTextbox(self, width=300, height=80)
        self.observ_.grid(row=8, column=1, padx=20, pady=5, sticky="w")

        # Fecha solicitada
        ctk.CTkLabel(self, text="Fecha solicitada del cliente:").grid(row=9, column=0, padx=20, pady=5, sticky="e")
        self.tiempo_ = ctk.CTkEntry(self, width=150)
        self.tiempo_.grid(row=9, column=1, padx=20, pady=5, sticky="w")
        add_placeholder(self.tiempo_, "dd-mm-yyyy")

        # Botones
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)

        btn_solicitar = ctk.CTkButton(btn_frame, text="Solicitar Precio", width=140, command=self.save_data)
        btn_solicitar.grid(row=0, column=0, padx=20)

        btn_cerrar = ctk.CTkButton(btn_frame, text="Cerrar", width=140, command=self.on_close)
        btn_cerrar.grid(row=0, column=1, padx=20)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_data(self):
        """Guardar datos del producto en la base de datos."""
        #cod_prod_ = self.cod_prod_.get().strip()
        cliente_ = self.cliente_.get().strip().upper()
        contacto_ = self.contacto_.get().strip()
        prod_ = self.prod_.get().strip()
        unidades_ = self.unidades_.get().strip()
        alto = self.alto_entry.get().strip()
        ancho = self.ancho_entry.get().strip()
        observ_user = self.observ_.get("1.0", "end").strip()
        tiempo_ = self.tiempo_.get().strip()

        # Validaciones
        """if not cod_prod_:
            messagebox.showerror("Error", "El campo 'Código Producto' no puede estar vacío.")
            return"""
        if not prod_:
            messagebox.showerror("Error", "El campo 'Producto' no puede estar vacío.")
            return
        if len(prod_) > 300:
            messagebox.showerror("Error", "El campo 'Producto' debe tener máximo 300 caracteres.")
            return
        if not contacto_:
            messagebox.showerror("Error", "El campo 'Contacto' no puede estar vacío.")
            return
        if not alto or not ancho:
            messagebox.showerror("Error", "Los campos 'Alto' y 'Ancho' no pueden estar vacíos.")
            return
        if tiempo_ != "dd-mm-yyyy":
            try:
                datetime.datetime.strptime(tiempo_, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Error", "La fecha debe tener formato dd-mm-yyyy.")
                return

        # Concatenar observaciones
        observ_ = f"{observ_user}\nMedidas: {alto} x {ancho} cm\nFecha entrega: {tiempo_}"

        # Mostrar detalles
        detalles = (#f"Código Producto: {cod_prod_}\n"
                    f"Cliente: {cliente_}\n"
                    f"Contacto: {contacto_}\n"
                    f"Producto: {prod_.upper()}\n"
                    f"Cantidad: {unidades_}\n"
                    f"Fecha solicitada: {tiempo_}\n"
                    f"Observaciones:\n{observ_}")
        messagebox.showinfo("Detalles del Producto", detalles)

        # Guardar en base de datos
        try:
            self.cursor.execute('''INSERT INTO NUEVOS 
                (cliente_, contacto_, prod_, unidades_, observ_, tiempo_)
                VALUES ( ?, ?, ?, ?, ?, ?)''',
                (cliente_, contacto_, prod_.upper(), unidades_, observ_, tiempo_))
            self.conn.commit()
            # Actualizar la ventana de verificación si está abierta
            if self.verificar_window and self.verificar_window.winfo_exists():
                self.verificar_window.cargar_datos()
        except sqlite3.Error as e:
            messagebox.showerror("Error DB", f"No se puede guardar la información:\n{e}")
            return

        # Limpiar los campos
        #self.cod_prod_.delete(0, ctk.END)
        self.cliente_.delete(0, ctk.END)
        self.contacto_.delete(0, ctk.END)
        self.prod_.delete(0, ctk.END)
        self.unidades_.delete(0, ctk.END)
        self.alto_entry.delete(0, ctk.END)
        self.ancho_entry.delete(0, ctk.END)
        self.observ_.delete("1.0", ctk.END)
        self.tiempo_.delete(0, ctk.END)
        add_placeholder(self.tiempo_, "dd-mm-yyyy")

    def abrir_verificar(self):
        """Abrir o enfocar ventana de verificación."""
        if self.verificar_window is None or not self.verificar_window.winfo_exists():
            self.verificar_window = VerificarAsignacionWindow()
        else:
            self.verificar_window.lift()
            self.verificar_window.focus()

    def on_close(self):
        """Cerrar ventana sin afectar la ventana de verificación."""
        self.conn.close()
        if self.parent:
            self.parent.deiconify()
        self.destroy()

def abrir_productos_nuevos(parent):
    """Abrir ventana de nuevo producto."""
    NuevoProductoWindow(parent)