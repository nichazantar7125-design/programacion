import tkinter as tk

class JuegoTriqui:
    def __init__(self):
        self.tablero = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.turno = "X"

    def jugar(self, fila, columna):
        if self.tablero[fila][columna] != "":
            return False
        self.tablero[fila][columna] = self.turno
        return True

    def cambiar_turno(self):
        if self.turno == "X":
            self.turno = "O"
        else:
            self.turno = "X"

    def hay_ganador(self):
        for fila in range(3):
            if (
                self.tablero[fila][0] != ""
                and
                self.tablero[fila][0]
                == self.tablero[fila][1]
                == self.tablero[fila][2]
            ):
                return True

        for columna in range(3):
            if (
                self.tablero[0][columna] != ""
                and
                self.tablero[0][columna]
                == self.tablero[1][columna]
                == self.tablero[2][columna]
            ):
                return True

        if (
            self.tablero[0][0] != ""
            and
            self.tablero[0][0]
            == self.tablero[1][1]
            == self.tablero[2][2]
        ):
            return True

        if (
            self.tablero[0][2] != ""
            and
            self.tablero[0][2]
            == self.tablero[1][1]
            == self.tablero[2][0]
        ):
            return True
        return False

    def tablero_lleno(self):
        for fila in self.tablero:
            if "" in fila:
                return False
        return True

    def reiniciar(self):
        self.tablero = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.turno = "X"

class InterfazTriqui:
    def __init__(self):
        self.juego = JuegoTriqui()
        self.ventana = tk.Tk()
        self.ventana.title("Triqui")
        self.etiqueta = tk.Label(
            self.ventana,
            text="Turno: X",
            font=("Arial", 16)
        )
        self.etiqueta.grid(
            row=0,
            column=0,
            columnspan=3,
            pady=10
        )
        self.botones = []


        for fila in range(3):

            fila_botones = []

            for columna in range(3):

                boton = tk.Button(
                    self.ventana,
                    text="",
                    font=("Arial", 24),
                    width=5,
                    height=2,
                    command=lambda f=fila, c=columna:
                        self.clic_casilla(f, c)
                )

                boton.grid(
                    row=fila + 1,
                    column=columna,
                    padx=3,
                    pady=3
                )

                fila_botones.append(boton)

            self.botones.append(fila_botones)


        self.boton_reiniciar = tk.Button(
            self.ventana,
            text="Nueva partida",
            command=self.reiniciar
        )

        self.boton_reiniciar.grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=10
        )


    def clic_casilla(self, fila, columna):

        jugada_valida = self.juego.jugar(
            fila,
            columna
        )


        if not jugada_valida:
            return


        self.botones[fila][columna].config(
            text=self.juego.turno,
            state="disabled"
        )


        if self.juego.hay_ganador():

            self.etiqueta.config(
                text="Ganó " + self.juego.turno
            )

            self.deshabilitar_tablero()

            return


        if self.juego.tablero_lleno():

            self.etiqueta.config(
                text="Empate"
            )

            return


        self.juego.cambiar_turno()


        self.etiqueta.config(
            text="Turno: " + self.juego.turno
        )


    def deshabilitar_tablero(self):

        for fila in self.botones:

            for boton in fila:

                boton.config(
                    state="disabled"
                )


    def reiniciar(self):

        self.juego.reiniciar()


        for fila in self.botones:

            for boton in fila:

                boton.config(
                    text="",
                    state="normal"
                )


        self.etiqueta.config(
            text="Turno: X"
        )


    def ejecutar(self):

        self.ventana.mainloop()

app = InterfazTriqui()

app.ejecutar()