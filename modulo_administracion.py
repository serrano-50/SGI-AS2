import customtkinter as ctk
import sqlite3
from tkinter import ttk
from tkinter import messagebox

def abrir_administracion(root):
    """Open the administration window for managing price requests."""
    SolicitudesPreciosWindow(master=root)

class SolicitudesPreciosWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Administración - Solicitudes de precios")
        self.geometry("800x600")

        # Configurar grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Bloque solicitudes de precios
        bloque_izq_inf = ctk.CTkFrame(self, fg_color="#9dafb9")
        bloque_izq_inf.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        bloque_izq_inf.grid_rowconfigure(1, weight=1)
        bloque_izq_inf.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            bloque_izq_inf,
            text="Solicitudes de precios",
            font=ctk.CTkFont(size=20),
        ).grid(row=0, column=0, padx=10, pady=10)

        # Frame para la tabla solicitudes
        table_frame_sol = ctk.CTkFrame(bloque_izq_inf)
        table_frame_sol.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Estilo para aumentar altura fila
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        self.tree_sol = ttk.Treeview(
            table_frame_sol,
            columns=("Cliente", "Contacto", "Producto", "Unidades", "Tiempo"),
            show="headings",
        )
        self.tree_sol.heading("Cliente", text="Cliente")
        self.tree_sol.heading("Contacto", text="Contacto")
        self.tree_sol.heading("Producto", text="Producto")
        self.tree_sol.heading("Unidades", text="Unidades")
        self.tree_sol.heading("Tiempo", text="Tiempo")

        scrollbar_sol = ttk.Scrollbar(table_frame_sol, orient="vertical", command=self.tree_sol.yview)
        self.tree_sol.configure(yscrollcommand=scrollbar_sol.set)
        scrollbar_sol.pack(side="right", fill="y")
        self.tree_sol.pack(fill="both", expand=True)

        # Frame para detalles y edición
        self.detail_frame = ctk.CTkFrame(bloque_izq_inf, fg_color="#b0c4de")
        self.detail_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.detail_frame.grid_columnconfigure(1, weight=1)
        self.detail_frame.grid_columnconfigure(3, weight=1)

        # Label para observaciones
        self.label_observaciones = ctk.CTkLabel(
            self.detail_frame, text="Observaciones: ", wraplength=400, justify="left"
        )
        self.label_observaciones.grid(row=0, column=0, columnspan=4, sticky="w", padx=5, pady=5)

        # Entry fields
        ctk.CTkLabel(self.detail_frame, text="Código Producto:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.entry_cod_prod = ctk.CTkEntry(self.detail_frame)
        self.entry_cod_prod.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(self.detail_frame, text="Materiales:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.entry_materiales = ctk.CTkEntry(self.detail_frame)
        self.entry_materiales.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(self.detail_frame, text="Categoría:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
        self.entry_categoria = ctk.CTkEntry(self.detail_frame)
        self.entry_categoria.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(self.detail_frame, text="Precio:").grid(row=2, column=2, sticky="e", padx=5, pady=2)
        self.entry_precio = ctk.CTkEntry(self.detail_frame, font=ctk.CTkFont(size=18))
        self.entry_precio.grid(row=2, column=3, sticky="ew", padx=5, pady=2)

        # Botón para asignar datos
        self.btn_asignar = ctk.CTkButton(self.detail_frame, text="ASIGNAR", command=self.asignar_datos)
        self.btn_asignar.grid(row=3, column=0, columnspan=4, pady=10)

        # Botón cerrar
        self.btn_cerrar = ctk.CTkButton(self, text="Cerrar", command=self.cerrar_ventana)
        self.btn_cerrar.grid(row=3, column=0, pady=10)

        # Bind doble clic
        self.tree_sol.bind("<Double-1>", self.on_sol_double_click)

        # Variable para item seleccionado
        self.selected_item_id = None

        # Cargar datos iniciales
        self.cargar_solicitudes()

    def cargar_solicitudes(self):
        """Load price requests from the database."""
        for item in self.tree_sol.get_children():
            self.tree_sol.delete(item)
        try:
            conn = sqlite3.connect("ARTE.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Cliente_, Contacto_, Prod_, Unidades_, tiempo_, Observ_ FROM NUEVOS")
            rows = cursor.fetchall()
            for row in rows:
                cliente_, contacto_, prod_, unidades_, tiempo_, observ_ = row
                self.tree_sol.insert(
                    "",
                    "end",
                    values=(cliente_, contacto_, prod_, unidades_, tiempo_),
                    tags=(observ_,),
                )
            # Ajustar ancho columnas
            for col in ("Cliente", "Contacto", "Producto", "Unidades", "Tiempo"):
                self.tree_sol.column(col, width=100, stretch=True)
                max_width = max(
                    [len(str(self.tree_sol.set(item, col))) for item in self.tree_sol.get_children()] + [len(col)]
                )
                self.tree_sol.column(col, width=max_width * 8)
            conn.close()
        except sqlite3.Error as e:
            self.tree_sol.insert("", "end", values=("Error", "No se pudo cargar", str(e), "", ""))

    def on_sol_double_click(self, event):
        """Handle double-click on a table row."""
        selected = self.tree_sol.selection()
        if not selected:
            return
        item_id = selected[0]
        item = self.tree_sol.item(item_id)
        values = item["values"]
        if len(values) < 5:
            return

        tags = item.get("tags", ())
        observaciones = tags[0] if tags else ""

        self.label_observaciones.configure(text=f"Observaciones: {observaciones}")
        self.entry_cod_prod.delete(0, ctk.END)
        self.entry_categoria.delete(0, ctk.END)
        self.entry_materiales.delete(0, ctk.END)
        self.entry_precio.delete(0, ctk.END)
        self.selected_item_id = item_id

    def asignar_datos(self):
        """Assign product code, category, materials, and price to the selected request and update both tables."""
        if not self.selected_item_id:
            messagebox.showwarning("Advertencia", "Seleccione un registro de solicitudes con doble clic primero.")
            return

        cod_prod = self.entry_cod_prod.get().strip().upper()
        categoria = self.entry_categoria.get().strip()
        materiales = self.entry_materiales.get().strip()
        precio = self.entry_precio.get().strip()

        if not cod_prod or not categoria or not materiales or not precio:
            messagebox.showwarning(
                "Advertencia", "Por favor, complete todos los campos: Código Producto, Categoría, Materiales y Precio."
            )
            return

        try:
            precio_val = float(precio)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        item = self.tree_sol.item(self.selected_item_id)
        valores = item["values"]
        tags = item.get("tags", ())
        observ_ = tags[0] if tags else ""

        if len(valores) < 5:
            messagebox.showerror("Error", "Registro seleccionado inválido.")
            return

        cliente_, contacto_, prod_, unidades_, tiempo_ = valores

        try:
            conn = sqlite3.connect("ARTE.db")
            cursor = conn.cursor()

            # Begin transaction
            conn.execute("BEGIN TRANSACTION")

            # Update NUEVOS table
            cursor.execute(
                """
                UPDATE NUEVOS
                SET cod_prod_ = ?, categoria_ = ?, material_ = ?, prec_est_ = ?
                WHERE Cliente_ = ? AND Contacto_ = ? AND Prod_ = ? AND Unidades_ = ? AND Observ_ = ? AND tiempo_ = ?
                """,
                (cod_prod, categoria, materiales, precio_val, cliente_, contacto_, prod_, unidades_, observ_, tiempo_),
            )

            # Insert into PRODUCT table with specified mappings
            # Insert into PRODUCT table con EXIST = unidades_
            cursor.execute(
                """
                INSERT INTO PRODUCT (ID_cat, N_prod, Describe, PrecioV, Categ, Mater, EXIST)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (cod_prod, prod_, observ_, precio_val, categoria, materiales, unidades_),
            )


            # Commit transaction
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Datos asignados correctamente en ambas tablas.")
            self.entry_cod_prod.delete(0, ctk.END)
            self.entry_categoria.delete(0, ctk.END)
            self.entry_materiales.delete(0, ctk.END)
            self.entry_precio.delete(0, ctk.END)
            self.label_observaciones.configure(text="Observaciones: ")
            self.selected_item_id = None
            self.cargar_solicitudes()  # Refresh table

        except sqlite3.Error as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Error de base de datos", f"No se pudo actualizar los registros:\n{e}")

    def cerrar_ventana(self):
        """Close the window and show the parent window."""
        if self.master is not None:
            self.master.deiconify()
        self.destroy()