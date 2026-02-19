import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime

class GestorFinanzasPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Saldos y Movimientos Pro - Export Edition")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f4f7f6")

        # --- Base de Datos ---
        self.db_name = 'control_gastos.db'
        self.inicializar_bd()

        # --- Configuración de Estilos ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#ffffff", foreground="#333333", rowheight=30, fieldbackground="#ffffff", font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", background="#dcdde1", foreground="#2f3640", font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview", background=[('selected', '#3498db')])

        # --- 1. ENCABEZADO (SALDO ACTUAL) ---
        self.header = tk.Frame(self.root, bg="#2f3640", height=150)
        self.header.pack(fill="x", side="top")
        
        tk.Label(self.header, text="DISPONIBLE ACTUAL", font=("Segoe UI", 12), fg="#dcdde1", bg="#2f3640").pack(pady=(20, 0))
        self.label_saldo_grande = tk.Label(self.header, text="$ 0.00", font=("Segoe UI", 35, "bold"), fg="#ffffff", bg="#2f3640")
        self.label_saldo_grande.pack()

        self.sub_header = tk.Frame(self.header, bg="#2f3640")
        self.sub_header.pack(pady=10)
        self.lbl_resumen_ingreso = tk.Label(self.sub_header, text="Ingresos: $0.00", font=("Segoe UI", 10, "bold"), fg="#2ecc71", bg="#2f3640")
        self.lbl_resumen_ingreso.pack(side="left", padx=30)
        self.lbl_resumen_gasto = tk.Label(self.sub_header, text="Gastos: $0.00", font=("Segoe UI", 10, "bold"), fg="#e74c3c", bg="#2f3640")
        self.lbl_resumen_gasto.pack(side="left", padx=30)

        # --- 2. CUERPO ---
        self.cuerpo = tk.Frame(self.root, bg="#f4f7f6")
        self.cuerpo.pack(fill="both", expand=True, padx=20, pady=20)

        # Panel Izquierdo: Formulario
        self.frame_form = tk.Frame(self.cuerpo, bg="#ffffff", padx=20, pady=20, highlightbackground="#dcdde1", highlightthickness=1)
        self.frame_form.pack(side="left", fill="y")

        tk.Label(self.frame_form, text="NUEVO REGISTRO", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#2f3640").pack(pady=(0, 20))

        tk.Label(self.frame_form, text="Concepto:", bg="#ffffff", fg="#7f8c8d").pack(anchor="w")
        self.entry_concepto = tk.Entry(self.frame_form, font=("Segoe UI", 11), bd=0, bg="#f1f2f6")
        self.entry_concepto.pack(fill="x", pady=(5, 15), ipady=5)

        tk.Label(self.frame_form, text="Monto ($):", bg="#ffffff", fg="#7f8c8d").pack(anchor="w")
        self.entry_monto = tk.Entry(self.frame_form, font=("Segoe UI", 11), bd=0, bg="#f1f2f6")
        self.entry_monto.pack(fill="x", pady=(5, 15), ipady=5)

        tk.Label(self.frame_form, text="Tipo:", bg="#ffffff", fg="#7f8c8d").pack(anchor="w")
        self.combo_tipo = ttk.Combobox(self.frame_form, values=["Ingreso", "Gasto"], state="readonly")
        self.combo_tipo.current(1)
        self.combo_tipo.pack(fill="x", pady=(5, 25))

        btn_guardar = tk.Button(self.frame_form, text="GUARDAR", command=self.guardar_datos, bg="#2ecc71", fg="white", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2", pady=10)
        btn_guardar.pack(fill="x", pady=5)

        # SECCIÓN DE EXPORTACIÓN
        tk.Label(self.frame_form, text="ACCIONES", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#7f8c8d").pack(pady=(30, 10))
        
        btn_exportar = tk.Button(self.frame_form, text="EXPORTAR A EXCEL (CSV)", command=self.exportar_csv, bg="#3498db", fg="white", font=("Segoe UI", 9), bd=0, cursor="hand2", pady=8)
        btn_exportar.pack(fill="x")

        # Panel Derecho: Tabla
        self.frame_tabla = tk.Frame(self.cuerpo, bg="#f4f7f6")
        self.frame_tabla.pack(side="right", fill="both", expand=True, padx=(20, 0))

        tk.Label(self.frame_tabla, text="HISTORIAL DE TRANSACCIONES", font=("Segoe UI", 11, "bold"), bg="#f4f7f6", fg="#2f3640").pack(anchor="w", pady=(0, 10))

        columnas = ("ID", "Fecha", "Concepto", "Monto", "Tipo")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")
        
        self.tabla.column("ID", width=50)
        self.tabla.column("Concepto", width=250)
        self.tabla.pack(fill="both", expand=True)

        btn_borrar = tk.Button(self.frame_tabla, text="Eliminar Seleccionado", command=self.eliminar_registro, bg="#e74c3c", fg="white", bd=0, pady=5, padx=10, cursor="hand2")
        btn_borrar.pack(anchor="e", pady=10)

        self.actualizar_vista()

    # --- MÉTODOS ---

    def inicializar_bd(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS movimientos (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, concepto TEXT, monto REAL, tipo TEXT)")

    def guardar_datos(self):
        concepto, monto, tipo = self.entry_concepto.get(), self.entry_monto.get(), self.combo_tipo.get()
        if not concepto or not monto:
            messagebox.showwarning("Campos vacíos", "Completa la descripción y el monto.")
            return
        try:
            monto_f = float(monto)
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("INSERT INTO movimientos VALUES (NULL, ?, ?, ?, ?)", (fecha, concepto, monto_f, tipo))
            self.entry_concepto.delete(0, tk.END)
            self.entry_monto.delete(0, tk.END)
            self.actualizar_vista()
        except ValueError:
            messagebox.showerror("Error", "Monto inválido.")

    def actualizar_vista(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        t_ing, t_gas = 0, 0
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movimientos ORDER BY id DESC")
            for fila in cursor.fetchall():
                self.tabla.insert("", "end", values=(fila[0], fila[1], fila[2], f"${fila[3]:,.2f}", fila[4]))
                if fila[4] == "Ingreso": t_ing += fila[3]
                else: t_gas += fila[3]
        
        saldo = t_ing - t_gas
        self.label_saldo_grande.config(text=f"$ {saldo:,.2f}", fg="#2ecc71" if saldo >= 0 else "#e74c3c")
        self.lbl_resumen_ingreso.config(text=f"Ingresos: ${t_ing:,.2f}")
        self.lbl_resumen_gasto.config(text=f"Gastos: ${t_gas:,.2f}")

    def eliminar_registro(self):
        try:
            id_reg = self.tabla.item(self.tabla.selection()[0])['values'][0]
            if messagebox.askyesno("Confirmar", "¿Eliminar este registro?"):
                with sqlite3.connect(self.db_name) as conn:
                    conn.execute("DELETE FROM movimientos WHERE id = ?", (id_reg,))
                self.actualizar_vista()
        except IndexError:
            messagebox.showwarning("Atención", "Selecciona una fila.")

    def exportar_csv(self):
        """Lógica para guardar el historial en un archivo externo"""
        try:
            # Preguntar al usuario dónde guardar
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivo CSV", "*.csv"), ("Todos los archivos", "*.*")],
                title="Guardar Historial Financiero"
            )
            
            if archivo:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM movimientos")
                    filas = cursor.fetchall()
                    
                with open(archivo, mode='w', newline='', encoding='utf-8') as f:
                    escritor = csv.writer(f)
                    # Escribir cabeceras
                    escritor.writerow(['ID', 'Fecha', 'Concepto', 'Monto', 'Tipo'])
                    # Escribir datos
                    escritor.writerows(filas)
                
                messagebox.showinfo("Éxito", f"Datos exportados correctamente en:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorFinanzasPro(root)
    root.mainloop()