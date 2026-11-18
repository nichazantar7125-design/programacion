import random
import tkinter as tk

# ---------------------------------------------------------------- DATOS
# cada carta es un emoji + un texto (el \n pone el texto en la línea de abajo)
PALABRAS = ["📋\nClase", "📦\nObjeto", "🌳\nHerencia", "🎭\nPolimorfismo",
            "🔒\nEncapsulamiento", "🔍\nAbstracción", "🔧\nMétodo",
            "🔖\nAtributo", "🔨\nConstructor", "📜\nInterfaz"]

NIVELES = {"Fácil": (3, 4, 12), "Normal": (4, 4, 14), "Difícil": (4, 5, 16)}   # (filas, columnas, intentos en solitario)

# colores
FONDO = "#12142B"        # fondo de la ventana
TEXTO = "#EDEFFF"        # letras claras
OCULTA = "#3B4488"       # carta boca abajo
AMARILLO = "#FFD43B"     # carta volteada y botones
VERDE = "#5EE08A"        # pareja encontrada
OSCURO = "#1B1E3A"       # letras sobre fondo claro

raiz = tk.Tk()
raiz.title("Memoria POO")
raiz.configure(bg=FONDO)

var_modo = tk.StringVar(value="Solitario")     # guarda lo que se elige en el menú
var_nivel = tk.StringVar(value="Normal")

# ---------------------------------------------------- ESTADO DE LA PARTIDA
pantalla = None     # el marco que se está mostrando (menú o juego)
etiqueta = None     # texto del marcador
cartas = []         # palabras mezcladas
botones = []        # cartas del tablero
primera = None      # primera carta volteada (None = ninguna)
bloqueo = False     # True mientras se ven dos cartas distintas
turno = 0           # a quién le toca
puntos = []         # parejas de cada jugador
intentos = 0
max_intentos = 0    # intentos permitidos (solo en solitario)
id_after = None     # temporizador pendiente


def limpiar():
    """Borra la pantalla actual y crea una vacía."""
    global pantalla, id_after
    if id_after is not None:                    # cancela el giro pendiente
        raiz.after_cancel(id_after)
        id_after = None
    if pantalla is not None:
        pantalla.destroy()
    pantalla = tk.Frame(raiz, bg=FONDO)
    pantalla.pack(padx=30, pady=20)


def boton(padre, texto, comando):
    """Botón amarillo hecho con un Label (así el color se ve en todos los sistemas)."""
    b = tk.Label(padre, text=texto, bg=AMARILLO, fg="#2B2400", cursor="hand2",
                 font=("Helvetica", 12, "bold"), padx=20, pady=6)
    b.bind("<Button-1>", lambda evento: comando())
    return b


# ---------------------------------------------------------------- MENÚ
def selector(titulo, variable, opciones):
    """Un título y una fila de opciones para elegir una."""
    tk.Label(pantalla, text=titulo, bg=FONDO, fg=TEXTO,
             font=("Helvetica", 10, "bold")).pack(pady=(14, 4))
    fila = tk.Frame(pantalla, bg=FONDO)
    fila.pack()
    for opcion in opciones:
        tk.Radiobutton(fila, text=opcion, value=opcion, variable=variable,
                       indicatoron=False, bg=FONDO, fg=TEXTO, selectcolor=OCULTA,
                       activebackground=OCULTA, activeforeground=TEXTO,
                       font=("Helvetica", 11, "bold"), padx=14, pady=5,
                       bd=0, highlightthickness=0).pack(side="left", padx=3)


def mostrar_menu():
    limpiar()
    tk.Label(pantalla, text="{ }  MEMORIA POO", bg=FONDO, fg=TEXTO,
             font=("Helvetica", 26, "bold")).pack()
    tk.Label(pantalla, text="Empareja los conceptos de la Programación Orientada a Objetos",
             bg=FONDO, fg=TEXTO, font=("Helvetica", 10)).pack(pady=(2, 8))

    selector("MODO DE JUEGO", var_modo, ("Solitario", "2 jugadores"))
    selector("DIFICULTAD", var_nivel, tuple(NIVELES.keys()))

    boton(pantalla, "▶  JUGAR", mostrar_juego).pack(pady=20)


