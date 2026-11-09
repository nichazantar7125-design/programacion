class JuegoTriqui:
    def __init__(self):
        self.tablero= [["","",""],["","",""],["","",""]]
        self.turno = "X"

    def casilla_valida(self, fila, columna):
        return (0 <= fila < 3 and 0 <= columna < 3
            and self.tablero[fila][columna] == "")

    def cambiar_turno(self):
        if self.turno == "X":
            self.turno = "O"
        else:
            self.turno = "X"

    def realizar_jugada(self, fila, columna):
        if not self.casilla_valida(fila, columna):
            return False
        self.tablero[fila][columna] = self.turno
        self.cambiar_turno()
        return True

juego = JuegoTriqui()
juego.cambiar_turno()
print(juego.turno)  # O