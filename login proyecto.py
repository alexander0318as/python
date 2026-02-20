import tkinter as tk
from tkinter import messagebox
import re

class SystemProFutbol:
    def __init__(self, root):
        self.root = root
        self.root.title("FC BOGOTÁ - System Pro Futbol")
        self.root.geometry("500x780")
        self.root.configure(bg="#0a0f0d") # Fondo casi negro para resaltar el verde tech
        self.root.resizable(False, False)
        
        # --- PALETA DE COLORES TECH ---
        self.color_deep = "#0a1f1a"    # Verde bosque muy profundo
        self.color_neon = "#1db954"    # Verde tech (estilo Spotify/Digital)
        self.color_azul_tech = "#112233" # Azul medianoche
        self.color_texto = "#e0e0e0"
        
        self.main_frame = tk.Frame(self.root, bg=self.color_deep)
        self.main_frame.pack(fill="both", expand=True)

        self.mostrar_login()

    def limpiar_pantalla(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_pantalla()
        
        # --- HEADER TECH ---
        header = tk.Frame(self.main_frame, bg=self.color_deep, height=220)
        header.pack(fill="x")
        
        # Efecto de "Glow" o brillo en el título
        tk.Label(header, text="FC BOGOTÁ", font=("Orbitron", 40, "bold"), 
                 bg=self.color_deep, fg=self.color_neon).pack(pady=(50, 0))
        tk.Label(header, text="SYSTEM PRO FUTBOL", font=("Consolas", 10), 
                 bg=self.color_deep, fg="#666").pack()

        # --- TARJETA FLOTANTE (Efecto Glassmorphism) ---
        card = tk.Frame(self.main_frame, bg=self.color_azul_tech, padx=20, pady=20)
        card.pack(pady=10, padx=40, fill="both", expand=True)

        tk.Label(card, text="SELECIONE SU ROL", font=("Helvetica", 9, "bold"), 
                 bg=self.color_azul_tech, fg=self.color_neon).pack(pady=(0, 20))

        # Selector de Rol Moderno
        self.rol_var = tk.StringVar(value="Jugador")
        rol_frame = tk.Frame(card, bg=self.color_azul_tech)
        rol_frame.pack(pady=5)
        for r in ["Jugador", "Entrenador", "Admin"]:
            tk.Radiobutton(rol_frame, text=r, variable=self.rol_var, value=r, 
                           bg=self.color_azul_tech, fg="white", selectcolor=self.color_deep,
                           activebackground=self.color_neon, font=("Helvetica", 9)).pack(side="left", padx=10)

        self.ent_email = self.crear_campo(card, "Correo electronico")
        self.ent_pass = self.crear_campo(card, "Contraseña", secreto=True)

        # Botón de Inicio Tech
        btn_login = tk.Button(card, text="ACCEDER AL CLUB", bg=self.color_neon, fg=self.color_deep, 
                              font=("Helvetica", 11, "bold"), command=self.login_action, 
                              bd=0, cursor="hand2", activebackground="#1ed760")
        btn_login.pack(fill="x", padx=20, pady=30, ipady=12)

        # Registro link
        btn_reg = tk.Label(card, text="¿Aún no eres miembro? Registrate aquí", bg=self.color_azul_tech, 
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

        self.reg_nombre = self.crear_campo(form, "Nombre Completo del Jugador")
        self.reg_documento = self.crear_campo(form, "Documento de Identidad")
        self.reg_fecha = self.crear_campo(form, "Fecha de Nacimiento")
        self.reg_email = self.crear_campo(form, "Correo del Jugador")
        self.reg_pass = self.crear_campo(form, "Crear Contraseña", secreto=True)

        # Términos y Condiciones
        self.terminos_var = tk.BooleanVar()
        check_frame = tk.Frame(form, bg=self.color_deep)
        check_frame.pack(fill="x", padx=30, pady=15)
        
        tk.Checkbutton(check_frame, variable=self.terminos_var, bg=self.color_deep, 
                       activebackground=self.color_deep, selectcolor="#333").pack(side="left")
        
        tk.Label(check_frame, text="Acepto términos y Política de Datos (Ley 1581)", 
                 bg=self.color_deep, fg="#aaa", font=("Helvetica", 8)).pack(side="left")

        # Botón Registro
        tk.Button(form, text="REGISTRAR JUGADOR", bg=self.color_neon, fg=self.color_deep, 
                  font=("Helvetica", 11, "bold"), command=self.registro_action, 
                  bd=0, cursor="hand2").pack(fill="x", padx=30, pady=10, ipady=12)

        btn_back = tk.Label(form, text="← Volver", bg=self.color_deep, fg="#666", cursor="hand2")
        btn_back.pack()
        btn_back.bind("<Button-1>", lambda e: self.mostrar_login())

    def crear_campo(self, parent, texto, secreto=False):
        tk.Label(parent, text=texto.upper(), font=("Consolas", 8), bg=parent.cget("bg"), fg="#888").pack(anchor="w", padx=30, pady=(10,0))
        # Entry con estilo moderno (bordes oscuros)
        entry = tk.Entry(parent, font=("Helvetica", 11), bg="#1e2a30", fg="white", 
                         insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333")
        if secreto: entry.config(show="*")
        entry.pack(fill="x", padx=30, ipady=8)
        return entry

    def login_action(self):
        messagebox.showinfo("System Pro Futbol", "Iniciando protocolos de acceso...")

    def registro_action(self):
        if not self.terminos_var.get():
            messagebox.showwarning("Aviso Legal", "Debe aceptar el manejo de datos personales.")
            return
        
        if not self.reg_nombre.get() or not self.reg_email.get():
            messagebox.showwarning("Campos vacíos", "Por favor llene los datos obligatorios.")
            return
            
        messagebox.showinfo("Registro Exitoso", "Datos enviados al servidor de FC BOGOTÁ.")
        self.mostrar_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemProFutbol(root)
    root.mainloop()