# --------------------------------------------------------------- JUEGO
def mostrar_juego():
    global cartas, botones, primera, bloqueo, turno, puntos, intentos, max_intentos, etiqueta
    limpiar()

    filas, columnas, max_intentos = NIVELES[var_nivel.get()]
    total = filas * columnas // 2                       # número de parejas

    cartas = random.sample(PALABRAS, total) * 2         # elige palabras y las duplica
    random.shuffle(cartas)

    if var_modo.get() == "2 jugadores":
        puntos = [0, 0]
    else:
        puntos = [0]
    primera = None
    bloqueo = False
    turno = 0
    intentos = 0

    tk.Label(pantalla, text="{ }  MEMORIA POO", bg=FONDO, fg=TEXTO,
             font=("Helvetica", 18, "bold")).pack()
    etiqueta = tk.Label(pantalla, bg=FONDO, fg=AMARILLO, font=("Helvetica", 14, "bold"))
    etiqueta.pack(pady=8)

    tablero = tk.Frame(pantalla, bg=FONDO)
    tablero.pack()
    botones = []
    for fila in range(filas):
        for columna in range(columnas):
            i = fila * columnas + columna
            b = tk.Label(tablero, text="?", width=16, height=3, bg=OCULTA, fg=TEXTO,
                         font=("Helvetica", 12, "bold"), relief="raised", bd=3,
                         cursor="hand2")
            b.bind("<Button-1>", lambda evento, i=i: voltear(i))
            b.grid(row=fila, column=columna, padx=4, pady=4)
            botones.append(b)

    abajo = tk.Frame(pantalla, bg=FONDO)
    abajo.pack(pady=12)
    boton(abajo, "↻  Reiniciar", mostrar_juego).pack(side="left", padx=6)
    boton(abajo, "Menú", mostrar_menu).pack(side="left", padx=6)

    actualizar()


def actualizar():
    """Escribe el marcador según el modo."""
    if len(puntos) == 1:
        etiqueta.config(text="Intentos restantes: " + str(max_intentos - intentos) +
                             "   ·   Parejas: " + str(puntos[0]) + "/" + str(len(cartas) // 2))
    else:
        etiqueta.config(text="Turno: Jugador " + str(turno + 1) +
                             "   ·   J1: " + str(puntos[0]) + "   J2: " + str(puntos[1]))


def voltear(i):
    global primera, bloqueo, intentos, id_after
    if bloqueo or botones[i]["text"] != "?":
        return
    botones[i].config(text=cartas[i], bg=AMARILLO, fg=OSCURO)     # carta volteada
    if primera is None:
        primera = i
        return

    intentos = intentos + 1                             # segunda carta = un intento

    if cartas[primera] == cartas[i]:
        botones[primera].config(bg=VERDE)               # pareja: se pinta de verde
        botones[i].config(bg=VERDE)
        puntos[turno] = puntos[turno] + 1
        primera = None
        actualizar()
        if sum(puntos) == len(cartas) // 2:
            fin()
    else:
        bloqueo = True
        if len(puntos) == 1 and intentos == max_intentos:
            perder()                                    # se acabaron los intentos
            return
        id_after = raiz.after(1000, ocultar, primera, i)
        primera = None
        actualizar()


def ocultar(a, b):
    global bloqueo, turno, id_after
    id_after = None
    for n in (a, b):
        botones[n].config(text="?", bg=OCULTA, fg=TEXTO)     # vuelven a boca abajo
    bloqueo = False
    turno = (turno + 1) % len(puntos)       # con 1 jugador siempre da 0
    actualizar()


def perder():
    """Solitario: se acabaron los intentos. El tablero queda bloqueado."""
    etiqueta.config(text="Perdiste. Encontraste " + str(puntos[0]) + " de " +
                         str(len(cartas) // 2) + " parejas.", fg="#FF7B7B")


def fin():
    if len(puntos) == 1:
        mensaje = "¡Ganaste en " + str(intentos) + " intentos!"
    elif puntos[0] > puntos[1]:
        mensaje = "¡Gana el Jugador 1!"
    elif puntos[1] > puntos[0]:
        mensaje = "¡Gana el Jugador 2!"
    else:
        mensaje = "¡Empate!"
    etiqueta.config(text=mensaje, fg=VERDE)


# ------------------------------------------------------------- INICIO
mostrar_menu()
raiz.mainloop()