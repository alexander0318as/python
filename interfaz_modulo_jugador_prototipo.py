import tkinter as tk
from tkinter import ttk

class VentanaJugadorV4:
    def __init__(self, datos):
        self.root = tk.Tk()
        self.root.title("System Pro Futbol - FC BOGOTÁ")
        self.root.geometry("1100x800")
        
        # --- PALETA DE COLORES ---
        self.bg_principal = "#F8F9FA"
        self.bg_sidebar = "#FFFFFF"
        self.azul_fcb = "#00468C"
        self.verde_exito = "#28A745"
        self.rojo_alerta = "#DC3545"
        self.texto_p = "#212529"
        self.texto_s = "#6C757D"
        
        self.root.configure(bg=self.bg_principal)

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.bg_sidebar, width=260, highlightthickness=1, highlightbackground="#E9ECEF")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Contenido
        self.content = tk.Frame(self.root, bg=self.bg_principal, padx=40, pady=30)
        self.content.pack(side="right", fill="both", expand=True)

        self.setup_sidebar()
        self.seccion_inicio(datos)
        self.root.mainloop()

    def setup_sidebar(self):
        tk.Label(self.sidebar, text="FC BOGOTÁ", font=("Helvetica", 22, "bold"), bg=self.bg_sidebar, fg=self.azul_fcb).pack(pady=(40, 5))
        tk.Label(self.sidebar, text="PANEL JUGADOR", font=("Helvetica", 8, "bold"), bg=self.bg_sidebar, fg=self.texto_s).pack(pady=(0, 30))

        # Botones de navegación
        self.crear_btn("🏠 Inicio", lambda: self.seccion_inicio({"nombre": "xxxxxx xxxxxxx"}))
        self.crear_btn("📅 Mi Agenda", self.seccion_entrenamientos)
        
        tk.Label(self.sidebar, text="ESTADÍSTICAS", font=("Helvetica", 7, "bold"), bg=self.bg_sidebar, fg=self.texto_s).pack(anchor="w", padx=25, pady=(20, 5))
        self.crear_btn("👥 Del Equipo", self.seccion_stats_jugadores)
        self.crear_btn("⚽ De Partidos", self.seccion_stats_partidos)
        
        tk.Label(self.sidebar, text="PERSONAL", font=("Helvetica", 7, "bold"), bg=self.sidebar["bg"], fg=self.texto_s).pack(anchor="w", padx=25, pady=(20, 5))
        self.crear_btn("🏥 Salud y Estado", self.seccion_salud)
        self.crear_btn("💳 Pagos", self.seccion_pagos)
        
        tk.Button(self.sidebar, text="Cerrar Sesión", font=("Helvetica", 10), bg="#F8D7DA", fg="#842029", bd=0, command=self.root.destroy).pack(side="bottom", fill="x", pady=20, padx=20)

    def crear_btn(self, texto, comando):
        btn = tk.Button(self.sidebar, text=texto, font=("Helvetica", 10), bg=self.bg_sidebar, fg=self.texto_p,
                        bd=0, padx=30, pady=12, anchor="w", cursor="hand2", activebackground="#F1F3F5", command=comando)
        btn.pack(fill="x")

    def limpiar(self):
        for w in self.content.winfo_children(): w.destroy()

    def seccion_inicio(self, datos):
        self.limpiar()
        tk.Label(self.content, text=f"Bienvenido, {datos['nombre']}", font=("Helvetica", 26, "bold"), bg=self.bg_principal).pack(anchor="w")
        self.crear_card_info("TU PRÓXIMO RETO", "Sábado 22 Feb - 08:00 AM\nEstadio Campincito vs Santa Fe")

    # --- NUEVAS SECCIONES DE ESTADÍSTICAS ---
    def seccion_stats_jugadores(self):
        self.limpiar()
        tk.Label(self.content, text="Líderes de Plantilla", font=("Helvetica", 20, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        # Tabla de Rendimiento de Jugadores
        frame_tabla = tk.Frame(self.content, bg="white", bd=1, relief="flat")
        frame_tabla.pack(fill="both", expand=True)

        cols = ("Jugador", "Posición", "Goles", "Asistencias", "Calificación")
        tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=8)
        for c in cols: tabla.heading(c, text=c)
        
        jugadores = [
            ("M. Rodriguez", "Delantero", "12", "4", "9.2"),
            ("S. Castro", "Volante", "3", "8", "8.5"),
            ("J. Moreno", "Portero", "0", "0", "8.9")
        ]
        for j in jugadores: tabla.insert("", "end", values=j)
        tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def seccion_stats_partidos(self):
        self.limpiar()
        tk.Label(self.content, text="Historial de Partidos Temporada 2026", font=("Helvetica", 20, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        # Resumen visual
        res_f = tk.Frame(self.content, bg=self.bg_principal)
        res_f.pack(fill="x", pady=10)
        
        stats = [("PJ", "10", self.azul_fcb), ("PG", "7", self.verde_exito), ("PE", "2", "#FFC107"), ("PP", "1", self.rojo_alerta)]
        for i, (t, v, c) in enumerate(stats):
            f = tk.Frame(res_f, bg="white", padx=20, pady=10, highlightthickness=1, highlightbackground="#EEE")
            f.grid(row=0, column=i, padx=5)
            tk.Label(f, text=t, font=("Helvetica", 8, "bold"), bg="white", fg=self.texto_s).pack()
            tk.Label(f, text=v, font=("Helvetica", 14, "bold"), bg="white", fg=c).pack()

    # --- SECCIÓN SALUD ---
    def seccion_salud(self):
        self.limpiar()
        tk.Label(self.content, text="Mi Estado Físico y Salud", font=("Helvetica", 20, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        card = tk.Frame(self.content, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#EEE")
        card.pack(fill="x")
        
        tk.Label(card, text="ESTADO: APTO PARA COMPETIR ✅", font=("Helvetica", 12, "bold"), bg="white", fg=self.verde_exito).pack(anchor="w")
        
        detalles = [
            ("Altura:", "1.75 m"), ("Peso:", "68 kg"), 
            ("Última lesión:", "Ninguna"), ("Observaciones:", "Fortalecer rodilla derecha")
        ]
        for l, v in detalles:
            f = tk.Frame(card, bg="white")
            f.pack(fill="x", pady=5)
            tk.Label(f, text=l, font=("Helvetica", 10, "bold"), bg="white", width=15, anchor="w").pack(side="left")
            tk.Label(f, text=v, font=("Helvetica", 10), bg="white").pack(side="left")

    # --- SECCIÓN PAGOS ---
    def seccion_pagos(self):
        self.limpiar()
        tk.Label(self.content, text="Gestión de Mensualidades", font=("Helvetica", 20, "bold"), bg=self.bg_principal).pack(anchor="w", pady=(0,20))
        
        card = tk.Frame(self.content, bg="white", padx=25, pady=25)
        card.pack(fill="x")

        # Semáforo de pago
        tk.Label(card, text="ESTADO DE CUENTA: AL DÍA", font=("Helvetica", 14, "bold"), bg="white", fg=self.verde_exito).pack(anchor="w")
        tk.Label(card, text="Próximo vencimiento: 05 de Marzo, 2026", bg="white", fg=self.texto_s).pack(anchor="w", pady=(0, 20))

        # Historial simple
        tk.Label(card, text="HISTORIAL RECIENTE", font=("Helvetica", 8, "bold"), bg="white").pack(anchor="w")
        for mes in ["Enero - Pagado ($150.000)", "Febrero - Pagado ($150.000)"]:
            tk.Label(card, text=f"• {mes}", bg="white", fg="#444").pack(anchor="w", pady=2)

    def seccion_entrenamientos(self):
        self.limpiar()
        tk.Label(self.content, text="Mi Agenda de Trabajo", font=("Helvetica", 20, "bold"), bg=self.bg_principal).pack(anchor="w")
        # Aquí iría la tabla de entrenamientos que ya conocemos

    def crear_card_info(self, titulo, texto):
        f = tk.Frame(self.content, bg="white", padx=20, pady=20, highlightthickness=1, highlightbackground="#EEE")
        f.pack(fill="x", pady=20)
        tk.Label(f, text=titulo, font=("Helvetica", 8, "bold"), bg="white", fg=self.azul_fcb).pack(anchor="w")
        tk.Label(f, text=texto, font=("Helvetica", 12), bg="white").pack(anchor="w", pady=10)

if __name__ == "__main__":
    VentanaJugadorV4({"nombre": "xxxxxx xxxxxxx"})