import tkinter as tk
from tkinter import messagebox
import re
import sqlite3

class SystemProFutbol:
    def __init__(self, root):
        self.root = root
        self.root.title("FC BOGOTÁ - System Pro Futbol")
        self.root.geometry("500x780")
        self.root.configure(bg="#0a0f0d")
        self.root.resizable(False, False)
        
        # Inicializar Base de Datos
        self.preparar_db()
        
        # --- PALETA DE COLORES TECH ---
        self.color_deep = "#0a1f1a"
        self.color_neon = "#1db954"
        self.color_azul_tech = "#112233"
        
        self.main_frame = tk.Frame(self.root, bg=self.color_deep)
        self.main_frame.pack(fill="both", expand=True)

        self.mostrar_login()

    def preparar_db(self):
        """Crea la base de datos y la tabla si no existen"""
        conexion = sqlite3.connect("escuela_futbol.db")
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rol TEXT,
                nombre TEXT,
                documento TEXT,
                fecha_nacimiento TEXT,
                email TEXT UNIQUE,
                password TEXT
            )
        ''')
        conexion.commit()
        conexion.close()

    def limpiar_pantalla(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_pantalla()
        
        header = tk.Frame(self.main_frame, bg=self.color_deep, height=220)
        header.pack(fill="x")
        
        tk.Label(header, text="FC BOGOTÁ", font=("Orbitron", 40, "bold"), 
                 bg=self.color_deep, fg=self.color_neon).pack(pady=(50, 0))
        tk.Label(header, text="SYSTEM PRO FUTBOL", font=("Consolas", 10), 
                 bg=self.color_deep, fg="#666").pack()

        card = tk.Frame(self.main_frame, bg=self.color_azul_tech, padx=20, pady=20)
        card.pack(pady=10, padx=40, fill="both", expand=True)

        tk.Label(card, text="SELECCIONE SU ROL", font=("Helvetica", 9, "bold"), 
                 bg=self.color_azul_tech, fg=self.color_neon).pack(pady=(0, 20))

        self.rol_var = tk.StringVar(value="Jugador")
        rol_frame = tk.Frame(card, bg=self.color_azul_tech)
        rol_frame.pack(pady=5)
        for r in ["Jugador", "Entrenador", "Admin"]:
            tk.Radiobutton(rol_frame, text=r, variable=self.rol_var, value=r, 
                           bg=self.color_azul_tech, fg="white", selectcolor=self.color_deep,
                           activebackground=self.color_neon, font=("Helvetica", 9)).pack(side="left", padx=10)

        self.ent_email = self.crear_campo(card, "Correo electrónico")
        self.ent_pass = self.crear_campo(card, "Contraseña", secreto=True)

        btn_login = tk.Button(card, text="ACCEDER AL CLUB", bg=self.color_neon, fg=self.color_deep, 
                              font=("Helvetica", 11, "bold"), command=self.login_action, 
                              bd=0, cursor="hand2", activebackground="#1ed760")
        btn_login.pack(fill="x", padx=20, pady=30, ipady=12)

        btn_reg = tk.Label(card, text="¿Aún no eres miembro? Regístrate aquí", bg=self.color_azul_tech, 
                           fg=self.color_neon, font=("Helvetica", 9, "underline"), cursor="hand2")
        btn_reg.pack()
        btn_reg.bind("<Button-1>", lambda e: self.mostrar_registro())

    def mostrar_registro(self):
        self.limpiar_pantalla()
        
        header = tk.Frame(self.main_frame, bg=self.color_azul_tech, height=80)
        header.pack(fill="x")
        tk.Label(header, text="REGISTRO DE USUARIO", font=("Orbitron", 18), 
                 bg=self.color_azul_tech, fg="white").pack(pady=25)

        form = tk.Frame(self.main_frame, bg=self.color_deep)
        form.pack(pady=10, padx=40, fill="both", expand=True)

        self.reg_nombre = self.crear_campo(form, "Nombre Completo")
        self.reg_documento = self.crear_campo(form, "Documento de Identidad")
        self.reg_fecha = self.crear_campo(form, "Fecha de Nacimiento")
        self.reg_email = self.crear_campo(form, "Correo Electrónico")
        self.reg_pass = self.crear_campo(form, "Crear Contraseña", secreto=True)

        self.terminos_var = tk.BooleanVar()
        check_frame = tk.Frame(form, bg=self.color_deep)
        check_frame.pack(fill="x", padx=30, pady=15)
        tk.Checkbutton(check_frame, variable=self.terminos_var, bg=self.color_deep, 
                       activebackground=self.color_deep, selectcolor="#333").pack(side="left")
        tk.Label(check_frame, text="Acepto términos y Política de Datos", 
                 bg=self.color_deep, fg="#aaa", font=("Helvetica", 8)).pack(side="left")

        tk.Button(form, text="REGISTRARSE", bg=self.color_neon, fg=self.color_deep, 
                  font=("Helvetica", 11, "bold"), command=self.registro_action, 
                  bd=0, cursor="hand2").pack(fill="x", padx=30, pady=10, ipady=12)

        btn_back = tk.Label(form, text="← Volver", bg=self.color_deep, fg="#666", cursor="hand2")
        btn_back.pack()
        btn_back.bind("<Button-1>", lambda e: self.mostrar_login())

    def crear_campo(self, parent, texto, secreto=False):
        tk.Label(parent, text=texto.upper(), font=("Consolas", 8), bg=parent.cget("bg"), fg="#888").pack(anchor="w", padx=30, pady=(10,0))
        entry = tk.Entry(parent, font=("Helvetica", 11), bg="#1e2a30", fg="white", 
                         insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333")
        if secreto: entry.config(show="*")
        entry.pack(fill="x", padx=30, ipady=8)
        return entry

    def login_action(self):
        email = self.ent_email.get()
        password = self.ent_pass.get()
        rol_seleccionado = self.rol_var.get()

        if not email or not password:
            messagebox.showwarning("Atención", "Completa todos los campos.")
            return

        # Consulta a la DB
        conexion = sqlite3.connect("escuela_futbol.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=? AND password=? AND rol=?", 
                       (email, password, rol_seleccionado))
        usuario = cursor.fetchone()
        conexion.close()

        if usuario:
            messagebox.showinfo("Éxito", f"Bienvenido {usuario[2]} ({rol_seleccionado})")
            # Aquí lanzarías el Dashboard
        else:
            messagebox.showerror("Error", "Credenciales incorrectas o rol no coincide.")

    def registro_action(self):
        if not self.terminos_var.get():
            messagebox.showwarning("Aviso Legal", "Debe aceptar el manejo de datos personales.")
            return
        
        datos = (
            self.rol_var.get(),
            self.reg_nombre.get(),
            self.reg_documento.get(),
            self.reg_fecha.get(),
            self.reg_email.get(),
            self.reg_pass.get()
        )

        if not all(datos[1:]): # Verifica que no haya campos vacíos (excepto rol)
            messagebox.showwarning("Campos vacíos", "Por favor llene todos los datos.")
            return

        try:
            conexion = sqlite3.connect("escuela_futbol.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (rol, nombre, documento, fecha_nacimiento, email, password) VALUES (?,?,?,?,?,?)", datos)
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Registro Exitoso", "Usuario guardado en la base de datos de FC BOGOTÁ.")
            self.mostrar_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Este correo ya está registrado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemProFutbol(root)
    root.mainloop()