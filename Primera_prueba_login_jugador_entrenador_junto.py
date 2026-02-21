import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3
import calendar

# =================================================================
# 1. INTERFAZ DEL JUGADOR (TAL CUAL LA TENÍAS)
# =================================================================
class InterfazJugador:
    def __init__(self, container, nombre_jugador, app_instance):
        self.root = container
        self.nombre_jugador = nombre_jugador
        self.app = app_instance
        
        # --- PALETA DE COLORES (MODERN LIGHT) ---
        self.bg_principal = "#F0F2F5"
        self.bg_sidebar = "#FFFFFF"
        self.azul_fcb = "#00468C"
        self.verde_exito = "#28A745"
        self.rojo_error = "#DC3545"
        self.texto_p = "#1C1E21"
        self.texto_s = "#606770"

        self.setup_layout()
        self.setup_sidebar()
        self.seccion_inicio()
        self.actualizar_reloj()

    def setup_layout(self):
        for widget in self.root.winfo_children(): widget.destroy()
        
        self.sidebar = tk.Frame(self.root, bg=self.bg_sidebar, width=260, highlightthickness=1, highlightbackground="#E9ECEF")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self.root, bg=self.bg_principal, padx=40, pady=20)
        self.content.pack(side="right", fill="both", expand=True)

    def setup_sidebar(self):
        tk.Label(self.sidebar, text="FC BOGOTÁ", font=("Helvetica", 24, "bold"), bg=self.bg_sidebar, fg=self.azul_fcb).pack(pady=(40, 5))
        tk.Label(self.sidebar, text="PERFIL DEL DEPORTISTA", font=("Helvetica", 8, "bold"), bg=self.bg_sidebar, fg=self.texto_s).pack(pady=(0, 40))

        self.crear_boton_menu("🏠 Inicio", self.seccion_inicio)
        self.crear_boton_menu("📅 Mi Asistencia", self.seccion_asistencia)
        self.crear_boton_menu("📋 Convocatoria", self.seccion_convocatoria)
        
        tk.Label(self.sidebar, text="RENDIMIENTO", font=("Helvetica", 7, "bold"), bg=self.bg_sidebar, fg=self.texto_s).pack(anchor="w", padx=25, pady=(20, 5))
        self.crear_boton_menu("👥 Stats del Equipo", self.seccion_stats_jugadores)
        self.crear_boton_menu("⚽ Stats de Partidos", self.seccion_stats_partidos)
        
        tk.Label(self.sidebar, text="PERSONAL", font=("Helvetica", 7, "bold"), bg=self.bg_sidebar, fg=self.texto_s).pack(anchor="w", padx=25, pady=(20, 5))
        self.crear_boton_menu("🏥 Salud y Estado", self.seccion_salud)
        self.crear_boton_menu("💳 Gestión de Pagos", self.seccion_pagos)

        tk.Button(self.sidebar, text="Cerrar Sesión", font=("Helvetica", 10), bg="#F8D7DA", fg="#842029", bd=0, pady=8, 
                  command=self.app.mostrar_login).pack(side="bottom", fill="x", pady=20, padx=20)

    def crear_boton_menu(self, texto, comando):
        btn = tk.Button(self.sidebar, text=texto, font=("Helvetica", 11), bg=self.bg_sidebar, fg=self.texto_p,
                        bd=0, padx=30, pady=12, anchor="w", cursor="hand2", activebackground="#F1F3F5", command=comando)
        btn.pack(fill="x")

    def limpiar_pantalla(self):
        for widget in self.content.winfo_children(): widget.destroy()

    def actualizar_reloj(self):
        ahora = datetime.now()
        proximo = ahora.replace(hour=16, minute=0, second=0, microsecond=0) + timedelta(days=1)
        diff = proximo - ahora
        h, rem = divmod(diff.seconds, 3600)
        m, s = divmod(rem, 60)
        if hasattr(self, 'label_reloj') and self.label_reloj.winfo_exists():
            self.label_reloj.config(text=f"{h:02d}h {m:02d}m {s:02d}s")
            self.root.after(1000, self.actualizar_reloj)

    def seccion_inicio(self):
        self.limpiar_pantalla()
        header = tk.Frame(self.content, bg=self.bg_principal)
        header.pack(fill="x", pady=(0, 20))
        tk.Label(header, text=f"Hola, {self.nombre_jugador} 👋", font=("Helvetica", 28, "bold"), bg=self.bg_principal).pack(side="left")
        
        reloj_f = tk.Frame(header, bg=self.azul_fcb, padx=15, pady=5)
        reloj_f.pack(side="right")
        tk.Label(reloj_f, text="PRÓXIMO EVENTO EN:", font=("Helvetica", 8, "bold"), bg=self.azul_fcb, fg="white").pack()
        self.label_reloj = tk.Label(reloj_f, text="--h --m --s", font=("Consolas", 12, "bold"), bg=self.azul_fcb, fg=self.verde_exito)
        self.label_reloj.pack()
        self.seccion_convocatoria(incrustada=True)

    def seccion_asistencia(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Mi Disciplina (Asistencia)", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        grid_f = tk.Frame(self.content, bg="white", padx=25, pady=25, highlightthickness=1, highlightbackground="#EEE")
        grid_f.pack(fill="x")
        asistencias = [2, 4, 6, 9, 11, 13, 16, 18, 20]
        for i in range(1, 29):
            bg = self.verde_exito if i in asistencias else "#F8F9FA"
            lbl = tk.Label(grid_f, text=str(i), bg=bg, fg="white" if i in asistencias else "#CCC", width=4, height=2, font=("Helvetica", 10, "bold"))
            lbl.grid(row=(i-1)//7 + 1, column=(i-1)%7, padx=4, pady=4)

    def seccion_convocatoria(self, incrustada=False):
        if not incrustada: self.limpiar_pantalla()
        tk.Label(self.content, text="Estado de Convocatoria", font=("Helvetica", 18, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(20,10))
        card = tk.Frame(self.content, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#EEE")
        card.pack(fill="x")
        tk.Label(card, text="CONVOCADO - TITULAR ✅", font=("Helvetica", 15, "bold"), bg="white", fg=self.verde_exito).pack(side="left")

    def seccion_stats_jugadores(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Rendimiento del Equipo", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        cols = ("Jugador", "Posición", "Goles", "Asistencias", "Calificación")
        tabla = ttk.Treeview(self.content, columns=cols, show="headings")
        for c in cols: tabla.heading(c, text=c)
        tabla.insert("", "end", values=("M. Rodriguez", "Delantero", "12", "4", "9.2"))
        tabla.pack(fill="both", expand=True)

    def seccion_stats_partidos(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Balance de la Temporada", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        frame_cards = tk.Frame(self.content, bg=self.bg_principal)
        frame_cards.pack(fill="x")
        stats = [("PJ", "12", self.azul_fcb), ("PG", "9", self.verde_exito)]
        for i, (tit, val, col) in enumerate(stats):
            c = tk.Frame(frame_cards, bg="white", padx=35, pady=20, highlightthickness=1, highlightbackground="#EEE")
            c.grid(row=0, column=i, padx=5)
            tk.Label(c, text=tit, font=("Helvetica", 8, "bold"), bg="white", fg=self.texto_s).pack()
            tk.Label(c, text=val, font=("Helvetica", 20, "bold"), bg="white", fg=col).pack()

    def seccion_salud(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Salud y Estado Físico", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        card = tk.Frame(self.content, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#EEE")
        card.pack(fill="x")
        tk.Label(card, text="ESTADO: APTO PARA COMPETIR ✅", font=("Helvetica", 14, "bold"), bg="white", fg=self.verde_exito).pack()

    def seccion_pagos(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Gestión de Pagos", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        card = tk.Frame(self.content, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#EEE")
        card.pack(fill="x")
        tk.Label(card, text="MENSUALIDAD: AL DÍA", font=("Helvetica", 14, "bold"), bg="white", fg=self.verde_exito).pack()

# =================================================================
# 2. INTERFAZ DEL ENTRENADOR (TAL CUAL LA TENÍAS)
# =================================================================
class InterfazEntrenador:
    def __init__(self, container, nombre_entrenador, app_instance):
        self.root = container
        self.app = app_instance
        self.db_name = "escuela_futbol.db"
        
        self.inicializar_tablas()
        self.cargar_datos_maestros()
        self.setup_main_layout()
        self.seccion_bienvenida()

    def conectar(self): return sqlite3.connect(self.db_name)

    def inicializar_tablas(self):
        conn = self.conectar(); cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS asistencia (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, fecha TEXT, estado TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS stats_jugadores (nombre TEXT PRIMARY KEY, goles INTEGER, asistencias INTEGER, partidos INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS stats_club (id INTEGER PRIMARY KEY, jugados INTEGER, ganados INTEGER, empatados INTEGER, perdidos INTEGER, goles_favor INTEGER, goles_contra INTEGER)''')
        
        cursor.execute("SELECT COUNT(*) FROM jugadores")
        if cursor.fetchone()[0] == 0:
            nombres = ["Mateo Rodriguez", "Santiago Castro", "Andrés Villa", "Luis Díaz"]
            for n in nombres:
                cursor.execute("INSERT OR IGNORE INTO jugadores (nombre) VALUES (?)", (n,))
                cursor.execute("INSERT OR IGNORE INTO stats_jugadores VALUES (?, 0, 0, 0)", (n,))
            cursor.execute("INSERT OR IGNORE INTO stats_club VALUES (1, 0, 0, 0, 0, 0, 0)")
        conn.commit(); conn.close()

    def cargar_datos_maestros(self):
        conn = self.conectar(); cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM jugadores")
        self.jugadores = [fila[0] for fila in cursor.fetchall()]
        conn.close()

    def setup_main_layout(self):
        for widget in self.root.winfo_children(): widget.destroy()
        self.sidebar = tk.Frame(self.root, bg="#1A252F", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self.content = tk.Frame(self.root, bg="#F4F7F6")
        self.content.pack(side="right", fill="both", expand=True)

        tk.Label(self.sidebar, text="FC BOGOTÁ", font=("Helvetica", 18, "bold"), bg="#1A252F", fg="#27AE60").pack(pady=30)
        opciones = [("📅 Control Asistencia", self.seccion_asistencia), ("📊 Stats Jugadores", self.seccion_stats_jugadores), ("🏆 Stats Equipo", self.seccion_stats_equipo)]
        for texto, comando in opciones:
            tk.Button(self.sidebar, text=texto, font=("Helvetica", 11, "bold"), bg="#1A252F", fg="white", bd=0, padx=20, pady=15, anchor="w", cursor="hand2", command=comando).pack(fill="x")
        
        tk.Button(self.sidebar, text="Cerrar Sesión", bg="#E74C3C", fg="white", command=self.app.mostrar_login).pack(side="bottom", fill="x", pady=20, padx=20)

    def limpiar_pantalla(self):
        for widget in self.content.winfo_children(): widget.destroy()

    def seccion_bienvenida(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Panel de Control Conectado", font=("Helvetica", 24, "bold"), bg="#F4F7F6", fg="#1A252F").pack(pady=100)

    def seccion_asistencia(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Gestión de Asistencia", font=("Helvetica", 20, "bold"), bg="#F4F7F6").pack(anchor="w", padx=20, pady=20)
        f_main = tk.Frame(self.content, bg="#F4F7F6"); f_main.pack(fill="both", expand=True, padx=20)
        col_fecha = tk.LabelFrame(f_main, text=" 1. Fecha ", bg="white", padx=10, pady=10); col_fecha.pack(side="left", fill="y", padx=5)
        self.cb_dia = ttk.Combobox(col_fecha, values=[str(i).zfill(2) for i in range(1, 32)], width=5); self.cb_dia.set(datetime.now().strftime("%d")); self.cb_dia.pack()
        self.cb_mes = ttk.Combobox(col_fecha, values=[str(i).zfill(2) for i in range(1, 13)], width=5); self.cb_mes.set(datetime.now().strftime("%m")); self.cb_mes.pack()
        self.cb_ano = ttk.Combobox(col_fecha, values=["2025", "2026"], width=5); self.cb_ano.set("2026"); self.cb_ano.pack()
        tk.Button(col_fecha, text="Cargar Lista", command=self.dibujar_lista_asistencia, bg="#3498DB", fg="white").pack(pady=10, fill="x")
        self.col_lista_asis = tk.LabelFrame(f_main, text=" 2. Pasar Lista ", bg="white", padx=10, pady=10); self.col_lista_asis.pack(side="left", fill="both", expand=True, padx=5)
        self.col_historial_asis = tk.LabelFrame(f_main, text=" 3. Resumen ", bg="white", padx=10, pady=10); self.col_historial_asis.pack(side="left", fill="both", expand=True, padx=5)

    def dibujar_lista_asistencia(self):
        for w in self.col_lista_asis.winfo_children(): w.destroy()
        self.vars_asis = {}
        for j in self.jugadores:
            f = tk.Frame(self.col_lista_asis, bg="white"); f.pack(fill="x", pady=2)
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
        conn.commit(); conn.close(); messagebox.showinfo("Éxito", "Asistencia guardada.")

    def dibujar_calendario_asis(self, nombre):
        for w in self.col_historial_asis.winfo_children(): w.destroy()
        tk.Label(self.col_historial_asis, text=f"Récord de {nombre}", bg="white", font=("bold")).pack()
        grid = tk.Frame(self.col_historial_asis, bg="white"); grid.pack()
        mes, ano = int(self.cb_mes.get()), int(self.cb_ano.get()); cal_matriz = calendar.monthcalendar(ano, mes)
        conn = self.conectar(); cursor = conn.cursor(); cursor.execute("SELECT fecha, estado FROM asistencia WHERE nombre=?", (nombre,)); datos = dict(cursor.fetchall()); conn.close()
        for r, sem in enumerate(cal_matriz):
            for c, dia in enumerate(sem):
                if dia == 0: continue
                f_key = f"{str(dia).zfill(2)}/{str(mes).zfill(2)}/{ano}"
                estado = datos.get(f_key, "N")
                color = "#EEE"
                if estado == "Asistio": color = "#28A745"
                elif estado == "Falto": color = "#DC3545"
                tk.Label(grid, text=str(dia), bg=color, width=3).grid(row=r, column=c, padx=1, pady=1)

    def seccion_stats_jugadores(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Estadísticas de Jugadores", font=("Helvetica", 20, "bold"), bg="#F4F7F6").pack(anchor="w", padx=20, pady=20)
        f_stats = tk.Frame(self.content, bg="#F4F7F6"); f_stats.pack(fill="both", expand=True, padx=20)
        f_edit = tk.LabelFrame(f_stats, text=" Editar ", bg="white", padx=15, pady=15); f_edit.pack(side="left", fill="y", padx=5)
        self.cb_j_stats = ttk.Combobox(f_edit, values=self.jugadores, state="readonly"); self.cb_j_stats.pack(fill="x")
        self.ent_g = tk.Entry(f_edit); self.ent_a = tk.Entry(f_edit); self.ent_p = tk.Entry(f_edit)
        for e, t in [(self.ent_g, "Goles:"), (self.ent_a, "Asist:"), (self.ent_p, "Part:")]:
            tk.Label(f_edit, text=t, bg="white").pack(anchor="w"); e.pack(fill="x", pady=2)
        tk.Button(f_edit, text="ACTUALIZAR DB", bg="#27AE60", fg="white", command=self.guardar_stats).pack(pady=20, fill="x")
        self.tree = ttk.Treeview(f_stats, columns=("Jugador", "Goles", "Asistencias", "Partidos"), show="headings")
        for c in self.tree["columns"]: self.tree.heading(c, text=c); self.tree.column(c, width=80)
        self.tree.pack(fill="both", expand=True); self.actualizar_tabla_stats()

    def actualizar_tabla_stats(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        conn = self.conectar(); cursor = conn.cursor(); cursor.execute("SELECT * FROM stats_jugadores"); [self.tree.insert("", "end", values=fila) for fila in cursor.fetchall()]; conn.close()

    def guardar_stats(self):
        j = self.cb_j_stats.get()
        if j:
            conn = self.conectar(); cursor = conn.cursor()
            cursor.execute("UPDATE stats_jugadores SET goles=?, asistencias=?, partidos=? WHERE nombre=?", (self.ent_g.get(), self.ent_a.get(), self.ent_p.get(), j))
            conn.commit(); conn.close(); self.actualizar_tabla_stats(); messagebox.showinfo("Ok", "Actualizado.")

    def seccion_stats_equipo(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Rendimiento del Club", font=("Helvetica", 22, "bold"), bg="#F4F7F6").pack(anchor="w", padx=30, pady=20)
        self.f_cards = tk.Frame(self.content, bg="#F4F7F6"); self.f_cards.pack(fill="x", padx=30)
        f_edit_club = tk.LabelFrame(self.content, text=" Actualizar Temporada ", bg="white", padx=20, pady=20); f_edit_club.pack(fill="x", padx=30, pady=20)
        self.inputs_club = {}
        campos = [("Jugados:", "jugados"), ("Ganados:", "ganados"), ("Empatados:", "empatados"), ("Perdidos:", "perdidos"), ("Favor:", "goles_favor"), ("Contra:", "goles_contra")]
        conn = self.conectar(); cursor = conn.cursor(); cursor.execute("SELECT * FROM stats_club WHERE id=1"); actuales = cursor.fetchone(); conn.close()
        for i, (label, key) in enumerate(campos):
            tk.Label(f_edit_club, text=label, bg="white").grid(row=i//2*2, column=i%2, sticky="w")
            ent = tk.Entry(f_edit_club); ent.insert(0, str(actuales[i+1]) if actuales else "0"); ent.grid(row=i//2*2+1, column=i%2, padx=10); self.inputs_club[key] = ent
        tk.Button(f_edit_club, text="GUARDAR BALANCE", bg="#27AE60", fg="white", command=self.actualizar_club_stats).grid(row=6, column=0, columnspan=2, pady=20)
        self.dibujar_tarjetas_equipo()

    def dibujar_tarjetas_equipo(self):
        for w in self.f_cards.winfo_children(): w.destroy()
        conn = self.conectar(); cursor = conn.cursor(); cursor.execute("SELECT * FROM stats_club WHERE id=1"); s = cursor.fetchone(); conn.close()
        titulos = ["PJ", "PG", "PE", "PP", "GF", "GC"]
        if s:
            for i in range(1, 7):
                card = tk.Frame(self.f_cards, bg="white", relief="groove", bd=2); card.pack(side="left", padx=5, expand=True, fill="both")
                tk.Label(card, text=titulos[i-1], bg="white", fg="gray").pack(); tk.Label(card, text=str(s[i]), font=("Arial", 18, "bold"), bg="white").pack()

    def actualizar_club_stats(self):
        conn = self.conectar(); cursor = conn.cursor()
        cursor.execute("UPDATE stats_club SET jugados=?, ganados=?, empatados=?, perdidos=?, goles_favor=?, goles_contra=? WHERE id=1", (self.inputs_club['jugados'].get(), self.inputs_club['ganados'].get(), self.inputs_club['empatados'].get(), self.inputs_club['perdidos'].get(), self.inputs_club['goles_favor'].get(), self.inputs_club['goles_contra'].get()))
        conn.commit(); conn.close(); self.dibujar_tarjetas_equipo(); messagebox.showinfo("Ok", "Balance actualizado.")

# =================================================================
# 3. CLASE PRINCIPAL (LOGIN Y REGISTRO ORIGINALES)
# =================================================================
class SystemProFutbol:
    def __init__(self, root):
        self.root = root
        self.root.title("FC BOGOTÁ - System Pro Futbol")
        self.root.geometry("1300x850")
        self.root.configure(bg="#0a0f0d")
        
        self.preparar_db()
        self.color_deep = "#0a1f1a"; self.color_neon = "#1db954"; self.color_azul_tech = "#112233"
        self.main_frame = tk.Frame(self.root, bg=self.color_deep)
        self.main_frame.pack(fill="both", expand=True)
        self.mostrar_login()

    def preparar_db(self):
        conn = sqlite3.connect("escuela_futbol.db")
        conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, rol TEXT, nombre TEXT, documento TEXT, fecha_nacimiento TEXT, email TEXT UNIQUE, password TEXT)''')
        conn.close()

    def limpiar_pantalla(self):
        for widget in self.main_frame.winfo_children(): widget.destroy()

    def mostrar_login(self):
        self.limpiar_pantalla()
        self.main_frame.configure(bg=self.color_deep)
        header = tk.Frame(self.main_frame, bg=self.color_deep); header.pack(pady=40)
        tk.Label(header, text="FC BOGOTÁ", font=("Orbitron", 40, "bold"), bg=self.color_deep, fg=self.color_neon).pack()
        
        card = tk.Frame(self.main_frame, bg=self.color_azul_tech, padx=30, pady=30); card.pack(pady=10)
        self.rol_var = tk.StringVar(value="Jugador")
        rf = tk.Frame(card, bg=self.color_azul_tech); rf.pack(pady=5)
        for r in ["Jugador", "Entrenador", "Admin"]:
            tk.Radiobutton(rf, text=r, variable=self.rol_var, value=r, bg=self.color_azul_tech, fg="white", selectcolor="#000").pack(side="left", padx=10)

        self.ent_email = self.crear_campo(card, "Correo electrónico")
        self.ent_pass = self.crear_campo(card, "Contraseña", secreto=True)
        tk.Button(card, text="ACCEDER AL CLUB", bg=self.color_neon, fg=self.color_deep, font=("Helvetica", 11, "bold"), command=self.login_action, width=35).pack(pady=30, ipady=12)
        btn = tk.Label(card, text="¿Aún no eres miembro? Regístrate aquí", bg=self.color_azul_tech, fg=self.color_neon, cursor="hand2", font=("Helvetica", 9, "underline"))
        btn.pack(); btn.bind("<Button-1>", lambda e: self.mostrar_registro())

    def mostrar_registro(self):
        self.limpiar_pantalla()
        header = tk.Frame(self.main_frame, bg=self.color_azul_tech, height=80); header.pack(fill="x")
        tk.Label(header, text="REGISTRO DE USUARIO", font=("Orbitron", 18), bg=self.color_azul_tech, fg="white").pack(pady=25)
        form = tk.Frame(self.main_frame, bg=self.color_deep); form.pack(pady=10)
        self.reg_nombre = self.crear_campo(form, "Nombre Completo")
        self.reg_documento = self.crear_campo(form, "Documento de Identidad")
        self.reg_fecha = self.crear_campo(form, "Fecha de Nacimiento")
        self.reg_email = self.crear_campo(form, "Correo Electrónico")
        self.reg_pass = self.crear_campo(form, "Crear Contraseña", secreto=True)
        self.terminos_var = tk.BooleanVar()
        cf = tk.Frame(form, bg=self.color_deep); cf.pack(pady=15)
        tk.Checkbutton(cf, variable=self.terminos_var, bg=self.color_deep).pack(side="left")
        tk.Label(cf, text="Acepto términos y Política de Datos", bg=self.color_deep, fg="#aaa").pack(side="left")
        tk.Button(form, text="REGISTRARSE", bg=self.color_neon, command=self.registro_action, width=35).pack(ipady=12)
        btn = tk.Label(form, text="← Volver", bg=self.color_deep, fg="#666", cursor="hand2"); btn.pack(pady=10)
        btn.bind("<Button-1>", lambda e: self.mostrar_login())

    def crear_campo(self, parent, texto, secreto=False):
        tk.Label(parent, text=texto.upper(), font=("Consolas", 8), bg=parent.cget("bg"), fg="#888").pack(anchor="w", padx=30, pady=(10,0))
        e = tk.Entry(parent, font=("Helvetica", 11), bg="#1e2a30", fg="white", bd=0, insertbackground="white")
        if secreto: e.config(show="*")
        e.pack(fill="x", padx=30, ipady=8); return e

    def login_action(self):
        e, p, r = self.ent_email.get(), self.ent_pass.get(), self.rol_var.get()
        conn = sqlite3.connect("escuela_futbol.db"); cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email=? AND password=? AND rol=?", (e, p, r))
        u = cur.fetchone(); conn.close()
        if u:
            if r == "Jugador": InterfazJugador(self.main_frame, u[2], self)
            elif r == "Entrenador": InterfazEntrenador(self.main_frame, u[2], self)
        else: messagebox.showerror("Error", "Credenciales incorrectas")

    def registro_action(self):
        if not self.terminos_var.get(): messagebox.showwarning("Aviso", "Acepte términos"); return
        datos = (self.rol_var.get(), self.reg_nombre.get(), self.reg_documento.get(), self.reg_fecha.get(), self.reg_email.get(), self.reg_pass.get())
        try:
            conn = sqlite3.connect("escuela_futbol.db"); cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (rol, nombre, documento, fecha_nacimiento, email, password) VALUES (?,?,?,?,?,?)", datos)
            conn.commit(); conn.close(); messagebox.showinfo("Ok", "Registrado"); self.mostrar_login()
        except: messagebox.showerror("Error", "El correo ya existe")

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemProFutbol(root)
    root.mainloop()