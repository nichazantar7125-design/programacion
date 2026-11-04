import tkinter as tk

class JuegoTriqui:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.tablero = [["", "", ""] for _ in range(3)]
        self.turno = "X"
        self.ganador = None
        self.terminado = False


    def casilla_valida(self, fila, columna):
        return (0 <= fila < 3 and 0 <= columna < 3
                and self.tablero[fila][columna] == "")


    def cambiar_turno(self):
        if self.turno == "X":
            self.turno = "O"
        else:
            self.turno = "X"

    def realizar_jugada(self, fila, columna):
        if self.terminado or not self.casilla_valida(fila, columna):
            return False
        self.tablero[fila][columna] = self.turno
        self.ganador = self.hay_ganador()
        if self.ganador is not None:
            self.terminado = True
        elif self.tablero_lleno():
            self.terminado = True
        else:
            self.cambiar_turno()
        return True

    def hay_ganador(self):
        for fila in self.tablero:
            if fila[0] != "" and fila[0] == fila[1] == fila[2]:
                return fila[0]
        for columna in range(3):
            marca = self.tablero[0][columna]
            if (marca != "" and marca == self.tablero[1][columna]
                    == self.tablero[2][columna]):
                return marca
        centro = self.tablero[1][1]
        if centro != "":
            if self.tablero[0][0] == centro == self.tablero[2][2]:
                return centro
            if self.tablero[0][2] == centro == self.tablero[2][0]:
                return centro
        return None

    def tablero_lleno(self):
        for fila in self.tablero:
            for casilla in fila:
                if casilla == "":
                    return False
        return True

class InterfazTriqui:
    def __init__(self):
        self.juego = JuegoTriqui()
        self.ventana = tk.Tk()
        self.ventana.title("Triqui")
        self.botones = []
        self.mensaje = tk.Label(self.ventana, text="Turno: X",
                                font=("Arial", 14))
        self.mensaje.grid(row=3, column=0, columnspan=3)
        for fila in range(3):
            fila_botones = []
            for columna in range(3):
                boton = tk.Button(
                    self.ventana, text="", width=5, height=2,
                    font=("Arial", 24),
                    command=lambda f=fila, c=columna: self.al_hacer_clic(f, c))
                boton.grid(row=fila, column=columna, padx=3, pady=3)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

        tk.Button(self.ventana, text="Nueva partida",
                  command=self.nueva_partida).grid(
                      row=4, column=0, columnspan=3, pady=8)

    def al_hacer_clic(self, fila, columna):
        if self.juego.realizar_jugada(fila, columna):
            self.actualizar_vista()
        else:
            self.mensaje.config(text="Jugada inválida o partida terminada.")

    def actualizar_vista(self):
        for fila in range(3):
            for columna in range(3):
                self.botones[fila][columna].config(
                    text=self.juego.tablero[fila][columna])
        if self.juego.ganador is not None:
            texto = f"Ganó {self.juego.ganador}"
        elif self.juego.terminado:
            texto = "Empate"
        else:
            texto = f"Turno: {self.juego.turno}"
        self.mensaje.config(text=texto)

    def nueva_partida(self):
        self.juego.reiniciar()
        self.actualizar_vista()

    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    InterfazTriqui().iniciar()