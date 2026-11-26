import random
import tkinter as tk

# Nicole Isabela Chazatar Inagan y Ashlynn Nicole Santander Achicanoy

CONCEPTOS = {
    "Clase": ("📋", "#FFB3C1"), "Objeto": ("📦", "#FFD6A5"), "Herencia": ("🌳", "#B5EAD7"),
    "Polimorfismo": ("🎭", "#C7B8FF"), "Encapsulamiento": ("🔒", "#A0C4FF"),
    "Abstracción": ("🔍", "#BDE0FE"), "Método": ("🔧", "#FDFFB6"), "Atributo": ("🔖", "#FFC6FF"),
    "Constructor": ("🔨", "#CAFFBF"), "Interfaz": ("📜", "#FFD1A9"),
}
NIVELES = {"Fácil": (3, 4, 12), "Normal": (4, 4, 14), "Difícil": (4, 5, 16)}
FONDO, TEXTO, OCULTA, AMARILLO, VERDE, ROJO = "#12142B", "#EDEFFF", "#3B4488", "#FFD43B", "#5EE08A", "#FF7B7B"

class Carta:
    def __init__(self, concepto):
        self.concepto, self.estado = concepto, "oculta"

    def cambiar(self, estado):
        self.estado = estado

    def coincide_con(self, otra):
        return self.concepto == otra.concepto

