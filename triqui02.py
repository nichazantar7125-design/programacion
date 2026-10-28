import tkinter as tk


# ======================================================================
# LÓGICA DEL JUEGO (no depende de tkinter)
# ======================================================================
class JuegoTriqui:

    def __init__(self, nombre_x="Jugador X", nombre_o="Jugador O", inicia="X"):
        self.nombres = {"X": nombre_x, "O": nombre_o}
        self.marcador = {"X": 0, "O": 0}
        self.empates = 0
        self.inicial = inicia
        self._limpiar_partida()

    # ---------- estado de la partida ----------
    def _limpiar_partida(self):
        self.tablero = [["", "", ""] for _ in range(3)]
        self.turno = self.inicial
        self.terminado = False
        self.ganador = None  # "X", "O" o None (empate / en curso)

    def nueva_partida(self):
        """Limpia el tablero pero conserva marcador y nombres."""
        self._limpiar_partida()

    def reiniciar_marcador(self):
        self.marcador = {"X": 0, "O": 0}
        self.empates = 0
        self._limpiar_partida()

    # ---------- configuración ----------
    def establecer_nombre(self, simbolo, nombre):
        nombre = nombre.strip()
        self.nombres[simbolo] = nombre if nombre else "Jugador " + simbolo

    def establecer_inicial(self, simbolo):
        """Define quién comienza. Si el tablero está vacío, aplica ya."""
        self.inicial = simbolo
        if self.tablero_vacio():
            self.turno = simbolo

    # ---------- jugadas ----------
    def jugar(self, fila, columna):
        """Devuelve True si la jugada fue válida."""
        if self.terminado or self.tablero[fila][columna] != "":
            return False

        self.tablero[fila][columna] = self.turno

        if self.hay_ganador():
            self.terminado = True
            self.ganador = self.turno
            self.marcador[self.turno] += 1
        elif self.tablero_lleno():
            self.terminado = True
            self.empates += 1
        else:
            self.cambiar_turno()

        return True

    def cambiar_turno(self):
        self.turno = "O" if self.turno == "X" else "X"

    # ---------- consultas ----------
    def nombre_turno(self):
        return self.nombres[self.turno]

    def hay_ganador(self):
        t = self.tablero
        lineas = []
        for i in range(3):
            lineas.append([t[i][0], t[i][1], t[i][2]])  # filas
            lineas.append([t[0][i], t[1][i], t[2][i]])  # columnas
        lineas.append([t[0][0], t[1][1], t[2][2]])      # diagonal
        lineas.append([t[0][2], t[1][1], t[2][0]])      # diagonal inversa

        return any(l[0] != "" and l[0] == l[1] == l[2] for l in lineas)

    def tablero_lleno(self):
        return all(celda != "" for fila in self.tablero for celda in fila)

    def tablero_vacio(self):
        return all(celda == "" for fila in self.tablero for celda in fila)


# ======================================================================
# INTERFAZ GRÁFICA (solo muestra el estado y reenvía los clics)
# ======================================================================
COLORES = {"X": "#1565c0", "O": "#c62828"}
FONDOS = {"X": "#e3f2fd", "O": "#ffebee"}
FONDO_NEUTRO = "#f5f5f5"


