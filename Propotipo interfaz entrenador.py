import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar

class SistemaEntrenadorIntegrado:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FC BOGOTÁ - Panel del Cuerpo Técnico")
        self.root.geometry("1300x850")
        self.root.configure(bg="#F4F7F6")

        # --- BASE DE DATOS TEMPORAL ---
        self.jugadores = ["Mateo Rodriguez", "Santiago Castro", "Andrés Villa", "Luis Díaz"]
        
        self.registro_asistencia = {
            "Mateo Rodriguez": {"15/02/2026": "Asistio", "16/02/2026": "Asistio"},
            "Santiago Castro": {"15/02/2026": "Falto"}
        }
        
        self.jugadores_stats = {
            "Mateo Rodriguez": {"goles": 12, "asistencias": 5, "partidos": 10},
            "Santiago Castro": {"goles": 0, "asistencias": 1, "partidos": 12},
            "Andrés Villa": {"goles": 2, "asistencias": 0, "partidos": 11},
            "Luis Díaz": {"goles": 8, "asistencias": 7, "partidos": 9}
        }

        # --- NUEVOS DATOS: ESTADÍSTICAS DEL CLUB ---
        self.club_stats = {
            "jugados": 15,
            "ganados": 10,
            "empatados": 2,
            "perdidos": 3,
            "goles_favor": 35,
            "goles_contra": 12
        }

        self.setup_main_layout()
        self.seccion_bienvenida() 
        self.root.mainloop()

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
            ("🏆 Stats Equipo", self.seccion_stats_equipo),
            ("📋 Pizarra Táctica", lambda: messagebox.showinfo("Próximamente", "Módulo de Pizarra en desarrollo..."))
        ]

        for texto, comando in opciones:
            tk.Button(self.sidebar, text=texto, font=("Helvetica", 11, "bold"), bg="#1A252F", fg="white", 
                      bd=0, padx=20, pady=15, anchor="w", cursor="hand2", 
                      activebackground="#2C3E50", command=comando).pack(fill="x")

    def limpiar_pantalla(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def seccion_bienvenida(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Bienvenido, Entrenador", font=("Helvetica", 24, "bold"), bg="#F4F7F6", fg="#1A252F").pack(pady=100)
        tk.Label(self.content, text="Seleccione una opción a la izquierda para gestionar el club.", font=("Helvetica", 12), bg="#F4F7F6", fg="gray").pack()

    # =================================================================
    # MÓDULO 1: ASISTENCIA (CORREGIDO 'IN')
    # =================================================================
    def seccion_asistencia(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Gestión de Asistencia", font=("Helvetica", 20, "bold"), bg="#F4F7F6").pack(anchor="w", padx=20, pady=20)
        f_main = tk.Frame(self.content, bg="#F4F7F6")
        f_main.pack(fill="both", expand=True, padx=20)
        col_fecha = tk.LabelFrame(f_main, text=" 1. Fecha ", bg="white", padx=10, pady=10)
        col_fecha.pack(side="left", fill="y", padx=5)
        self.cb_dia = ttk.Combobox(col_fecha, values=[str(i).zfill(2) for i in range(1, 32)], width=5); self.cb_dia.set("20"); self.cb_dia.pack()
        self.cb_mes = ttk.Combobox(col_fecha, values=[str(i).zfill(2) for i in range(1, 13)], width=5); self.cb_mes.set("02"); self.cb_mes.pack()
        self.cb_ano = ttk.Combobox(col_fecha, values=["2026"], width=5); self.cb_ano.set("2026"); self.cb_ano.pack()
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
            tk.Radiobutton(f, text="V", variable=v, value="Asistio", bg="white", fg="green").pack(side="left")
            tk.Radiobutton(f, text="F", variable=v, value="Falto", bg="white", fg="red").pack(side="left")
            tk.Button(f, text="Hist", font=("Arial", 7), command=lambda n=j: self.dibujar_calendario_asis(n)).pack(side="right")
        tk.Button(self.col_lista_asis, text="GUARDAR", bg="#27AE60", fg="white", command=self.guardar_asistencia).pack(pady=10, fill="x")

    def dibujar_calendario_asis(self, nombre):
        for w in self.col_historial_asis.winfo_children(): w.destroy()
        grid = tk.Frame(self.col_historial_asis, bg="white"); grid.pack()
        mes, ano = int(self.cb_mes.get()), int(self.cb_ano.get())
        cal_matriz = calendar.monthcalendar(ano, mes)
        for r, sem in enumerate(cal_matriz):
            for c, dia in enumerate(sem):
                if dia == 0: continue
                f_key = f"{str(dia).zfill(2)}/{str(mes).zfill(2)}/{ano}"
                estado = self.registro_asistencia.get(nombre, {}).get(f_key, "N")
                color = "#EEE"
                if estado == "Asistio": color = "#28A745"
                elif estado == "Falto": color = "#DC3545"
                tk.Label(grid, text=str(dia), bg=color, width=3).grid(row=r, column=c, padx=1, pady=1)

    def guardar_asistencia(self):
        fecha = f"{self.cb_dia.get()}/{self.cb_mes.get()}/{self.cb_ano.get()}"
        for j, v in self.vars_asis.items():
            if v.get() != "Pendiente":
                if j not in self.registro_asistencia: self.registro_asistencia[j] = {}
                self.registro_asistencia[j][fecha] = v.get()
        messagebox.showinfo("Éxito", "Guardado")

    # =================================================================
    # MÓDULO 2: STATS JUGADORES
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
        tk.Button(f_edit, text="ACTUALIZAR", bg="#27AE60", fg="white", command=self.guardar_stats).pack(pady=20, fill="x")
        f_tabla = tk.LabelFrame(f_stats, text=" Tabla General ", bg="white", padx=10, pady=10)
        f_tabla.pack(side="left", fill="both", expand=True, padx=5)
        cols = ("Jugador", "Goles", "Asistencias", "Partidos")
        self.tree = ttk.Treeview(f_tabla, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=80, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.actualizar_tabla_stats()

    def cargar_stats_campos(self, event):
        j = self.cb_j_stats.get(); s = self.jugadores_stats[j]
        self.ent_g.delete(0, tk.END); self.ent_g.insert(0, str(s["goles"]))
        self.ent_a.delete(0, tk.END); self.ent_a.insert(0, str(s["asistencias"]))
        self.ent_p.delete(0, tk.END); self.ent_p.insert(0, str(s["partidos"]))

    def guardar_stats(self):
        j = self.cb_j_stats.get()
        if j:
            self.jugadores_stats[j] = {"goles": int(self.ent_g.get()), "asistencias": int(self.ent_a.get()), "partidos": int(self.ent_p.get())}
            self.actualizar_tabla_stats(); messagebox.showinfo("Ok", "Guardado")

    def actualizar_tabla_stats(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for j, s in self.jugadores_stats.items(): self.tree.insert("", "end", values=(j, s["goles"], s["asistencias"], s["partidos"]))

    # =================================================================
    # MÓDULO 3: ESTADÍSTICAS DE EQUIPO (NUEVO)
    # =================================================================
    def seccion_stats_equipo(self):
        self.limpiar_pantalla()
        tk.Label(self.content, text="Rendimiento Global del Club", font=("Helvetica", 22, "bold"), bg="#F4F7F6").pack(anchor="w", padx=30, pady=20)

        # Contenedor de Tarjetas Informativas
        self.f_cards = tk.Frame(self.content, bg="#F4F7F6")
        self.f_cards.pack(fill="x", padx=30)
        self.dibujar_tarjetas_equipo()

        # Formulario de Edición
        f_bottom = tk.Frame(self.content, bg="#F4F7F6")
        f_bottom.pack(fill="both", expand=True, padx=30, pady=20)

        f_edit_club = tk.LabelFrame(f_bottom, text=" Actualizar Datos del Club ", bg="white", padx=20, pady=20, font=("bold"))
        f_edit_club.pack(side="left", fill="both", expand=True)

        # Campos de entrada para el equipo
        self.inputs_club = {}
        campos = [("Partidos Jugados:", "jugados"), ("Victorias:", "ganados"), 
                  ("Empates:", "empatados"), ("Derrotas:", "perdidos"), 
                  ("Goles a Favor:", "goles_favor"), ("Goles en Contra:", "goles_contra")]

        for i, (label, key) in enumerate(campos):
            row, col = i // 2, i % 2
            tk.Label(f_edit_club, text=label, bg="white").grid(row=row*2, column=col, sticky="w", padx=10, pady=(5,0))
            ent = tk.Entry(f_edit_club, font=("Helvetica", 11), width=20)
            ent.insert(0, str(self.club_stats[key]))
            ent.grid(row=row*2+1, column=col, padx=10, pady=5)
            self.inputs_club[key] = ent

        tk.Button(f_edit_club, text="GUARDAR BALANCE TEMPORADA", bg="#27AE60", fg="white", font=("bold"), 
                  pady=10, command=self.actualizar_club_stats).grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")

    def dibujar_tarjetas_equipo(self):
        for w in self.f_cards.winfo_children(): w.destroy()
        
        # Datos para las tarjetas
        data = [
            ("PARTIDOS", self.club_stats["jugados"], "#3498DB"),
            ("GANADOS", self.club_stats["ganados"], "#27AE60"),
            ("PERDIDOS", self.club_stats["perdidos"], "#E74C3C"),
            ("GOLES +", self.club_stats["goles_favor"], "#F1C40F"),
            ("GOLES -", self.club_stats["goles_contra"], "#95A5A6")
        ]

        for i, (titulo, valor, color) in enumerate(data):
            card = tk.Frame(self.f_cards, bg="white", highlightthickness=2, highlightbackground=color, width=150, height=100)
            card.pack(side="left", padx=10, pady=10, expand=True, fill="both")
            card.pack_propagate(False)
            
            tk.Label(card, text=titulo, font=("Helvetica", 9, "bold"), bg="white", fg="gray").pack(pady=(10,0))
            tk.Label(card, text=str(valor), font=("Helvetica", 20, "bold"), bg="white", fg=color).pack()

    def actualizar_club_stats(self):
        try:
            for key, entry in self.inputs_club.items():
                self.club_stats[key] = int(entry.get())
            
            self.dibujar_tarjetas_equipo()
            messagebox.showinfo("Éxito", "Balance del club actualizado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa solo números en todos los campos.")

if __name__ == "__main__":
    SistemaEntrenadorIntegrado()