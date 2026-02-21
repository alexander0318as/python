import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime, timedelta

# --- CLASE DE LA INTERFAZ DEL JUGADOR (DASHBOARD) ---
class InterfazJugador:
    def __init__(self, container, nombre_jugador, app_instance):
        self.container = container 
        self.nombre_jugador = nombre_jugador
        self.app = app_instance # Referencia para volver al login
        
        # Paleta Modern Light
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
        for widget in self.container.winfo_children():
            widget.destroy()
        
        self.sidebar = tk.Frame(self.container, bg=self.bg_sidebar, width=260, highlightthickness=1, highlightbackground="#E9ECEF")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self.container, bg=self.bg_principal, padx=40, pady=20)
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
        
        tk.Button(self.sidebar, text="Cerrar Sesión", font=("Helvetica", 10), bg="#F8D7DA", fg="#842029", bd=0, pady=8, 
                  command=self.app.mostrar_login).pack(side="bottom", fill="x", pady=20, padx=20)

    def crear_boton_menu(self, texto, comando):
        btn = tk.Button(self.sidebar, text=texto, font=("Helvetica", 11), bg=self.bg_sidebar, fg=self.texto_p,
                        bd=0, padx=30, pady=12, anchor="w", cursor="hand2", activebackground="#F1F3F5", command=comando)
        btn.pack(fill="x")

    def limpiar_pantalla(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def actualizar_reloj(self):
        ahora = datetime.now()
        proximo = ahora.replace(hour=16, minute=0, second=0, microsecond=0) + timedelta(days=1)
        diff = proximo - ahora
        h, rem = divmod(diff.seconds, 3600)
        m, s = divmod(rem, 60)
        if hasattr(self, 'label_reloj') and self.label_reloj.winfo_exists():
            self.label_reloj.config(text=f"{h:02d}h {m:02d}m {s:02d}s")
            self.container.after(1000, self.actualizar_reloj)

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

# --- CLASE PRINCIPAL ---
class SystemProFutbol:
    def __init__(self, root):
        self.root = root
        self.root.title("FC BOGOTÁ - System Pro Futbol")
        self.root.geometry("1200x850") # Tamaño optimizado para el dashboard
        self.root.configure(bg="#0a0f0d")
        
        self.preparar_db()
        
        # Colores Tech
        self.color_deep = "#0a1f1a"
        self.color_neon = "#1db954"
        self.color_azul_tech = "#112233"
        
        self.main_frame = tk.Frame(self.root, bg=self.color_deep)
        self.main_frame.pack(fill="both", expand=True)

        self.mostrar_login()

    def preparar_db(self):
        conexion = sqlite3.connect("escuela_futbol.db")
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, rol TEXT, nombre TEXT, 
                        documento TEXT, fecha_nacimiento TEXT, email TEXT UNIQUE, password TEXT)''')
        conexion.commit()
        conexion.close()

    def limpiar_pantalla(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_pantalla()
        self.main_frame.configure(bg=self.color_deep)
        
        header = tk.Frame(self.main_frame, bg=self.color_deep, height=220)
        header.pack(fill="x")
        tk.Label(header, text="FC BOGOTÁ", font=("Orbitron", 40, "bold"), bg=self.color_deep, fg=self.color_neon).pack(pady=(50, 0))
        tk.Label(header, text="SYSTEM PRO FUTBOL", font=("Consolas", 10), bg=self.color_deep, fg="#666").pack()

        card = tk.Frame(self.main_frame, bg=self.color_azul_tech, padx=20, pady=20)
        card.pack(pady=10, padx=40, fill="y")

        tk.Label(card, text="SELECCIONE SU ROL", font=("Helvetica", 9, "bold"), bg=self.color_azul_tech, fg=self.color_neon).pack(pady=(0, 20))

        self.rol_var = tk.StringVar(value="Jugador")
        rol_frame = tk.Frame(card, bg=self.color_azul_tech)
        rol_frame.pack(pady=5)
        for r in ["Jugador", "Entrenador", "Admin"]:
            tk.Radiobutton(rol_frame, text=r, variable=self.rol_var, value=r, 
                           bg=self.color_azul_tech, fg="white", selectcolor=self.color_deep).pack(side="left", padx=10)

        self.ent_email = self.crear_campo(card, "Correo electrónico")
        self.ent_pass = self.crear_campo(card, "Contraseña", secreto=True)

        tk.Button(card, text="ACCEDER AL CLUB", bg=self.color_neon, fg=self.color_deep, 
                  font=("Helvetica", 11, "bold"), command=self.login_action, 
                  bd=0, cursor="hand2", width=35).pack(pady=30, ipady=12)

        btn_reg = tk.Label(card, text="¿Aún no eres miembro? Regístrate aquí", bg=self.color_azul_tech, 
                           fg=self.color_neon, font=("Helvetica", 9, "underline"), cursor="hand2")
        btn_reg.pack()
        btn_reg.bind("<Button-1>", lambda e: self.mostrar_registro())

    def mostrar_registro(self):
        self.limpiar_pantalla()
        self.main_frame.configure(bg=self.color_deep)
        
        header = tk.Frame(self.main_frame, bg=self.color_azul_tech, height=80)
        header.pack(fill="x")
        tk.Label(header, text="REGISTRO DE USUARIO", font=("Orbitron", 18), bg=self.color_azul_tech, fg="white").pack(pady=25)

        form = tk.Frame(self.main_frame, bg=self.color_deep)
        form.pack(pady=10, padx=40, fill="both", expand=True)

        # CAMPOS ORIGINALES
        self.reg_nombre = self.crear_campo(form, "Nombre Completo")
        self.reg_documento = self.crear_campo(form, "Documento de Identidad")
        self.reg_fecha = self.crear_campo(form, "Fecha de Nacimiento")
        self.reg_email = self.crear_campo(form, "Correo Electrónico")
        self.reg_pass = self.crear_campo(form, "Crear Contraseña", secreto=True)

        self.terminos_var = tk.BooleanVar()
        check_frame = tk.Frame(form, bg=self.color_deep)
        check_frame.pack(fill="x", padx=30, pady=15)
        tk.Checkbutton(check_frame, variable=self.terminos_var, bg=self.color_deep, selectcolor="#333").pack(side="left")
        tk.Label(check_frame, text="Acepto términos y Política de Datos", bg=self.color_deep, fg="#aaa", font=("Helvetica", 8)).pack(side="left")

        tk.Button(form, text="REGISTRARSE", bg=self.color_neon, fg=self.color_deep, 
                  font=("Helvetica", 11, "bold"), command=self.registro_action, bd=0, cursor="hand2").pack(fill="x", padx=30, pady=10, ipady=12)

        btn_back = tk.Label(form, text="← Volver", bg=self.color_deep, fg="#666", cursor="hand2")
        btn_back.pack()
        btn_back.bind("<Button-1>", lambda e: self.mostrar_login())

    def crear_campo(self, parent, texto, secreto=False):
        tk.Label(parent, text=texto.upper(), font=("Consolas", 8), bg=parent.cget("bg"), fg="#888").pack(anchor="w", padx=30, pady=(10,0))
        entry = tk.Entry(parent, font=("Helvetica", 11), bg="#1e2a30", fg="white", bd=0, insertbackground="white")
        if secreto: entry.config(show="*")
        entry.pack(fill="x", padx=30, ipady=8)
        return entry

    def login_action(self):
        email = self.ent_email.get()
        password = self.ent_pass.get()
        rol_sel = self.rol_var.get()

        conexion = sqlite3.connect("escuela_futbol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND password=? AND rol=?", (email, password, rol_sel))
        usuario = cursor.fetchone()
        conexion.close()

        if usuario:
            if rol_sel == "Jugador":
                InterfazJugador(self.main_frame, usuario[2], self) # Lanza el dashboard
            else:
                messagebox.showinfo("Acceso", f"Bienvenido {usuario[2]}. Panel en desarrollo.")
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def registro_action(self):
        if not self.terminos_var.get():
            messagebox.showwarning("Aviso Legal", "Debe aceptar el manejo de datos personales.")
            return
        
        datos = (self.rol_var.get(), self.reg_nombre.get(), self.reg_documento.get(), 
                 self.reg_fecha.get(), self.reg_email.get(), self.reg_pass.get())

        if not all(datos[1:]):
            messagebox.showwarning("Campos vacíos", "Por favor llene todos los datos.")
            return

        try:
            conexion = sqlite3.connect("escuela_futbol.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (rol, nombre, documento, fecha_nacimiento, email, password) VALUES (?,?,?,?,?,?)", datos)
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.mostrar_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El correo ya existe.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemProFutbol(root)
    root.mainloop()