class InterfazTriqui:

    def __init__(self):
        self.juego = JuegoTriqui()

        self.ventana = tk.Tk()
        self.ventana.title("Triqui")
        self.ventana.resizable(False, False)

        self._crear_panel_jugadores()
        self._crear_marcador()
        self._crear_tablero()
        self._crear_botones()
        self.actualizar()

    # ---------- construcción de widgets ----------
    def _crear_panel_jugadores(self):
        panel = tk.Frame(self.ventana)
        panel.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0))

        self.var_nombre = {"X": tk.StringVar(value="Jugador X"),
                           "O": tk.StringVar(value="Jugador O")}

        for col, simbolo in enumerate(("X", "O")):
            tk.Label(panel, text=simbolo + ":", fg=COLORES[simbolo],
                     font=("Arial", 12, "bold")).grid(row=col, column=0, sticky="e")
            entrada = tk.Entry(panel, textvariable=self.var_nombre[simbolo], width=16)
            entrada.grid(row=col, column=1, padx=5, pady=2)
            self.var_nombre[simbolo].trace_add(
                "write", lambda *_, s=simbolo: self.cambiar_nombre(s))

        tk.Label(panel, text="Comienza:").grid(row=0, column=2, padx=(15, 0))
        self.var_inicial = tk.StringVar(value="X")
        marco = tk.Frame(panel)
        marco.grid(row=1, column=2, padx=(15, 0))
        for simbolo in ("X", "O"):
            tk.Radiobutton(marco, text=simbolo, value=simbolo,
                           variable=self.var_inicial,
                           command=self.cambiar_inicial).pack(side="left")

    def _crear_marcador(self):
        self.etiqueta_marcador = tk.Label(self.ventana, font=("Arial", 12))
        self.etiqueta_marcador.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        self.etiqueta = tk.Label(self.ventana, font=("Arial", 16, "bold"))
        self.etiqueta.grid(row=2, column=0, columnspan=3, pady=8)

    def _crear_tablero(self):
        self.botones = []
        for fila in range(3):
            fila_botones = []
            for columna in range(3):
                boton = tk.Button(
                    self.ventana, text="", font=("Arial", 24, "bold"),
                    width=5, height=2, bg=FONDO_NEUTRO,
                    command=lambda f=fila, c=columna: self.clic_casilla(f, c))
                boton.grid(row=fila + 3, column=columna, padx=3, pady=3)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

    def _crear_botones(self):
        tk.Button(self.ventana, text="Nueva partida",
                  command=self.nueva_partida).grid(
            row=6, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 2))

        tk.Button(self.ventana, text="Reiniciar marcador",
                  command=self.reiniciar_marcador).grid(
            row=7, column=0, columnspan=3, sticky="ew", padx=10, pady=(2, 10))

    # ---------- eventos ----------
    def cambiar_nombre(self, simbolo):
        self.juego.establecer_nombre(simbolo, self.var_nombre[simbolo].get())
        self.actualizar()

    def cambiar_inicial(self):
        self.juego.establecer_inicial(self.var_inicial.get())
        self.actualizar()

    def clic_casilla(self, fila, columna):
        if self.juego.jugar(fila, columna):
            self.actualizar()

    def nueva_partida(self):
        self.juego.nueva_partida()
        self.actualizar()

    def reiniciar_marcador(self):
        self.juego.reiniciar_marcador()
        self.actualizar()

    # ---------- dibujo ----------
    def actualizar(self):
        j = self.juego

        for fila in range(3):
            for columna in range(3):
                simbolo = j.tablero[fila][columna]
                boton = self.botones[fila][columna]
                if simbolo:
                    boton.config(text=simbolo, state="disabled",
                                 disabledforeground=COLORES[simbolo],
                                 bg=FONDOS[simbolo])
                else:
                    estado = "disabled" if j.terminado else "normal"
                    boton.config(text="", state=estado, bg=FONDO_NEUTRO)

        if j.ganador:
            self.etiqueta.config(text="¡Ganó " + j.nombres[j.ganador] + "!",
                                 fg=COLORES[j.ganador])
        elif j.terminado:
            self.etiqueta.config(text="Empate", fg="black")
        else:
            self.etiqueta.config(text="Turno: " + j.nombre_turno() + " (" + j.turno + ")",
                                 fg=COLORES[j.turno])

        self.etiqueta_marcador.config(
            text="{} (X): {}   |   {} (O): {}   |   Empates: {}".format(
                j.nombres["X"], j.marcador["X"],
                j.nombres["O"], j.marcador["O"],
                j.empates))

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    InterfazTriqui().ejecutar()