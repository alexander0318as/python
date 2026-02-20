import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class InterfazJugadorSolo:
    def __init__(self, nombre_jugador="Santiago Castro"):
        self.root = tk.Tk()
        self.root.title("System Pro Futbol - Dashboard del Jugador")
        self.root.geometry("1200x850")
        
        # --- PALETA DE COLORES (MODERN LIGHT) ---
        self.bg_principal = "#F0F2F5"      # Gris claro de fondo
        self.bg_sidebar = "#FFFFFF"        # Blanco puro lateral
        self.azul_fcb = "#00468C"          # Azul institucional
        self.verde_exito = "#28A745"       # Verde indicadores
        self.rojo_error = "#DC3545"        # Rojo alertas
        self.texto_p = "#1C1E21"           # Texto oscuro
        self.texto_s = "#606770"           # Texto gris
        
        self.root.configure(bg=self.bg_principal)
        self.nombre_jugador = nombre_jugador

        # Contenedor de la Barra Lateral
        self.sidebar = tk.Frame(self.root, bg=self.bg_sidebar, width=260, highlightthickness=1, highlightbackground="#E9ECEF")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Contenedor de Contenido Dinámico
        self.content = tk.Frame(self.root, bg=self.bg_principal, padx=40, pady=20)
        self.content.pack(side="right", fill="both", expand=True)

        self.setup_sidebar()
        self.seccion_inicio()
        self.actualizar_reloj() # Iniciar contador
        
        self.root.mainloop()

    def setup_sidebar(self):
        # Logo y Título
        tk.Label(self.sidebar, text="FC BOGOTÁ", font=("Helvetica", 24, "bold"), bg=self.bg_sidebar, fg=self.azul_fcb).pack(pady=(40, 5))
        tk.Label(self.sidebar, text="PERFIL DEL DEPORTISTA", font=("Helvetica", 8, "bold"), bg=self.bg_sidebar, fg=self.texto_s).pack(pady=(0, 40))

        # Botones de Navegación
        self.crear_boton_menu("🏠 Inicio", self.seccion_inicio)
        self.crear_boton_menu("📅 Mi Asistencia", self.seccion_asistencia)
        self.crear_boton_menu("📋 Convocatoria", self.seccion_convocatoria)
        
        tk.Label(self.sidebar, text="RENDIMIENTO", font=("Helvetica", 7, "bold"), bg=self.bg_sidebar, fg=self.texto_s).pack(anchor="w", padx=25, pady=(20, 5))
        self.crear_boton_menu("👥 Stats del Equipo", self.seccion_stats_jugadores)
        self.crear_boton_menu("⚽ Stats de Partidos", self.seccion_stats_partidos)
        
        tk.Label(self.sidebar, text="PERSONAL", font=("Helvetica", 7, "bold"), bg=self.bg_sidebar, fg=self.texto_s).pack(anchor="w", padx=25, pady=(20, 5))
        self.crear_boton_menu("🏥 Salud y Estado", self.seccion_salud)
        self.crear_boton_menu("💳 Gestión de Pagos", self.seccion_pagos)

        # Botón de salida decorativo
        tk.Button(self.sidebar, text="Cerrar Sesión", font=("Helvetica", 10), bg="#F8D7DA", fg="#842029", bd=0, pady=8, command=self.root.destroy).pack(side="bottom", fill="x", pady=20, padx=20)

    def crear_boton_menu(self, texto, comando):
        btn = tk.Button(self.sidebar, text=texto, font=("Helvetica", 11), bg=self.bg_sidebar, fg=self.texto_p,
                        bd=0, padx=30, pady=12, anchor="w", cursor="hand2", activebackground="#F1F3F5", command=comando)
        btn.pack(fill="x")

    def limpiar_pantalla(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def actualizar_reloj(self):
        ahora = datetime.now()
        # Simulamos próximo entreno mañana a las 4 PM
        proximo = ahora.replace(hour=16, minute=0, second=0, microsecond=0) + timedelta(days=1)
        diff = proximo - ahora
        h, rem = divmod(diff.seconds, 3600)
        m, s = divmod(rem, 60)
        if hasattr(self, 'label_reloj'):
            self.label_reloj.config(text=f"{h:02d}h {m:02d}m {s:02d}s")
        self.root.after(1000, self.actualizar_reloj)

    # --- VISTAS DEL JUGADOR ---

    def seccion_inicio(self):
        self.limpiar_pantalla()
        header = tk.Frame(self.content, bg=self.bg_principal)
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text=f"Hola, {self.nombre_jugador} 👋", font=("Helvetica", 28, "bold"), bg=self.bg_principal).pack(side="left")
        
        # Widget de Reloj
        reloj_f = tk.Frame(header, bg=self.azul_fcb, padx=15, pady=5)
        reloj_f.pack(side="right")
        tk.Label(reloj_f, text="PRÓXIMO EVENTO EN:", font=("Helvetica", 8, "bold"), bg=self.azul_fcb, fg="white").pack()
        self.label_reloj = tk.Label(reloj_f, text="--h --m --s", font=("Consolas", 12, "bold"), bg=self.azul_fcb, fg=self.verde_exito)
        self.label_reloj.pack()

        # Resumen rápido (Convocatoria)
        self.seccion_convocatoria(incrustada=True)

    def seccion_asistencia(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Mi Disciplina (Asistencia)", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        grid_f = tk.Frame(self.content, bg="white", padx=25, pady=25, highlightthickness=1, highlightbackground="#EEE")
        grid_f.pack(fill="x")

        # Cabecera de días
        dias = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
        for i, d in enumerate(dias):
            tk.Label(grid_f, text=d, bg="white", font=("Helvetica", 10, "bold"), fg=self.texto_s).grid(row=0, column=i, padx=15, pady=10)

        # Generar cuadrícula de ejemplo
        asistencias = [2, 4, 6, 9, 11, 13, 16, 18, 20]
        for i in range(1, 29):
            bg = self.verde_exito if i in asistencias else "#F8F9FA"
            fg = "white" if i in asistencias else "#CCC"
            lbl = tk.Label(grid_f, text=str(i), bg=bg, fg=fg, width=4, height=2, font=("Helvetica", 10, "bold"))
            lbl.grid(row=(i-1)//7 + 1, column=(i-1)%7, padx=4, pady=4)

    def seccion_convocatoria(self, incrustada=False):
        if not incrustada: self.limpiar_pantalla()
        tk.Label(self.content, text="Estado de Convocatoria", font=("Helvetica", 18, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(20,10))
        
        card = tk.Frame(self.content, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#EEE")
        card.pack(fill="x")
        
        tk.Canvas(card, width=15, height=15, bg=self.verde_exito, highlightthickness=0).pack(side="left", padx=(0,15))
        tk.Label(card, text="CONVOCADO - TITULAR ✅", font=("Helvetica", 15, "bold"), bg="white", fg=self.verde_exito).pack(side="left")
        tk.Label(card, text="Vs Millonarios FC | Domingo 10:00 AM | Cancha Salitre 3", font=("Helvetica", 10), bg="white", fg=self.texto_s).pack(side="right")

    def seccion_stats_jugadores(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Rendimiento del Equipo", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        cols = ("Jugador", "Posición", "Goles", "Asistencias", "Calificación")
        tabla = ttk.Treeview(self.content, columns=cols, show="headings", height=10)
        for c in cols: tabla.heading(c, text=c)
        
        jugadores = [("M. Rodriguez", "Delantero", "12", "4", "9.2"), ("S. Castro", "Volante", "3", "8", "8.5"), ("A. Villa", "Defensa", "1", "2", "7.9")]
        for j in jugadores: tabla.insert("", "end", values=j)
        tabla.pack(fill="both", expand=True)

    def seccion_stats_partidos(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Balance de la Temporada", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        frame_cards = tk.Frame(self.content, bg=self.bg_principal)
        frame_cards.pack(fill="x")
        
        stats = [("PJ", "12", self.azul_fcb), ("PG", "9", self.verde_exito), ("PE", "2", "#FFC107"), ("PP", "1", self.rojo_error)]
        for i, (tit, val, col) in enumerate(stats):
            c = tk.Frame(frame_cards, bg="white", padx=35, pady=20, highlightthickness=1, highlightbackground="#EEE")
            c.grid(row=0, column=i, padx=5)
            tk.Label(c, text=tit, font=("Helvetica", 8, "bold"), bg="white", fg=self.texto_s).pack()
            tk.Label(c, text=val, font=("Helvetica", 20, "bold"), bg="white", fg=col).pack()

    def seccion_salud(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Mi Perfil Médico", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        card = tk.Frame(self.content, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#EEE")
        card.pack(fill="x")
        
        tk.Label(card, text="ESTADO: APTO PARA COMPETIR ✅", font=("Helvetica", 14, "bold"), bg="white", fg=self.verde_exito).pack(anchor="w")
        tk.Label(card, text="\nAltura: 1.78m  |  Peso: 69kg  |  IMC: 21.8\nObservaciones: Jugador en óptimas condiciones físicas.", font=("Helvetica", 11), bg="white", justify="left").pack(anchor="w")

    def seccion_pagos(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Gestión Financiera", font=("Helvetica", 22, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        card = tk.Frame(self.content, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#EEE")
        card.pack(fill="x")
        
        tk.Label(card, text="MENSUALIDAD: AL DÍA", font=("Helvetica", 14, "bold"), bg="white", fg=self.verde_exito).pack(anchor="w")
        tk.Label(card, text="\nÚltimo pago recibido: 05 Feb 2026\nPróximo vencimiento: 05 Mar 2026", font=("Helvetica", 11), bg="white", justify="left").pack(anchor="w")

if __name__ == "__main__":
    InterfazJugadorSolo()