class Tablero:
    def __init__(self, filas, columnas):
        self.conceptos = random.sample(list(CONCEPTOS), filas * columnas // 2)
        self.cartas = [Carta(c) for c in self.conceptos * 2]
        random.shuffle(self.cartas)

    def completo(self):
        return all(c.estado == "emparejada" for c in self.cartas)

class Jugador:
    def __init__(self, nombre):
        self.nombre, self.parejas = nombre, 0

class JuegoMemoria:
    def __init__(self, modo, nivel):
        self.solitario = modo == "Solitario"
        self.filas, self.columnas, self.max_intentos = NIVELES[nivel]
        self.reiniciar()

    def reiniciar(self):
        self.tablero = Tablero(self.filas, self.columnas)
        self.jugadores = [Jugador(f"Jugador {k + 1}") for k in range(1 if self.solitario else 2)]
        self.turno = self.intentos = 0
        self.primera = self.resultado = self.ganador = None
        self.pendientes = []
        self.bloqueado = False

    def voltear(self, i):
        carta = self.tablero.cartas[i]
        if self.resultado or self.bloqueado:
            return "ignorada"
        if carta.estado != "oculta":
            return "repetida"
        carta.cambiar("visible")
        if self.primera is None:
            self.primera = carta
            return "primera"
        primera, self.primera = self.primera, None
        self.intentos += 1
        if primera.coincide_con(carta):
            primera.cambiar("emparejada")
            carta.cambiar("emparejada")
            self.jugadores[self.turno].parejas += 1
        else:
            self.pendientes = [primera, carta]
        self.revisar()
        self.bloqueado = bool(self.pendientes) and not self.resultado
        return "no_coincide" if self.pendientes else "pareja"

    def ocultar_pendientes(self):
        for carta in self.pendientes:
            carta.cambiar("oculta")
        self.pendientes = []
        self.bloqueado = False
        self.turno = (self.turno + 1) % len(self.jugadores)

    def revisar(self):
        p = [j.parejas for j in self.jugadores]
        if self.tablero.completo():
            if self.solitario:
                self.resultado = "victoria"
            elif p[0] == p[1]:
                self.resultado = "empate"
            else:
                self.resultado, self.ganador = "gana", self.jugadores[p[1] > p[0]]
        elif self.solitario and self.intentos == self.max_intentos:
            self.resultado = "derrota"

def etiqueta(padre, texto="", tam=11, color=TEXTO):
    return tk.Label(padre, text=texto, bg=FONDO, fg=color, font=("Helvetica", tam, "bold"))

def boton(padre, texto, comando):
    b = tk.Label(padre, text=texto, bg=AMARILLO, fg="#2B2400",
                 font=("Helvetica", 12, "bold"), padx=20, pady=6)
    b.bind("<Button-1>", lambda e: comando())
    return b

class MenuInicio(tk.Frame):
    def __init__(self, raiz, al_jugar):
        super().__init__(raiz, bg=FONDO)
        self.modo, self.nivel = tk.StringVar(value="Solitario"), tk.StringVar(value="Normal")
        etiqueta(self, "{ }  MEMORIA POO", 26).pack()
        for titulo, var, opciones in (("MODO DE JUEGO", self.modo, ("Solitario", "2 jugadores")),
                                      ("DIFICULTAD", self.nivel, tuple(NIVELES))):
            etiqueta(self, titulo, 10).pack(pady=(14, 4))
            fila = tk.Frame(self, bg=FONDO)
            fila.pack()
            for o in opciones:
                tk.Radiobutton(fila, text=o, value=o, variable=var, indicatoron=False, bg=FONDO, fg=TEXTO,
                               selectcolor=OCULTA, activebackground=OCULTA, activeforeground=TEXTO,
                               font=("Helvetica", 11, "bold"), padx=14, pady=5, bd=0,
                               highlightthickness=0).pack(side="left", padx=3)
        boton(self, "▶  JUGAR", lambda: al_jugar(self.modo.get(), self.nivel.get())).pack(pady=24)

class PantallaJuego(tk.Frame):
    def __init__(self, raiz, juego, al_menu):
        super().__init__(raiz, bg=FONDO)
        self.juego, self.id_after, self.casillas = juego, None, []
        etiqueta(self, "{ }  MEMORIA POO", 18).pack()
        self.marcador = etiqueta(self, tam=14)
        self.marcador.pack(pady=8)
        tablero = tk.Frame(self, bg=FONDO)
        tablero.pack()
        for i in range(juego.filas * juego.columnas):
            c = tk.Label(tablero, width=16, height=3, relief="raised", bd=3, cursor="hand2",
                         font=("Helvetica", 12, "bold"))
            c.bind("<Button-1>", lambda e, i=i: self.clic(i))
            c.grid(row=i // juego.columnas, column=i % juego.columnas, padx=4, pady=4)
            self.casillas.append(c)
        self.mensaje = etiqueta(self)
        self.mensaje.pack(pady=8)
        abajo = tk.Frame(self, bg=FONDO)
        abajo.pack()
        boton(abajo, "↻  Reiniciar", self.reiniciar).pack(side="left", padx=6)
        boton(abajo, "Menú", al_menu).pack(side="left", padx=6)
        self.refrescar()
        self.decir("Haz clic en una carta.")

    def destroy(self):
        if self.id_after:
            self.after_cancel(self.id_after)
        super().destroy()

    def decir(self, texto, color=TEXTO):
        self.mensaje.config(text=texto, fg=color)

    def reiniciar(self):
        if self.id_after:
            self.after_cancel(self.id_after)
            self.id_after = None
        self.juego.reiniciar()
        self.refrescar()
        self.decir("Nueva partida.")

    def refrescar(self):
        j, a = self.juego, self.juego.jugadores
        for casilla, carta in zip(self.casillas, j.tablero.cartas):
            icono, color = CONCEPTOS[carta.concepto]
            ver = carta.estado != "oculta" or j.resultado == "derrota"
            fondo = {"visible": AMARILLO, "emparejada": color}.get(carta.estado, ROJO if ver else OCULTA)
            casilla.config(text=f"{icono}\n{carta.concepto}" if ver else "?", bg=fondo,
                           fg="#1B1E3A" if ver else TEXTO)
        if j.solitario:
            texto = f"Intentos restantes: {j.max_intentos - j.intentos}   ·   Parejas: {a[0].parejas}/{len(j.tablero.conceptos)}"
        else:
            texto = f"Turno: {a[j.turno].nombre}   ·   {a[0].nombre}: {a[0].parejas}   {a[1].nombre}: {a[1].parejas}"
        self.marcador.config(text=texto)

    def clic(self, i):
        j = self.juego
        r = j.voltear(i)
        if r == "ignorada":
            return
        if r == "repetida":
            return self.decir("Esa carta ya está descubierta.")
        self.refrescar()
        if r == "primera":
            self.decir("Elige la segunda carta.")
        elif j.resultado:
            self.final()
        elif r == "pareja":
            self.decir(f"¡Pareja! {j.tablero.cartas[i].concepto}", VERDE)
        else:
            self.decir("No coinciden." + ("" if j.solitario else f" Turno de {j.jugadores[(j.turno + 1) % 2].nombre}."))
            self.id_after = self.after(1000, self.ocultar)

    def ocultar(self):
        self.id_after = None
        self.juego.ocultar_pendientes()
        self.refrescar()

    def final(self):
        j, a = self.juego, self.juego.jugadores
        total = len(j.tablero.conceptos)
        if j.resultado == "victoria":
            texto = f"¡Ganaste! Encontraste las {total} parejas en {j.intentos} intentos"
        elif j.resultado == "derrota":
            texto = f"Perdiste, se acabaron los intentos. Encontraste {a[0].parejas} de {total} parejas"
        elif j.resultado == "gana":
            texto = f"¡Gana {j.ganador.nombre}! {max(x.parejas for x in a)} parejas contra {min(x.parejas for x in a)}"
        else:
            texto = f"¡Empate! Cada jugador encontró {a[0].parejas} parejas"
        self.decir(texto, ROJO if j.resultado == "derrota" else VERDE)

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memoria POO")
        self.configure(bg=FONDO)
        self.pantalla = None
        self.menu()

    def mostrar(self, pantalla):
        if self.pantalla:
            self.pantalla.destroy()
        self.pantalla = pantalla
        pantalla.pack(padx=30, pady=20)

    def menu(self):
        self.mostrar(MenuInicio(self, self.jugar))

    def jugar(self, modo, nivel):
        self.mostrar(PantallaJuego(self, JuegoMemoria(modo, nivel), self.menu))

if __name__ == "__main__":
    Aplicacion().mainloop()