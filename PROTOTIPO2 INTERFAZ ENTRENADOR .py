import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar
import sqlite3

class SistemaEntrenadorFinal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FC BOGOTÁ - Gestión Profesional")
        self.root.geometry("1300x850")
        self.root.configure(bg="#F4F7F6")

        # --- CONFIGURACIÓN DE BASE DE DATOS ---
        self.db_name = "escuela_futbol.db" # <--- USA EL NOMBRE DE TU DB DEL LOGIN
        self.inicializar_tablas()
        
        # Cargar datos iniciales desde la DB
        self.cargar_datos_maestros()

        self.setup_main_layout()
        self.seccion_bienvenida() 
        self.root.mainloop()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def inicializar_tablas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        # Tabla Jugadores
        cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)''')
        # Tabla Asistencia
        cursor.execute('''CREATE TABLE IF NOT EXISTS asistencia (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, fecha TEXT, estado TEXT)''')
        # Tabla Stats Jugadores
        cursor.execute('''CREATE TABLE IF NOT EXISTS stats_jugadores (nombre TEXT PRIMARY KEY, goles INTEGER, asistencias INTEGER, partidos INTEGER)''')
        # Tabla Stats Club
        cursor.execute('''CREATE TABLE IF NOT EXISTS stats_club (id INTEGER PRIMARY KEY, jugados INTEGER, ganados INTEGER, empatados INTEGER, perdidos INTEGER, goles_favor INTEGER, goles_contra INTEGER)''')
        
        # Insertar datos de prueba si está vacía
        cursor.execute("SELECT COUNT(*) FROM jugadores")
        if cursor.fetchone()[0] == 0:
            nombres = ["Mateo Rodriguez", "Santiago Castro", "Andrés Villa", "Luis Díaz"]
            for n in nombres:
                cursor.execute("INSERT INTO jugadores (nombre) VALUES (?)", (n,))
                cursor.execute("INSERT INTO stats_jugadores VALUES (?, 0, 0, 0)", (n,))
            cursor.execute("INSERT INTO stats_club VALUES (1, 0, 0, 0, 0, 0, 0)")
        
        conn.commit()
        conn.close()

    def cargar_datos_maestros(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM jugadores")
        self.jugadores = [fila[0] for fila in cursor.fetchall()]
        conn.close()

    def setup_main_layout(self):
        self.sidebar = tk.Frame(self.root, bg="#1A252F", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self.root, bg="#F4F7F6")
        self.content.pack(side="right", fill="both", expand=True)

        tk.Label(self.sidebar, text="FC BOGOTÁ", font=("Helvetica", 18, "bold"), bg="#1A252F", fg="#27AE60").pack(pady=30)
        
        opciones = [
            ("📅 Control Asistencia", self.seccion_asistencia),
            ("📊 Stats Jugadores", self.seccion_stats_jugadores),
            ("🏆 Stats Equipo", self.seccion_stats_equipo)
        ]

        for texto, comando in opciones:
            tk.Button(self.sidebar, text=texto, font=("Helvetica", 11, "bold"), bg="#1A252F", fg="white", 
                      bd=0, padx=20, pady=15, anchor="w", cursor="hand2", 
                      activebackground="#2C3E50", command=comando).pack(fill="x")

    def limpiar_pantalla(self):
        for widget in self.content.winfo_children(): widget.destroy()

    def seccion_bienvenida(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Panel de Control Conectado", font=("Helvetica", 24, "bold"), bg="#F4F7F6", fg="#1A252F").pack(pady=100)
        tk.Label(self.content, text="Base de Datos: Activa", font=("Helvetica", 12), bg="#F4F7F6", fg="green").pack()

    # =================================================================
    # MÓDULO 1: ASISTENCIA (AHORA CON SQL)
    # =================================================================
    def seccion_asistencia(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Gestión de Asistencia", font=("Helvetica", 20, "bold"), bg="#F4F7F6").pack(anchor="w", padx=20, pady=20)
        f_main = tk.Frame(self.content, bg="#F4F7F6")
        f_main.pack(fill="both", expand=True, padx=20)
        
        col_fecha = tk.LabelFrame(f_main, text=" 1. Fecha ", bg="white", padx=10, pady=10)
        col_fecha.pack(side="left", fill="y", padx=5)
        self.cb_dia = ttk.Combobox(col_fecha, values=[str(i).zfill(2) for i in range(1, 32)], width=5); self.cb_dia.set(datetime.now().strftime("%d")); self.cb_dia.pack()
        self.cb_mes = ttk.Combobox(col_fecha, values=[str(i).zfill(2) for i in range(1, 13)], width=5); self.cb_mes.set(datetime.now().strftime("%m")); self.cb_mes.pack()
        self.cb_ano = ttk.Combobox(col_fecha, values=["2025", "2026"], width=5); self.cb_ano.set("2026"); self.cb_ano.pack()
        tk.Button(col_fecha, text="Cargar Lista", command=self.dibujar_lista_asistencia, bg="#3498DB", fg="white").pack(pady=10, fill="x")
        
        self.col_lista_asis = tk.LabelFrame(f_main, text=" 2. Pasar Lista ", bg="white", padx=10, pady=10)
        self.col_lista_asis.pack(side="left", fill="both", expand=True, padx=5)
        self.col_historial_asis = tk.LabelFrame(f_main, text=" 3. Resumen ", bg="white", padx=10, pady=10)
        self.col_historial_asis.pack(side="left", fill="both", expand=True, padx=5)

    def dibujar_lista_asistencia(self):
        for w in self.col_lista_asis.winfo_children(): w.destroy()
        fecha = f"{self.cb_dia.get()}/{self.cb_mes.get()}/{self.cb_ano.get()}"
        self.vars_asis = {}
        for j in self.jugadores:
            f = tk.Frame(self.col_lista_asis, bg="white")
            f.pack(fill="x", pady=2)
            tk.Label(f, text=j, bg="white", width=15, anchor="w").pack(side="left")
            v = tk.StringVar(value="Pendiente"); self.vars_asis[j] = v
            tk.Radiobutton(f, text="V", variable=v, value="Asistio", bg="white").pack(side="left")
            tk.Radiobutton(f, text="F", variable=v, value="Falto", bg="white").pack(side="left")
            tk.Button(f, text="Hist", font=("Arial", 7), command=lambda n=j: self.dibujar_calendario_asis(n)).pack(side="right")
        tk.Button(self.col_lista_asis, text="GUARDAR EN DB", bg="#27AE60", fg="white", command=self.guardar_asistencia).pack(pady=10, fill="x")

    def guardar_asistencia(self):
        fecha = f"{self.cb_dia.get()}/{self.cb_mes.get()}/{self.cb_ano.get()}"
        conn = self.conectar(); cursor = conn.cursor()
        for j, v in self.vars_asis.items():
            if v.get() != "Pendiente":
                cursor.execute("DELETE FROM asistencia WHERE nombre=? AND fecha=?", (j, fecha))
                cursor.execute("INSERT INTO asistencia (nombre, fecha, estado) VALUES (?, ?, ?)", (j, fecha, v.get()))
        conn.commit(); conn.close()
        messagebox.showinfo("Éxito", "Asistencia sincronizada con la base de datos.")

    def dibujar_calendario_asis(self, nombre):
        for w in self.col_historial_asis.winfo_children(): w.destroy()
        tk.Label(self.col_historial_asis, text=f"Récord de {nombre}", bg="white", font=("bold")).pack()
        grid = tk.Frame(self.col_historial_asis, bg="white"); grid.pack()
        
        mes, ano = int(self.cb_mes.get()), int(self.cb_ano.get())
        cal_matriz = calendar.monthcalendar(ano, mes)
        
        conn = self.conectar(); cursor = conn.cursor()
        cursor.execute("SELECT fecha, estado FROM asistencia WHERE nombre=?", (nombre,))
        datos = dict(cursor.fetchall())
        conn.close()

        for r, sem in enumerate(cal_matriz):
            for c, dia in enumerate(sem):
                if dia == 0: continue
                f_key = f"{str(dia).zfill(2)}/{str(mes).zfill(2)}/{ano}"
                estado = datos.get(f_key, "N")
                color = "#EEE"
                if estado == "Asistio": color = "#28A745"
                elif estado == "Falto": color = "#DC3545"
                tk.Label(grid, text=str(dia), bg=color, width=3).grid(row=r, column=c, padx=1, pady=1)

    # =================================================================
    # MÓDULO 2: STATS JUGADORES (CON SQL)
    # =================================================================
    def seccion_stats_jugadores(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Estadísticas de Jugadores", font=("Helvetica", 20, "bold"), bg="#F4F7F6").pack(anchor="w", padx=20, pady=20)
        f_stats = tk.Frame(self.content, bg="#F4F7F6")
        f_stats.pack(fill="both", expand=True, padx=20)
        
        f_edit = tk.LabelFrame(f_stats, text=" Editar ", bg="white", padx=15, pady=15)
        f_edit.pack(side="left", fill="y", padx=5)
        self.cb_j_stats = ttk.Combobox(f_edit, values=self.jugadores, state="readonly"); self.cb_j_stats.pack(fill="x")
        self.cb_j_stats.bind("<<ComboboxSelected>>", self.cargar_stats_campos)
        self.ent_g = tk.Entry(f_edit); self.ent_a = tk.Entry(f_edit); self.ent_p = tk.Entry(f_edit)
        for e, t in [(self.ent_g, "Goles:"), (self.ent_a, "Asist:"), (self.ent_p, "Part:")]:
            tk.Label(f_edit, text=t, bg="white").pack(anchor="w"); e.pack(fill="x", pady=2)
        tk.Button(f_edit, text="ACTUALIZAR DB", bg="#27AE60", fg="white", command=self.guardar_stats).pack(pady=20, fill="x")
        
        f_tabla = tk.LabelFrame(f_stats, text=" Tabla General ", bg="white", padx=10, pady=10)
        f_tabla.pack(side="left", fill="both", expand=True, padx=5)
        cols = ("Jugador", "Goles", "Asistencias", "Partidos")
        self.tree = ttk.Treeview(f_tabla, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=80, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.actualizar_tabla_stats()

    def actualizar_tabla_stats(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        conn = self.conectar(); cursor = conn.cursor()
        cursor.execute("SELECT * FROM stats_jugadores")
        for fila in cursor.fetchall(): self.tree.insert("", "end", values=fila)
        conn.close()

    def cargar_stats_campos(self, event):
        j = self.cb_j_stats.get()
        conn = self.conectar(); cursor = conn.cursor()
        cursor.execute("SELECT goles, asistencias, partidos FROM stats_jugadores WHERE nombre=?", (j,))
        s = cursor.fetchone()
        self.ent_g.delete(0, tk.END); self.ent_g.insert(0, str(s[0]))
        self.ent_a.delete(0, tk.END); self.ent_a.insert(0, str(s[1]))
        self.ent_p.delete(0, tk.END); self.ent_p.insert(0, str(s[2]))
        conn.close()

    def guardar_stats(self):
        j = self.cb_j_stats.get()
        if j:
            conn = self.conectar(); cursor = conn.cursor()
            cursor.execute("UPDATE stats_jugadores SET goles=?, asistencias=?, partidos=? WHERE nombre=?", 
                           (self.ent_g.get(), self.ent_a.get(), self.ent_p.get(), j))
            conn.commit(); conn.close()
            self.actualizar_tabla_stats(); messagebox.showinfo("Ok", "Base de datos actualizada.")

    # =================================================================
    # MÓDULO 3: STATS EQUIPO (CON SQL)
    # =================================================================
    def seccion_stats_equipo(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Rendimiento del Club", font=("Helvetica", 22, "bold"), bg="#F4F7F6").pack(anchor="w", padx=30, pady=20)
        self.f_cards = tk.Frame(self.content, bg="#F4F7F6"); self.f_cards.pack(fill="x", padx=30)
        
        f_bottom = tk.Frame(self.content, bg="#F4F7F6"); f_bottom.pack(fill="both", expand=True, padx=30, pady=20)
        f_edit_club = tk.LabelFrame(f_bottom, text=" Actualizar Temporada ", bg="white", padx=20, pady=20)
        f_edit_club.pack(side="left", fill="both", expand=True)

        self.inputs_club = {}
        campos = [("Jugados:", "jugados"), ("Ganados:", "ganados"), ("Empatados:", "empatados"), 
                  ("Perdidos:", "perdidos"), ("Favor:", "goles_favor"), ("Contra:", "goles_contra")]
        
        conn = self.conectar(); cursor = conn.cursor()
        cursor.execute("SELECT * FROM stats_club WHERE id=1")
        actuales = cursor.fetchone()
        conn.close()

        for i, (label, key) in enumerate(campos):
            tk.Label(f_edit_club, text=label, bg="white").grid(row=i//2*2, column=i%2, sticky="w")
            ent = tk.Entry(f_edit_club); ent.insert(0, str(actuales[i+1])); ent.grid(row=i//2*2+1, column=i%2, padx=10)
            self.inputs_club[key] = ent

        tk.Button(f_edit_club, text="GUARDAR BALANCE", bg="#27AE60", fg="white", command=self.actualizar_club_stats).grid(row=6, column=0, columnspan=2, pady=20)
        self.dibujar_tarjetas_equipo()

    def dibujar_tarjetas_equipo(self):
        for w in self.f_cards.winfo_children(): w.destroy()
        conn = self.conectar(); cursor = conn.cursor(); cursor.execute("SELECT * FROM stats_club WHERE id=1"); s = cursor.fetchone(); conn.close()
        titulos = ["PJ", "PG", "PE", "PP", "GF", "GC"]
        for i in range(1, 7):
            card = tk.Frame(self.f_cards, bg="white", width=100, height=80, relief="groove", bd=2)
            card.pack(side="left", padx=5, expand=True, fill="both")
            tk.Label(card, text=titulos[i-1], bg="white", fg="gray").pack()
            tk.Label(card, text=str(s[i]), font=("Arial", 18, "bold"), bg="white").pack()

    def actualizar_club_stats(self):
        conn = self.conectar(); cursor = conn.cursor()
        cursor.execute("UPDATE stats_club SET jugados=?, ganados=?, empatados=?, perdidos=?, goles_favor=?, goles_contra=? WHERE id=1",
                       (self.inputs_club['jugados'].get(), self.inputs_club['ganados'].get(), self.inputs_club['empatados'].get(),
                        self.inputs_club['perdidos'].get(), self.inputs_club['goles_favor'].get(), self.inputs_club['goles_contra'].get()))
        conn.commit(); conn.close()
        self.dibujar_tarjetas_equipo(); messagebox.showinfo("Ok", "Equipo actualizado.")

if __name__ == "__main__":
    SistemaEntrenadorFinal()