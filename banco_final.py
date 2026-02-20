import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime

# --- LIBRERÍAS PARA PDF ---
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
except ImportError:
    print("Error: La librería 'reportlab' no está instalada. Ejecuta: pip install reportlab")

class GestorFinanzasPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Saldos y Movimientos Pro - Export Edition")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f4f7f6")

        self.db_name = 'control_gastos.db'
        self.inicializar_bd()

        # Estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#ffffff", foreground="#333333", rowheight=30, fieldbackground="#ffffff", font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", background="#dcdde1", foreground="#2f3640", font=("Segoe UI", 10, "bold"))

        # Interfaz
        self.crear_interfaz()
        self.actualizar_vista()

    def inicializar_bd(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS movimientos (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, concepto TEXT, monto REAL, tipo TEXT)")

    def crear_interfaz(self):
        # Encabezado
        self.header = tk.Frame(self.root, bg="#2f3640", height=150)
        self.header.pack(fill="x", side="top")
        
        tk.Label(self.header, text="DISPONIBLE ACTUAL", font=("Segoe UI", 12), fg="#dcdde1", bg="#2f3640").pack(pady=(20, 0))
        self.label_saldo_grande = tk.Label(self.header, text="$ 0.00", font=("Segoe UI", 35, "bold"), fg="#ffffff", bg="#2f3640")
        self.label_saldo_grande.pack()

        # Cuerpo
        self.cuerpo = tk.Frame(self.root, bg="#f4f7f6")
        self.cuerpo.pack(fill="both", expand=True, padx=20, pady=20)

        # Formulario
        self.frame_form = tk.Frame(self.cuerpo, bg="#ffffff", padx=20, pady=20, highlightbackground="#dcdde1", highlightthickness=1)
        self.frame_form.pack(side="left", fill="y")

        tk.Label(self.frame_form, text="Concepto:", bg="#ffffff").pack(anchor="w")
        self.entry_concepto = tk.Entry(self.frame_form, font=("Segoe UI", 11), bg="#f1f2f6", bd=0)
        self.entry_concepto.pack(fill="x", pady=5, ipady=5)

        tk.Label(self.frame_form, text="Monto ($):", bg="#ffffff").pack(anchor="w")
        self.entry_monto = tk.Entry(self.frame_form, font=("Segoe UI", 11), bg="#f1f2f6", bd=0)
        self.entry_monto.pack(fill="x", pady=5, ipady=5)

        self.combo_tipo = ttk.Combobox(self.frame_form, values=["Ingreso", "Gasto"], state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack(fill="x", pady=10)

        tk.Button(self.frame_form, text="GUARDAR", command=self.guardar_datos, bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), bd=0, pady=10).pack(fill="x", pady=10)

        # Botones de Exportación
        tk.Label(self.frame_form, text="EXPORTAR", bg="#ffffff", font=("Segoe UI", 10, "bold")).pack(pady=(20, 5))
        
        tk.Button(self.frame_form, text="A EXCEL (CSV)", command=self.exportar_csv, bg="#3498db", fg="white", bd=0, pady=7).pack(fill="x", pady=2)
        tk.Button(self.frame_form, text="A PDF", command=self.exportar_pdf, bg="#e67e22", fg="white", bd=0, pady=7).pack(fill="x", pady=2)

        # Tabla
        self.frame_tabla = tk.Frame(self.cuerpo, bg="#f4f7f6")
        self.frame_tabla.pack(side="right", fill="both", expand=True, padx=(20, 0))

        columnas = ("ID", "Fecha", "Concepto", "Monto", "Tipo")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=100)
        self.tabla.pack(fill="both", expand=True)

    def guardar_datos(self):
        concepto, monto = self.entry_concepto.get(), self.entry_monto.get()
        if not concepto or not monto: return
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("INSERT INTO movimientos (fecha, concepto, monto, tipo) VALUES (?, ?, ?, ?)",
                             (datetime.now().strftime("%d/%m/%Y %H:%M"), concepto, float(monto), self.combo_tipo.get()))
            self.entry_concepto.delete(0, tk.END)
            self.entry_monto.delete(0, tk.END)
            self.actualizar_vista()
        except Exception as e: messagebox.showerror("Error", str(e))

    def actualizar_vista(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        saldo = 0
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movimientos ORDER BY id DESC")
            for f in cursor.fetchall():
                self.tabla.insert("", "end", values=(f[0], f[1], f[2], f"${f[3]:,.2f}", f[4]))
                saldo += f[3] if f[4] == "Ingreso" else -f[3]
        self.label_saldo_grande.config(text=f"$ {saldo:,.2f}", fg="#2ecc71" if saldo >= 0 else "#e74c3c")

    def exportar_csv(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if archivo:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM movimientos")
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Fecha', 'Concepto', 'Monto', 'Tipo'])
                    writer.writerows(cursor.fetchall())
            messagebox.showinfo("Éxito", "Excel (CSV) guardado.")

    # --- FUNCIÓN PDF CORREGIDA ---
    def exportar_pdf(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not archivo: return

        try:
            doc = SimpleDocTemplate(archivo, pagesize=letter)
            estilos = getSampleStyleSheet()
            elementos = []

            # Encabezado del PDF
            elementos.append(Paragraph("<b>ESTADO DE CUENTA PRO</b>", estilos['Title']))
            elementos.append(Spacer(1, 12))

            # Obtener datos de la BD
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT fecha, concepto, monto, tipo FROM movimientos")
                filas = cursor.fetchall()

            if not filas:
                messagebox.showwarning("Aviso", "No hay datos para exportar.")
                return

            # Preparar Tabla
            data = [["FECHA", "CONCEPTO", "MONTO", "TIPO"]]
            for f in filas:
                data.append([f[0], f[1], f"${f[2]:,.2f}", f[3]])

            # Crear tabla con estilos
            t = Table(data, colWidths=[110, 220, 80, 80])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.darkslategray),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))

            # Colores para Ingreso/Gasto
            for i in range(1, len(data)):
                color = colors.green if data[i][3] == "Ingreso" else colors.red
                t.setStyle(TableStyle([('TEXTCOLOR', (3, i), (3, i), color)]))

            elementos.append(t)
            doc.build(elementos)
            messagebox.showinfo("Éxito", "Reporte PDF generado correctamente.")

        except PermissionError:
            messagebox.showerror("Error", "Cierra el PDF antes de generar uno nuevo.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorFinanzasPro(root)
    root.mainloop()