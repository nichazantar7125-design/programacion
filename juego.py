"""
MEMORIA POO - Juego de memoria con Python y Tkinter
===================================================
Las parejas son conceptos de la Programación Orientada a Objetos
(Clase, Objeto, Herencia, Polimorfismo...), cada uno con su icono dibujado.

Modos de juego:   Solitario | 2 jugadores | Contra bot
Dificultades:     Fácil (3x4) | Normal (4x4) | Difícil (4x5)
Se puede cambiar: tema de colores, reverso de las cartas y nombres.

ORGANIZACIÓN DEL ARCHIVO (de arriba hacia abajo)
------------------------------------------------
PARTE 1 - LÓGICA DEL JUEGO (no usa Tkinter, no dibuja nada)
    Carta           una carta: su símbolo y su estado
    Tablero         el conjunto de cartas (filas x columnas)
    Jugador         nombre, parejas e intentos de quien juega
    Bot             el rival automático (recuerda cartas y elige)
    JuegoMemoria    las REGLAS: turnos, parejas, intentos, fin de la partida
    Configuracion   las opciones que elige el jugador en el menú

PARTE 2 - INTERFAZ GRÁFICA (Tkinter)
    Boton, Opcion, Selector    pequeños controles reutilizables
    CartaVisual                una carta dibujada en pantalla (con animaciones)
    MenuInicio                 pantalla donde se eligen las opciones
    PantallaJuego              pantalla donde se juega
    Aplicacion                 cambia entre el menú y la pantalla de juego

IDEA CLAVE: la lógica NO sabe nada de colores ni ventanas, y la interfaz NO
decide las reglas. La interfaz le pregunta a JuegoMemoria qué pasó con cada
clic y, según la respuesta (un Resultado), muestra lo que corresponda.
"""

import math
import random
import tkinter as tk


# =============================================================================
#  PARTE 1 - LÓGICA DEL JUEGO
# =============================================================================

# Textos que usamos como "estados" y "resultados". Se guardan en clases para
# no escribir las palabras a mano en todo el programa (evita errores de dedo).

class EstadoCarta:
    OCULTA = "oculta"
    VISIBLE = "visible"
    EMPAREJADA = "emparejada"


class EstadoPartida:
    EN_CURSO = "en curso"
    GANADA = "ganada"          # solitario: encontró todas las parejas
    PERDIDA = "perdida"        # solitario: se acabaron los intentos
    FINALIZADA = "finalizada"  # 2 jugadores o bot: ya no quedan parejas


class Resultado:
    """Lo que responde JuegoMemoria después de cada clic."""
    PRIMERA_CARTA = "primera carta"
    PAREJA = "pareja"
    NO_PAREJA = "no pareja"
    YA_DESCUBIERTA = "ya descubierta"
    MISMA_CARTA = "misma carta"
    BLOQUEADO = "bloqueado"
    PARTIDA_TERMINADA = "partida terminada"


class Modo:
    SOLITARIO = "Solitario"
    DOS_JUGADORES = "2 jugadores"
    CONTRA_BOT = "Contra bot"
    TODOS = (SOLITARIO, DOS_JUGADORES, CONTRA_BOT)


# Cada dificultad es un diccionario con sus números.
#   espera: milisegundos que se ven dos cartas que NO coinciden
#   memoria_bot: probabilidad (0 a 1) de que el bot recuerde una carta vista
NIVELES = {
    "Fácil":   {"filas": 3, "columnas": 4, "intentos": 12, "espera": 1500, "memoria_bot": 0.35},
    "Normal":  {"filas": 4, "columnas": 4, "intentos": 14, "espera": 1000, "memoria_bot": 0.65},
    "Difícil": {"filas": 4, "columnas": 5, "intentos": 16, "espera": 700,  "memoria_bot": 0.95},
}
NOMBRES_NIVELES = ("Fácil", "Normal", "Difícil")


class Configuracion:
    """Guarda lo que el jugador elige en el menú."""

    def __init__(self):
        self.modo = Modo.SOLITARIO
        self.dificultad = "Normal"
        self.tema = "Noche"
        self.reverso = "{ }"
        self.nombre1 = "Jugador 1"
        self.nombre2 = "Jugador 2"


class Carta:
    """Una carta del tablero: guarda su símbolo y su estado."""

    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.estado = EstadoCarta.OCULTA

    def esta_oculta(self):
        return self.estado == EstadoCarta.OCULTA

    def esta_emparejada(self):
        return self.estado == EstadoCarta.EMPAREJADA

    def voltear(self):
        """Muestra la carta (solo si estaba oculta)."""
        if self.esta_oculta():
            self.estado = EstadoCarta.VISIBLE

    def ocultar(self):
        """Vuelve a poner boca abajo una carta visible que no hizo pareja."""
        if self.estado == EstadoCarta.VISIBLE:
            self.estado = EstadoCarta.OCULTA

    def emparejar(self):
        """Deja la carta boca arriba para siempre."""
        self.estado = EstadoCarta.EMPAREJADA

    def coincide_con(self, otra):
        """True si las dos cartas tienen el mismo símbolo."""
        return self.simbolo == otra.simbolo


class Tablero:
    """Conjunto de cartas organizadas en filas x columnas."""

    # 10 conceptos de POO. Según la dificultad se usan 6, 8 o 10 de ellos.
    SIMBOLOS = ("clase", "objeto", "herencia", "polimorfismo", "encapsulamiento",
                "abstraccion", "metodo", "atributo", "constructor", "interfaz")

    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.simbolos_usados = []   # los conceptos elegidos para esta partida
        self._cartas = []           # lista con todas las cartas
        self.mezclar()

    def total_parejas(self):
        return (self.filas * self.columnas) // 2

    def mezclar(self):
        """Elige conceptos al azar, crea 2 cartas de cada uno y las mezcla."""
        self.simbolos_usados = random.sample(self.SIMBOLOS, self.total_parejas())
        self._cartas = []
        for simbolo in self.simbolos_usados:
            self._cartas.append(Carta(simbolo))
            self._cartas.append(Carta(simbolo))
        random.shuffle(self._cartas)

    def obtener_carta(self, posicion):
        """Devuelve la carta de la posición (fila, columna)."""
        fila, columna = posicion
        return self._cartas[fila * self.columnas + columna]

    def posiciones(self):
        """Lista con todas las posiciones (fila, columna)."""
        lista = []
        for fila in range(self.filas):
            for columna in range(self.columnas):
                lista.append((fila, columna))
        return lista

    def posiciones_ocultas(self):
        """Posiciones de las cartas que están boca abajo."""
        lista = []
        for posicion in self.posiciones():
            if self.obtener_carta(posicion).esta_oculta():
                lista.append(posicion)
        return lista


class Jugador:
    """Una persona (o el bot) que juega."""

    def __init__(self, nombre, es_bot=False):
        self.nombre = nombre
        self.es_bot = es_bot
        self.parejas = 0
        self.intentos = 0

    def reiniciar(self):
        self.parejas = 0
        self.intentos = 0


class Bot:
    """Rival automático. Juega "limpio": solo usa lo que ha visto.

    Cada vez que se voltea una carta, el bot decide si la recuerda
    (con la probabilidad `memoria`). Con memoria alta es más difícil de ganar.
    """

    def __init__(self, memoria):
        self.memoria = memoria
        self.recuerdos = {}   # posición -> símbolo que recuerda

    def olvidar_todo(self):
        self.recuerdos = {}

    def ver_carta(self, posicion, simbolo):
        """Se llama cada vez que se voltea una carta."""
        if random.random() < self.memoria:
            self.recuerdos[posicion] = simbolo

    def elegir_primera(self, tablero):
        """Elige la primera carta de su turno."""
        # 1) Si recuerda una pareja completa, juega una de ellas.
        pareja = self._buscar_pareja_recordada(tablero)
        if pareja is not None:
            return pareja[0]
        # 2) Si no, prueba una carta que no conoce.
        ocultas = tablero.posiciones_ocultas()
        desconocidas = []
        for posicion in ocultas:
            if posicion not in self.recuerdos:
                desconocidas.append(posicion)
        if len(desconocidas) > 0:
            return random.choice(desconocidas)
        return random.choice(ocultas)

    def elegir_segunda(self, tablero, primera):
        """Elige la segunda carta, sabiendo cuál fue la primera."""
        simbolo = tablero.obtener_carta(primera).simbolo
        # 1) Si recuerda dónde está la pareja de la primera, la elige.
        for posicion in self.recuerdos:
            carta = tablero.obtener_carta(posicion)
            if posicion != primera and carta.esta_oculta() and self.recuerdos[posicion] == simbolo:
                return posicion
        # 2) Si no, prueba una carta que no conoce.
        ocultas = tablero.posiciones_ocultas()   # la primera ya está volteada
        desconocidas = []
        for posicion in ocultas:
            if posicion not in self.recuerdos:
                desconocidas.append(posicion)
        if len(desconocidas) > 0:
            return random.choice(desconocidas)
        return random.choice(ocultas)

    def _buscar_pareja_recordada(self, tablero):
        """Devuelve [pos1, pos2] si recuerda dos cartas ocultas iguales."""
        por_simbolo = {}
        for posicion in self.recuerdos:
            if tablero.obtener_carta(posicion).esta_oculta():
                simbolo = self.recuerdos[posicion]
                if simbolo not in por_simbolo:
                    por_simbolo[simbolo] = []
                por_simbolo[simbolo].append(posicion)
        for simbolo in por_simbolo:
            if len(por_simbolo[simbolo]) >= 2:
                return por_simbolo[simbolo][:2]
        return None


class JuegoMemoria:
    """Las reglas del juego. Conoce el estado de la partida.

    No dibuja nada: cada clic se procesa en seleccionar() y devuelve un Resultado.
    """

    def __init__(self, configuracion):
        nivel = NIVELES[configuracion.dificultad]
        self.modo = configuracion.modo
        self.tablero = Tablero(nivel["filas"], nivel["columnas"])
        self.max_intentos = nivel["intentos"]
        self.espera_ms = nivel["espera"]

        # Jugadores y bot según el modo elegido
        self.bot = None
        if self.modo == Modo.SOLITARIO:
            self.jugadores = [Jugador(configuracion.nombre1)]
        elif self.modo == Modo.DOS_JUGADORES:
            self.jugadores = [Jugador(configuracion.nombre1), Jugador(configuracion.nombre2)]
        else:
            self.jugadores = [Jugador(configuracion.nombre1), Jugador("Bot", True)]
            self.bot = Bot(nivel["memoria_bot"])
        self.reiniciar()

    # ------------------------------------------------------------ estado
    def reiniciar(self):
        """Deja la partida como nueva."""
        self.tablero.mezclar()
        for jugador in self.jugadores:
            jugador.reiniciar()
        if self.bot is not None:
            self.bot.olvidar_todo()
        self.turno = 0                       # índice del jugador que juega
        self.primera = None                  # primera carta del intento
        self.segunda = None                  # segunda carta del intento
        self.intentos_restantes = self.max_intentos   # solo cuenta en solitario
        self.bloqueado = False               # True mientras se ven 2 cartas distintas
        self.estado = EstadoPartida.EN_CURSO

    def en_curso(self):
        return self.estado == EstadoPartida.EN_CURSO

    def es_solitario(self):
        return self.modo == Modo.SOLITARIO

    def jugador_actual(self):
        return self.jugadores[self.turno]

    def jugador_siguiente(self):
        return self.jugadores[(self.turno + 1) % len(self.jugadores)]

    def turno_es_bot(self):
        return self.jugador_actual().es_bot

    def parejas_encontradas(self):
        total = 0
        for jugador in self.jugadores:
            total = total + jugador.parejas
        return total

    def intentos_usados(self):
        return self.max_intentos - self.intentos_restantes

    def ganador(self):
        """En 2 jugadores / bot: devuelve al ganador, o None si hay empate."""
        a = self.jugadores[0]
        b = self.jugadores[1]
        if a.parejas > b.parejas:
            return a
        if b.parejas > a.parejas:
            return b
        return None

    # ------------------------------------------------------------ reglas
    def seleccionar(self, posicion):
        """Procesa el clic sobre una carta y devuelve un Resultado."""
        if not self.en_curso():
            return Resultado.PARTIDA_TERMINADA
        if self.bloqueado:
            return Resultado.BLOQUEADO

        carta = self.tablero.obtener_carta(posicion)

        # Acciones inválidas: no cambian nada
        if not carta.esta_oculta():
            if carta is self.primera:
                return Resultado.MISMA_CARTA
            return Resultado.YA_DESCUBIERTA

        carta.voltear()
        if self.bot is not None:
            self.bot.ver_carta(posicion, carta.simbolo)   # el bot mira, igual que todos

        # Primera carta del intento
        if self.primera is None:
            self.primera = carta
            return Resultado.PRIMERA_CARTA

        # Segunda carta: aquí se cuenta el intento
        self.segunda = carta
        jugador = self.jugador_actual()
        jugador.intentos = jugador.intentos + 1
        if self.es_solitario():
            self.intentos_restantes = self.intentos_restantes - 1

        if self.primera.coincide_con(self.segunda):
            self.primera.emparejar()
            self.segunda.emparejar()
            jugador.parejas = jugador.parejas + 1     # el jugador repite turno
            self.primera = None
            self.segunda = None
            self._comprobar_fin()
            return Resultado.PAREJA

        # No coinciden: se bloquea el tablero hasta llamar a ocultar_pendientes()
        self.bloqueado = True
        self._comprobar_fin()
        return Resultado.NO_PAREJA

    def ocultar_pendientes(self):
        """Voltea las 2 cartas que no coincidieron y, si hay rival, pasa el turno."""
        if self.primera is not None:
            self.primera.ocultar()
        if self.segunda is not None:
            self.segunda.ocultar()
        self.primera = None
        self.segunda = None
        self.bloqueado = False
        if not self.es_solitario():
            self.turno = (self.turno + 1) % len(self.jugadores)

    def _comprobar_fin(self):
        """La victoria se revisa antes que la derrota."""
        if self.parejas_encontradas() == self.tablero.total_parejas():
            if self.es_solitario():
                self.estado = EstadoPartida.GANADA
            else:
                self.estado = EstadoPartida.FINALIZADA
        elif self.es_solitario() and self.intentos_restantes == 0:
            self.estado = EstadoPartida.PERDIDA


# =============================================================================
#  PARTE 2 - INTERFAZ GRÁFICA
# =============================================================================

TITULO = "{ }  MEMORIA POO"

# Los temas son diccionarios de colores. Para crear un tema nuevo basta con
# copiar uno, cambiarle el nombre y modificar los colores.
TEMAS = {
    "Noche": {
        "fondo": "#12142B", "panel": "#1D2146", "borde": "#2E3466",
        "texto": "#EDEFFF", "suave": "#9AA0D0", "oscuro": "#1B1E3A",
        "acento": "#FFD43B", "acento_hover": "#FFE066", "boton_texto": "#2B2400",
        "reverso": "#3B4488", "hover": "#5361C4", "carta_borde": "#5A67C8",
        "borde_hover": "#9AA5FF", "carta_texto": "#8E98E8",
        "visible_borde": "#FFFFFF", "pareja_borde": "#2ECC71",
        "revelada": "#262B52", "sombra": "#0B0C1C",
        "ok": "#5EE08A", "error": "#FF7B7B", "info": "#9AA0D0",
    },
    "Día": {
        "fondo": "#EEF1FF", "panel": "#FFFFFF", "borde": "#C9CFF0",
        "texto": "#1E2350", "suave": "#6A72A8", "oscuro": "#1E2350",
        "acento": "#FFB703", "acento_hover": "#FFC933", "boton_texto": "#3A2A00",
        "reverso": "#6C7BE8", "hover": "#8794F2", "carta_borde": "#4F5FD0",
        "borde_hover": "#2F3EB0", "carta_texto": "#E4E8FF",
        "visible_borde": "#1E2350", "pareja_borde": "#1FAF63",
        "revelada": "#E3E6FA", "sombra": "#C5CBEA",
        "ok": "#1F9D55", "error": "#D64545", "info": "#6A72A8",
    },
    "Neón": {
        "fondo": "#0A0A12", "panel": "#14141F", "borde": "#2B2B55",
        "texto": "#F2F2FF", "suave": "#8F8FC8", "oscuro": "#0A0A12",
        "acento": "#00F5D4", "acento_hover": "#5FFBE6", "boton_texto": "#00231D",
        "reverso": "#1B1B3A", "hover": "#2A2A5E", "carta_borde": "#FF2E97",
        "borde_hover": "#00F5D4", "carta_texto": "#FF2E97",
        "visible_borde": "#00F5D4", "pareja_borde": "#00F5D4",
        "revelada": "#1A1A2C", "sombra": "#040408",
        "ok": "#00F5D4", "error": "#FF2E97", "info": "#8F8FC8",
    },
    "Bosque": {
        "fondo": "#0E1F16", "panel": "#173224", "borde": "#2A5A3E",
        "texto": "#E8F7EC", "suave": "#8CBF9F", "oscuro": "#10231A",
        "acento": "#F4C95D", "acento_hover": "#FFDD85", "boton_texto": "#2B2200",
        "reverso": "#2F6B4A", "hover": "#3F8A60", "carta_borde": "#58B27C",
        "borde_hover": "#A8F0C4", "carta_texto": "#A8F0C4",
        "visible_borde": "#FFFFFF", "pareja_borde": "#F4C95D",
        "revelada": "#1D3D2B", "sombra": "#08130D",
        "ok": "#7BE0A0", "error": "#FF8A80", "info": "#8CBF9F",
    },
}
NOMBRES_TEMAS = ("Noche", "Día", "Neón", "Bosque")

# Reverso de las cartas: texto -> tamaño de letra
REVERSOS = {"{ }": 24, "?": 30, "</>": 20, "POO": 17}

# concepto -> (nombre, color, explicación que se muestra al hacer pareja)
CONCEPTOS = {
    "clase": ("Clase", "#FF6B6B", "el molde que define atributos y métodos."),
    "objeto": ("Objeto", "#FFA94D", "una instancia creada a partir de una clase."),
    "herencia": ("Herencia", "#FFD43B", "una clase reutiliza lo de otra clase."),
    "polimorfismo": ("Polimorfismo", "#69DB7C", "un mismo método, muchos comportamientos."),
    "encapsulamiento": ("Encapsulamiento", "#38D9A9", "protege los datos dentro del objeto."),
    "abstraccion": ("Abstracción", "#4DABF7", "muestra solo lo esencial."),
    "metodo": ("Método", "#B197FC", "una acción que puede realizar un objeto."),
    "atributo": ("Atributo", "#F783AC", "un dato que guarda un objeto."),
    "constructor": ("Constructor", "#FF8FAB", "prepara un objeto nuevo al crearlo."),
    "interfaz": ("Interfaz", "#74C0FC", "un contrato: qué métodos debe tener una clase."),
}

BLANCO = "#FFFFFF"
GRIS_CLARO = "#DDE0F7"
GRIS_MEDIO = "#B7BCE8"
FUENTE = "Helvetica"


def rect_redondeado(lienzo, x1, y1, x2, y2, radio, **opciones):
    """Dibuja un rectángulo con esquinas redondeadas en un Canvas."""
    puntos = [x1 + radio, y1, x2 - radio, y1, x2, y1, x2, y1 + radio,
              x2, y2 - radio, x2, y2, x2 - radio, y2, x1 + radio, y2,
              x1, y2, x1, y2 - radio, x1, y1 + radio, x1, y1]
    return lienzo.create_polygon(puntos, smooth=True, **opciones)


# ----------------------------------------------------------------- ICONOS
# Cada icono se dibuja en una cuadrícula imaginaria de 100 x 100 y luego se
# escala al tamaño que se necesite. Cada función recibe:
#   c  = el Canvas donde dibujar      p  = convierte (x, y) de 0-100 a píxeles
#   xy = igual que p pero para varios puntos      w  = grosor de línea
#   fg = color del trazo              ac = color de los rellenos claros

def _icono_clase(c, p, xy, w, fg, ac):
    """Cuadro UML: nombre, atributos y métodos."""
    c.create_rectangle(*xy(10, 6, 90, 94), fill=ac, outline=fg, width=w)
    c.create_rectangle(*xy(10, 6, 90, 30), fill=fg, outline=fg, width=w)
    c.create_line(*xy(10, 62, 90, 62), fill=fg, width=w)
    for y, x2 in ((42, 62), (52, 50), (73, 68), (83, 54)):
        c.create_line(*xy(20, y, x2, y), fill=fg, width=w, capstyle="round")


def _icono_objeto(c, p, xy, w, fg, ac):
    """Cubo: algo concreto que existe."""
    c.create_polygon(*xy(14, 38, 64, 38, 64, 90, 14, 90), fill=ac, outline=fg, width=w)
    c.create_polygon(*xy(14, 38, 36, 12, 86, 12, 64, 38), fill=GRIS_CLARO, outline=fg, width=w)
    c.create_polygon(*xy(64, 38, 86, 12, 86, 64, 64, 90), fill=GRIS_MEDIO, outline=fg, width=w)


def _icono_herencia(c, p, xy, w, fg, ac):
    """Árbol: una clase padre y dos clases hijas."""
    c.create_rectangle(*xy(28, 6, 72, 32), fill=ac, outline=fg, width=w)
    c.create_polygon(*xy(50, 34, 41, 47, 59, 47), fill=ac, outline=fg, width=w)
    c.create_line(*xy(50, 47, 50, 56), fill=fg, width=w)
    c.create_line(*xy(24, 56, 76, 56), fill=fg, width=w)
    c.create_line(*xy(24, 56, 24, 68), fill=fg, width=w)
    c.create_line(*xy(76, 56, 76, 68), fill=fg, width=w)
    c.create_rectangle(*xy(5, 68, 43, 94), fill=ac, outline=fg, width=w)
    c.create_rectangle(*xy(57, 68, 95, 94), fill=ac, outline=fg, width=w)


def _icono_polimorfismo(c, p, xy, w, fg, ac):
    """Tres formas distintas: muchas formas, un mismo nombre."""
    x1, y1 = p(10, 10)
    x2, y2 = p(52, 52)
    c.create_oval(x1, y1, x2, y2, fill=ac, outline=fg, width=w)
    c.create_rectangle(*xy(58, 10, 92, 44), fill=GRIS_CLARO, outline=fg, width=w)
    c.create_polygon(*xy(50, 94, 26, 56, 74, 56), fill=GRIS_MEDIO, outline=fg, width=w)


def _icono_encapsulamiento(c, p, xy, w, fg, ac):
    """Candado: los datos quedan protegidos."""
    grosor = max(w * 2, 3)
    x1, y1 = p(28, 6)
    x2, y2 = p(72, 62)
    c.create_arc(x1, y1, x2, y2, start=0, extent=180, style="arc", outline=fg, width=grosor)
    c.create_line(*xy(28, 34, 28, 48), fill=fg, width=grosor)
    c.create_line(*xy(72, 34, 72, 48), fill=fg, width=grosor)
    rect_redondeado(c, *xy(16, 44, 84, 94), 6, fill=ac, outline=fg, width=w)
    x1, y1 = p(41, 55)
    x2, y2 = p(59, 73)
    c.create_oval(x1, y1, x2, y2, fill=fg, outline=fg)
    c.create_polygon(*xy(46, 68, 54, 68, 57, 84, 43, 84), fill=fg, outline=fg)


def _icono_abstraccion(c, p, xy, w, fg, ac):
    """Ojo: ver solo lo esencial."""
    c.create_polygon(*xy(4, 50, 28, 24, 72, 24, 96, 50, 72, 76, 28, 76),
                     smooth=True, fill=ac, outline=fg, width=w)
    x1, y1 = p(32, 32)
    x2, y2 = p(68, 68)
    c.create_oval(x1, y1, x2, y2, fill=fg, outline=fg)
    x1, y1 = p(44, 44)
    x2, y2 = p(56, 56)
    c.create_oval(x1, y1, x2, y2, fill=ac, outline=ac)


def _icono_metodo(c, p, xy, w, fg, ac):
    """Engranaje: una acción que el objeto sabe hacer."""
    puntos = []
    for diente in range(8):
        base = math.radians(diente * 45)
        for desvio, radio in ((-14, 34), (-9, 47), (9, 47), (14, 34)):
            angulo = base + math.radians(desvio)
            puntos.extend(p(50 + radio * math.cos(angulo), 50 + radio * math.sin(angulo)))
    c.create_polygon(puntos, fill=ac, outline=fg, width=w)
    x1, y1 = p(34, 34)
    x2, y2 = p(66, 66)
    c.create_oval(x1, y1, x2, y2, fill=fg, outline=fg)
    x1, y1 = p(43, 43)
    x2, y2 = p(57, 57)
    c.create_oval(x1, y1, x2, y2, fill=ac, outline=ac)


def _icono_atributo(c, p, xy, w, fg, ac):
    """Etiqueta: un dato que describe al objeto."""
    c.create_polygon(*xy(6, 20, 62, 20, 95, 50, 62, 80, 6, 80), fill=ac, outline=fg, width=w)
    x1, y1 = p(14, 43)
    x2, y2 = p(28, 57)
    c.create_oval(x1, y1, x2, y2, fill=fg, outline=fg)
    c.create_line(*xy(38, 42, 64, 42), fill=fg, width=w * 2, capstyle="round")
    c.create_line(*xy(38, 58, 56, 58), fill=fg, width=w * 2, capstyle="round")


def _icono_constructor(c, p, xy, w, fg, ac):
    """Martillo: construye el objeto nuevo."""
    c.create_rectangle(*xy(42, 30, 58, 94), fill=GRIS_MEDIO, outline=fg, width=w)
    c.create_rectangle(*xy(12, 8, 88, 36), fill=ac, outline=fg, width=w)
    c.create_line(*xy(70, 8, 70, 36), fill=fg, width=w)


def _icono_interfaz(c, p, xy, w, fg, ac):
    """Hoja de contrato: lista de métodos que se deben cumplir."""
    c.create_rectangle(*xy(14, 10, 86, 94), fill=ac, outline=fg, width=w)
    c.create_rectangle(*xy(34, 4, 66, 20), fill=fg, outline=fg, width=w)
    for y in (40, 58, 76):
        c.create_rectangle(*xy(24, y - 6, 36, y + 6), fill=fg, outline=fg)
        c.create_line(*xy(44, y, 76, y), fill=fg, width=w * 2, capstyle="round")


FUNCIONES_ICONO = {
    "clase": _icono_clase, "objeto": _icono_objeto, "herencia": _icono_herencia,
    "polimorfismo": _icono_polimorfismo, "encapsulamiento": _icono_encapsulamiento,
    "abstraccion": _icono_abstraccion, "metodo": _icono_metodo,
    "atributo": _icono_atributo, "constructor": _icono_constructor,
    "interfaz": _icono_interfaz,
}


def dibujar_icono(lienzo, clave, cx, cy, tam, fg, ac=BLANCO):
    """Dibuja el icono `clave` centrado en (cx, cy), con lado `tam` píxeles."""
    k = tam / 100.0
    grosor = max(1, round(tam * 0.045))

    def p(x, y):
        return (cx + (x - 50) * k, cy + (y - 50) * k)

    def xy(*coordenadas):
        salida = []
        for i in range(0, len(coordenadas), 2):
            salida.extend(p(coordenadas[i], coordenadas[i + 1]))
        return salida

    FUNCIONES_ICONO[clave](lienzo, p, xy, grosor, fg, ac)


# ------------------------------------------------------ CONTROLES PEQUEÑOS

class Boton(tk.Label):
    """Botón hecho con un Label (así los colores se ven igual en todos los sistemas)."""

    def __init__(self, padre, texto, comando, tema, principal=False):
        if principal:
            fondo, letra = tema["acento"], tema["boton_texto"]
        else:
            fondo, letra = tema["borde"], tema["texto"]
        tk.Label.__init__(self, padre, text=texto, bg=fondo, fg=letra,
                          font=(FUENTE, 12, "bold"), padx=22, pady=7, cursor="hand2")
        self.comando = comando
        self.tema = tema
        self.principal = principal
        self.fondo_normal = fondo
        self.bind("<Button-1>", self._al_pulsar)
        self.bind("<Enter>", self._al_entrar)
        self.bind("<Leave>", self._al_salir)

    def _al_pulsar(self, evento):
        self.comando()

    def _al_entrar(self, evento):
        if self.principal:
            self.configure(bg=self.tema["acento_hover"])
        else:
            self.configure(bg=self.tema["hover"], fg=BLANCO)

    def _al_salir(self, evento):
        self.configure(bg=self.fondo_normal)
        if not self.principal:
            self.configure(fg=self.tema["texto"])


class Opcion(tk.Label):
    """Una opción dentro de un Selector. Resaltada si es la elegida."""

    def __init__(self, padre, texto, al_elegir, tema, activa):
        tk.Label.__init__(self, padre, text=texto, font=(FUENTE, 11, "bold"),
                          padx=14, pady=6, cursor="hand2")
        self.texto = texto
        self.al_elegir = al_elegir
        self.tema = tema
        self.activa = activa
        self._pintar(False)
        self.bind("<Button-1>", self._al_pulsar)
        self.bind("<Enter>", self._al_entrar)
        self.bind("<Leave>", self._al_salir)

    def _pintar(self, encima):
        if self.activa:
            self.configure(bg=self.tema["acento"], fg=self.tema["boton_texto"])
        elif encima:
            self.configure(bg=self.tema["borde"], fg=self.tema["texto"])
        else:
            self.configure(bg=self.tema["panel"], fg=self.tema["suave"])

    def _al_pulsar(self, evento):
        self.al_elegir(self.texto)

    def _al_entrar(self, evento):
        self._pintar(True)

    def _al_salir(self, evento):
        self._pintar(False)


class Selector(tk.Frame):
    """Un título y una fila de opciones para elegir una."""

    def __init__(self, padre, titulo, opciones, valor, tema, al_elegir):
        tk.Frame.__init__(self, padre, bg=tema["fondo"])
        tk.Label(self, text=titulo, bg=tema["fondo"], fg=tema["suave"],
                 font=(FUENTE, 9, "bold")).pack()
        fila = tk.Frame(self, bg=tema["fondo"])
        fila.pack(pady=(3, 0))
        for texto in opciones:
            opcion = Opcion(fila, texto, al_elegir, tema, texto == valor)
            opcion.pack(side="left", padx=3)


# ----------------------------------------------------------------- CARTA

class CartaVisual(tk.Canvas):
    """Una carta dibujada en pantalla.

    HEREDA de tk.Canvas: una CartaVisual "es un" Canvas (un lienzo para dibujar)
    al que le agregamos cómo dibujarse, animarse y qué hacer cuando le hacen clic.
    No conoce las reglas: la pantalla le dice cómo debe verse.

    Modos de vista: "oculta", "visible", "emparejada", "revelada" (al perder).
    """

    RELLENO = 6      # margen alrededor de la carta
    PASO_MS = 24     # milisegundos de cada cuadro de la animación

    def __init__(self, padre, raiz, posicion, tam, tema, reverso, al_clic):
        tk.Canvas.__init__(self, padre, width=tam, height=tam, bg=tema["panel"],
                           highlightthickness=0, bd=0)
        self.raiz = raiz
        self.posicion = posicion
        self.tam = tam
        self.tema = tema
        self.reverso = reverso
        self.al_clic = al_clic
        self.modo = "oculta"
        self.concepto = None
        self.destino = ("oculta", None)
        self.interactiva = True
        self.hover = False
        self.brillo = False
        self.animando = False
        self.vivo = True
        self.cuadros = []
        self.total_brillos = 0

        self.bind("<Button-1>", self._al_pulsar)
        self.bind("<Enter>", self._al_entrar)
        self.bind("<Leave>", self._al_salir)
        self.bind("<Destroy>", self._al_destruir)
        self.dibujar()

    # ---------------------------------------------------------- eventos
    def _al_pulsar(self, evento):
        self.al_clic(self.posicion)

    def _al_entrar(self, evento):
        self.hover = True
        if not self.animando and self.modo == "oculta":
            self.dibujar()

    def _al_salir(self, evento):
        self.hover = False
        if not self.animando and self.modo == "oculta":
            self.dibujar()

    def _al_destruir(self, evento):
        self.vivo = False

    # ----------------------------------------------- lo que pide la pantalla
    def fijar(self, modo, concepto, interactiva):
        """Cambia la vista de golpe, sin animación."""
        self.modo = modo
        self.concepto = concepto
        self.destino = (modo, concepto)
        self.interactiva = interactiva
        self._poner_cursor()
        self.dibujar()

    def actualizar(self, modo, concepto, interactiva):
        """Cambia la vista. Si la carta cambia de lado, hace la animación de giro."""
        self.destino = (modo, concepto)
        self.interactiva = interactiva
        self._poner_cursor()
        if self.animando:
            return   # al terminar el giro se aplicará self.destino
        cambia_de_lado = (self.modo == "oculta") != (modo == "oculta")
        if cambia_de_lado:
            self._animar_giro()
        elif self.modo != modo or self.concepto != concepto:
            self.modo = modo
            self.concepto = concepto
            self.dibujar()
        else:
            self.dibujar()

    def _poner_cursor(self):
        if self.interactiva and self.destino[0] == "oculta":
            self.configure(cursor="hand2")
        else:
            self.configure(cursor="arrow")

    # -------------------------------------------------------- animaciones
    def agitar(self):
        """Sacudida horizontal: las cartas no coincidieron."""
        if self.animando:
            return
        self._paso_agitar(0, 0)

    def _paso_agitar(self, i, previo):
        desplazamientos = [-4, 4, -3, 3, -1, 0]
        if not self.vivo:
            return
        if i >= len(desplazamientos):
            self.dibujar()
            return
        self.move("all", desplazamientos[i] - previo, 0)
        self.raiz.after(32, self._paso_agitar, i + 1, desplazamientos[i])

    def brillar(self, parpadeos):
        """El borde parpadea en dorado."""
        self.total_brillos = parpadeos * 2
        self._paso_brillo(0)

    def _paso_brillo(self, i):
        if not self.vivo:
            return
        if self.animando:
            self.raiz.after(30, self._paso_brillo, i)
            return
        self.brillo = (i % 2 == 0) and (i < self.total_brillos)
        self.dibujar()
        if i < self.total_brillos:
            self.raiz.after(110, self._paso_brillo, i + 1)

    def _color_de(self, modo, concepto):
        if modo == "oculta":
            return self.tema["reverso"]
        if modo == "revelada":
            return self.tema["revelada"]
        return CONCEPTOS[concepto][1]

    def _animar_giro(self):
        """Giro: la carta se encoge hasta una línea y se abre por el otro lado."""
        self.animando = True
        color_origen = self._color_de(self.modo, self.concepto)
        color_destino = self._color_de(self.destino[0], self.destino[1])
        self.cuadros = [(0.75, color_origen), (0.45, color_origen), (0.15, color_origen),
                        (0.15, color_destino), (0.45, color_destino), (0.75, color_destino)]
        self._paso_giro(0)

    def _paso_giro(self, i):
        if not self.vivo:
            return
        if i < len(self.cuadros):
            escala, color = self.cuadros[i]
            centro = self.tam / 2
            mitad = centro - self.RELLENO
            self.delete("all")
            rect_redondeado(self, centro - mitad * escala, self.RELLENO,
                            centro + mitad * escala, self.tam - self.RELLENO, 10,
                            fill=color, outline=self.tema["carta_borde"], width=2)
            self.raiz.after(self.PASO_MS, self._paso_giro, i + 1)
        else:
            self.animando = False
            self.modo = self.destino[0]
            self.concepto = self.destino[1]
            self.dibujar()

    # ------------------------------------------------------------- dibujo
    def dibujar(self):
        """Pinta la carta según su modo."""
        if not self.vivo:
            return
        self.delete("all")
        t = self.tam
        r = self.RELLENO
        rect_redondeado(self, r + 1, r + 3, t - r + 1, t - r + 3, 10,
                        fill=self.tema["sombra"], outline="")     # sombra
        if self.modo == "oculta":
            self._dibujar_reverso()
        else:
            self._dibujar_frente()

    def _dibujar_reverso(self):
        t = self.tam
        r = self.RELLENO
        tema = self.tema
        sobre = self.hover and self.interactiva
        subir = 3 if sobre else 0           # al pasar el mouse, la carta "se levanta"
        rect_redondeado(self, r, r - subir, t - r, t - r - subir, 10,
                        fill=tema["hover"] if sobre else tema["reverso"],
                        outline=tema["borde_hover"] if sobre else tema["carta_borde"],
                        width=3 if sobre else 2)
        rect_redondeado(self, r + 7, r + 7 - subir, t - r - 7, t - r - 7 - subir, 7,
                        fill="", outline=tema["carta_texto"], width=1)
        self.create_text(t / 2, t / 2 - subir, text=self.reverso, fill=tema["carta_texto"],
                         font=(FUENTE, REVERSOS[self.reverso], "bold"))

    def _dibujar_frente(self):
        t = self.tam
        r = self.RELLENO
        tema = self.tema
        nombre, color, _ = CONCEPTOS[self.concepto]
        if self.modo == "revelada":
            fondo, borde, trazo, relleno, letra = tema["revelada"], tema["carta_borde"], color, tema["revelada"], color
            grosor = 2
        else:
            fondo, trazo, relleno, letra = color, tema["oscuro"], BLANCO, tema["oscuro"]
            grosor = 4
            if self.modo == "emparejada":
                borde = tema["acento"] if self.brillo else tema["pareja_borde"]
            else:
                borde = tema["visible_borde"]
        rect_redondeado(self, r, r, t - r, t - r, 10, fill=fondo, outline=borde, width=grosor)
        dibujar_icono(self, self.concepto, t / 2, t * 0.40, t * 0.52, trazo, relleno)
        tamano_letra = 8 if len(nombre) > 11 else 9
        self.create_text(t / 2, t - 16, text=nombre, fill=letra,
                         font=(FUENTE, tamano_letra, "bold"))


# ------------------------------------------------------------ PANTALLAS

class MenuInicio(tk.Frame):
    """Pantalla de inicio: se elige modo, dificultad, tema, reverso y nombres."""

    def __init__(self, raiz, app):
        configuracion = app.configuracion
        tema = TEMAS[configuracion.tema]
        tk.Frame.__init__(self, raiz, bg=tema["fondo"])
        self.app = app
        self.configuracion = configuracion
        self.tema = tema
        self.entrada1 = None
        self.entrada2 = None
        self._crear_titulo()
        self._crear_selectores()
        self._crear_nombres()
        self._crear_informacion()
        Boton(self, "▶  JUGAR", self._jugar, tema, True).pack(pady=(10, 6))
        self._crear_ayuda()

    def _crear_titulo(self):
        tema = self.tema
        tk.Label(self, text=TITULO, bg=tema["fondo"], fg=tema["texto"],
                 font=(FUENTE, 28, "bold")).pack(pady=(24, 0))
        tk.Label(self, text="Empareja los conceptos de la Programación Orientada a Objetos",
                 bg=tema["fondo"], fg=tema["suave"], font=(FUENTE, 10)).pack(pady=(2, 10))
        # Fila de iconos decorativos
        adorno = tk.Canvas(self, width=10 * 40, height=36, bg=tema["fondo"], highlightthickness=0)
        adorno.pack(pady=(0, 8))
        for i, clave in enumerate(Tablero.SIMBOLOS):
            color = CONCEPTOS[clave][1]
            rect_redondeado(adorno, i * 40 + 2, 2, i * 40 + 34, 34, 7, fill=color, outline=color)
            dibujar_icono(adorno, clave, i * 40 + 18, 18, 22, tema["oscuro"])

    def _crear_selectores(self):
        c = self.configuracion
        t = self.tema
        Selector(self, "MODO DE JUEGO", Modo.TODOS, c.modo, t, self._elegir_modo).pack(pady=5)
        Selector(self, "DIFICULTAD", NOMBRES_NIVELES, c.dificultad, t,
                 self._elegir_dificultad).pack(pady=5)
        Selector(self, "TEMA DE COLORES", NOMBRES_TEMAS, c.tema, t,
                 self._elegir_tema).pack(pady=5)
        Selector(self, "REVERSO DE LAS CARTAS", tuple(REVERSOS.keys()), c.reverso, t,
                 self._elegir_reverso).pack(pady=5)

    def _crear_nombres(self):
        c = self.configuracion
        t = self.tema
        fila = tk.Frame(self, bg=t["fondo"])
        fila.pack(pady=(8, 2))
        tk.Label(fila, text="Jugador 1:", bg=t["fondo"], fg=t["suave"],
                 font=(FUENTE, 10, "bold")).pack(side="left", padx=(0, 4))
        self.entrada1 = self._nueva_entrada(fila, c.nombre1)
        if c.modo == Modo.DOS_JUGADORES:
            tk.Label(fila, text="Jugador 2:", bg=t["fondo"], fg=t["suave"],
                     font=(FUENTE, 10, "bold")).pack(side="left", padx=(14, 4))
            self.entrada2 = self._nueva_entrada(fila, c.nombre2)
        elif c.modo == Modo.CONTRA_BOT:
            tk.Label(fila, text="Rival: Bot", bg=t["fondo"], fg=t["acento"],
                     font=(FUENTE, 10, "bold")).pack(side="left", padx=(14, 0))

    def _nueva_entrada(self, padre, texto):
        t = self.tema
        entrada = tk.Entry(padre, width=13, font=(FUENTE, 11), justify="center",
                           bg=t["panel"], fg=t["texto"], insertbackground=t["texto"],
                           relief="flat", highlightthickness=1,
                           highlightbackground=t["borde"], highlightcolor=t["acento"])
        entrada.insert(0, texto)
        entrada.pack(side="left")
        return entrada

    def _crear_informacion(self):
        c = self.configuracion
        nivel = NIVELES[c.dificultad]
        pares = (nivel["filas"] * nivel["columnas"]) // 2
        texto = f"{nivel['filas']}×{nivel['columnas']}  ·  {pares} parejas"
        if c.modo == Modo.SOLITARIO:
            texto = texto + f"  ·  {nivel['intentos']} intentos"
        if c.modo == Modo.CONTRA_BOT:
            texto = texto + f"  ·  memoria del bot: {int(nivel['memoria_bot'] * 100)}%"
        tk.Label(self, text=texto, bg=self.tema["fondo"], fg=self.tema["acento"],
                 font=(FUENTE, 11, "bold")).pack(pady=(6, 0))

    def _crear_ayuda(self):
        lineas = ("Voltea dos cartas por intento y encuentra sus parejas.",
                  "Solitario: tienes un número limitado de intentos.",
                  "2 jugadores / Bot: juegan por turnos; si aciertas, repites.",
                  "Gana quien encuentre más parejas.")
        for linea in lineas:
            tk.Label(self, text=linea, bg=self.tema["fondo"], fg=self.tema["suave"],
                     font=(FUENTE, 9)).pack()
        tk.Frame(self, bg=self.tema["fondo"], height=18).pack()

    # ---------------------------------------------------------- eventos
    def _guardar_nombres(self):
        """Guarda en la configuración lo escrito en las casillas de nombre."""
        nombre = self.entrada1.get().strip()
        self.configuracion.nombre1 = nombre if nombre != "" else "Jugador 1"
        if self.entrada2 is not None:
            nombre = self.entrada2.get().strip()
            self.configuracion.nombre2 = nombre if nombre != "" else "Jugador 2"

    def _elegir_modo(self, valor):
        self._guardar_nombres()
        self.configuracion.modo = valor
        self.app.mostrar_menu()

    def _elegir_dificultad(self, valor):
        self._guardar_nombres()
        self.configuracion.dificultad = valor
        self.app.mostrar_menu()

    def _elegir_tema(self, valor):
        self._guardar_nombres()
        self.configuracion.tema = valor
        self.app.mostrar_menu()

    def _elegir_reverso(self, valor):
        self._guardar_nombres()
        self.configuracion.reverso = valor
        self.app.mostrar_menu()

    def _jugar(self):
        self._guardar_nombres()
        self.app.mostrar_juego(None)


class PantallaJuego(tk.Frame):
    """Pantalla donde se juega. Conecta los clics con JuegoMemoria."""

    ANCHO = 580

    MENSAJES_FIJOS = {
        Resultado.YA_DESCUBIERTA: ("Esa carta ya está descubierta", "error"),
        Resultado.MISMA_CARTA: ("Elige una carta diferente", "error"),
        Resultado.PARTIDA_TERMINADA: (
            "La partida terminó. Pulsa Reiniciar para jugar de nuevo.", "info"),
    }

    def __init__(self, raiz, app, configuracion, juego):
        tema = TEMAS[configuracion.tema]
        tk.Frame.__init__(self, raiz, bg=tema["fondo"])
        self.raiz = raiz
        self.app = app
        self.configuracion = configuracion
        self.tema = tema
        if juego is None:
            juego = JuegoMemoria(configuracion)
        self.juego = juego
        self.cartas = {}              # posición -> CartaVisual
        self.ids_after = []           # temporizadores pendientes (para cancelarlos)
        self.primera_posicion = None  # primera carta del intento actual
        self.pos_bot1 = None          # primera carta elegida por el bot
        self.confeti = []

        self._crear_banner()
        self._crear_marcadores()
        self._crear_tablero()
        self._crear_mensajes()
        self._crear_botones()

        self.raiz.bind("<Key-r>", self._al_tecla_r)
        self.raiz.bind("<Key-R>", self._al_tecla_r)

        if self.juego.en_curso():
            if self.juego.es_solitario():
                self._mostrar_mensaje("Haz clic en una carta para empezar.", "info")
            else:
                nombre = self.juego.jugador_actual().nombre
                self._mostrar_mensaje(f"Empieza {nombre}. Haz clic en una carta.", "info")
        else:
            self._mostrar_fin_si_corresponde()
        self._actualizar(False)
        self._programar_bot()

    def destroy(self):
        """Antes de cerrar la pantalla se cancelan los temporizadores y las teclas."""
        self._cancelar_temporizadores()
        try:
            self.raiz.unbind("<Key-r>")
            self.raiz.unbind("<Key-R>")
        except tk.TclError:
            pass
        tk.Frame.destroy(self)

    # ------------------------------------------------------ construcción
    def _crear_banner(self):
        t = self.tema
        self.banner = tk.Canvas(self, width=self.ANCHO, height=52, bg=t["fondo"],
                                highlightthickness=0)
        self.banner.pack(pady=(10, 0))
        self.id_titulo = self.banner.create_text(
            self.ANCHO / 2, 16, text=TITULO, fill=t["texto"], font=(FUENTE, 18, "bold"))
        subtitulo = f"{self.juego.modo}  ·  {self.configuracion.dificultad}"
        self.banner.create_text(self.ANCHO / 2, 38, text=subtitulo, fill=t["suave"],
                                font=(FUENTE, 9))
        self.coleccion = tk.Canvas(self, width=self.ANCHO, height=28, bg=t["fondo"],
                                   highlightthickness=0)
        self.coleccion.pack(pady=(0, 4))

    def _nuevo_panel(self, fila):
        t = self.tema
        panel = tk.Frame(fila, bg=t["panel"], highlightthickness=3,
                         highlightbackground=t["borde"])
        panel.pack(side="left", padx=6)
        return panel

    def _crear_marcadores(self):
        t = self.tema
        fila = tk.Frame(self, bg=t["fondo"])
        fila.pack(pady=(2, 4))
        self.paneles = []   # en 2 jugadores: (panel, etiqueta de parejas)

        if self.juego.es_solitario():
            panel = self._nuevo_panel(fila)
            tk.Label(panel, text="INTENTOS RESTANTES", bg=t["panel"], fg=t["suave"],
                     font=(FUENTE, 9, "bold")).pack(padx=16, pady=(6, 0))
            self.lbl_intentos = tk.Label(panel, bg=t["panel"], fg=t["texto"],
                                         font=(FUENTE, 24, "bold"))
            self.lbl_intentos.pack()
            self.puntos = tk.Canvas(panel, width=self.juego.max_intentos * 15, height=14,
                                    bg=t["panel"], highlightthickness=0)
            self.puntos.pack(padx=14, pady=(0, 8))

            panel = self._nuevo_panel(fila)
            tk.Label(panel, text="PAREJAS", bg=t["panel"], fg=t["suave"],
                     font=(FUENTE, 9, "bold")).pack(padx=30, pady=(6, 0))
            self.lbl_parejas = tk.Label(panel, bg=t["panel"], fg=t["texto"],
                                        font=(FUENTE, 24, "bold"))
            self.lbl_parejas.pack(pady=(0, 14))
        else:
            for jugador in self.juego.jugadores:
                panel = self._nuevo_panel(fila)
                tk.Label(panel, text=jugador.nombre.upper(), bg=t["panel"], fg=t["suave"],
                         font=(FUENTE, 10, "bold"), width=14).pack(padx=12, pady=(6, 0))
                etiqueta = tk.Label(panel, bg=t["panel"], fg=t["texto"],
                                    font=(FUENTE, 24, "bold"))
                etiqueta.pack()
                tk.Label(panel, text="parejas", bg=t["panel"], fg=t["suave"],
                         font=(FUENTE, 9)).pack(pady=(0, 6))
                self.paneles.append((panel, etiqueta))

    def _crear_tablero(self):
        t = self.tema
        marco = tk.Frame(self, bg=t["panel"], highlightthickness=1,
                         highlightbackground=t["borde"])
        marco.pack(pady=6)
        columnas = self.juego.tablero.columnas
        tam = 84 if columnas >= 5 else 90
        for posicion in self.juego.tablero.posiciones():
            fila, columna = posicion
            carta = CartaVisual(marco, self.raiz, posicion, tam, t,
                                self.configuracion.reverso, self._al_hacer_clic)
            carta.grid(row=fila, column=columna, padx=4, pady=4)
            self.cartas[posicion] = carta

    def _crear_mensajes(self):
        t = self.tema
        marco = tk.Frame(self, bg=t["panel"], highlightthickness=1,
                         highlightbackground=t["borde"])
        marco.pack(padx=24, pady=(4, 6), fill="x")
        self.lbl_mensaje = tk.Label(marco, text="", bg=t["panel"], fg=t["info"],
                                    font=(FUENTE, 12, "bold"), wraplength=480, height=2)
        self.lbl_mensaje.pack(padx=12, pady=4)

    def _crear_botones(self):
        fila = tk.Frame(self, bg=self.tema["fondo"])
        fila.pack(pady=(2, 14))
        Boton(fila, "↻  Reiniciar (R)", self._reiniciar, self.tema, True).pack(side="left", padx=5)
        Boton(fila, "Cambiar tema", self._cambiar_tema, self.tema).pack(side="left", padx=5)
        Boton(fila, "Menú", self._volver_menu, self.tema).pack(side="left", padx=5)

    # -------------------------------------------------------- temporizadores
    def _despues(self, milisegundos, funcion, *argumentos):
        """Programa una función para más tarde y guarda su id para poder cancelarla."""
        id_after = self.raiz.after(milisegundos, funcion, *argumentos)
        self.ids_after.append(id_after)
        return id_after

    def _cancelar_temporizadores(self):
        for id_after in self.ids_after:
            self.raiz.after_cancel(id_after)
        self.ids_after = []

    # ------------------------------------------------------------- eventos
    def _al_hacer_clic(self, posicion):
        """Clic de una persona sobre una carta."""
        if self.juego.en_curso() and self.juego.turno_es_bot() and not self.juego.bloqueado:
            self._mostrar_mensaje("Es el turno del Bot. Espera un momento...", "info")
            return
        self._jugar(posicion)

    def _jugar(self, posicion):
        """Envía una jugada (de persona o de bot) al juego y muestra el resultado."""
        jugador = self.juego.jugador_actual()
        resultado = self.juego.seleccionar(posicion)
        if resultado == Resultado.BLOQUEADO:
            return resultado    # durante la espera, los clics se ignoran

        solitario = self.juego.es_solitario()
        par = None
        if resultado == Resultado.PRIMERA_CARTA:
            self.primera_posicion = posicion
            if solitario:
                self._mostrar_mensaje("Elige la segunda carta.", "info")
            else:
                self._mostrar_mensaje(f"{jugador.nombre}: elige la segunda carta.", "info")
        elif resultado == Resultado.PAREJA:
            par = [self.primera_posicion, posicion]
            self.primera_posicion = None
            nombre, _, explicacion = CONCEPTOS[self.juego.tablero.obtener_carta(posicion).simbolo]
            quien = "Pareja encontrada" if solitario else f"{jugador.nombre} encontró una pareja"
            self._mostrar_mensaje(f"{quien} · {nombre}: {explicacion}", "ok")
        elif resultado == Resultado.NO_PAREJA:
            par = [self.primera_posicion, posicion]
            self.primera_posicion = None
            if solitario:
                self._mostrar_mensaje("No coinciden. Memoriza las posiciones.", "error")
            else:
                siguiente = self.juego.jugador_siguiente().nombre
                self._mostrar_mensaje(f"No coinciden. Turno de {siguiente}.", "error")
            self._despues(450, self._agitar_cartas, par)
            self._despues(self.juego.espera_ms, self._resolver_no_pareja)
        elif resultado in self.MENSAJES_FIJOS:
            texto, color = self.MENSAJES_FIJOS[resultado]
            self._mostrar_mensaje(texto, color)

        self._mostrar_fin_si_corresponde()
        self._actualizar(True)

        if resultado == Resultado.PAREJA:
            for p in par:
                self.cartas[p].brillar(3)
            if not self.juego.en_curso():
                self._celebrar()
        return resultado

    def _agitar_cartas(self, par):
        for posicion in par:
            self.cartas[posicion].agitar()

    def _resolver_no_pareja(self):
        """Pasado el tiempo de espera, las cartas se voltean y puede cambiar el turno."""
        self.juego.ocultar_pendientes()
        self._actualizar(True)
        self._programar_bot()

    def _reiniciar(self):
        self._cancelar_temporizadores()
        self.juego.reiniciar()
        self.primera_posicion = None
        self.banner.delete("confeti")
        self.banner.itemconfigure(self.id_titulo, text=TITULO, fill=self.tema["texto"])
        if self.juego.es_solitario():
            self._mostrar_mensaje("Nueva partida. ¡Mucha suerte!", "info")
        else:
            nombre = self.juego.jugador_actual().nombre
            self._mostrar_mensaje(f"Nueva partida. Empieza {nombre}.", "info")
        self._actualizar(True)
        self._programar_bot()

    def _al_tecla_r(self, evento):
        self._reiniciar()

    def _cambiar_tema(self):
        """Pasa al siguiente tema y vuelve a construir la pantalla con sus colores."""
        if self.juego.bloqueado:
            self.juego.ocultar_pendientes()
        posicion = NOMBRES_TEMAS.index(self.configuracion.tema)
        self.configuracion.tema = NOMBRES_TEMAS[(posicion + 1) % len(NOMBRES_TEMAS)]
        self.app.mostrar_juego(self.juego)

    def _volver_menu(self):
        self.app.mostrar_menu()

    # ----------------------------------------------------------------- bot
    def _programar_bot(self):
        """Si es el turno del bot, programa su jugada."""
        if self.juego.en_curso() and self.juego.turno_es_bot() and not self.juego.bloqueado:
            self._despues(800, self._bot_primera)

    def _bot_primera(self):
        bot = self.juego.bot
        self.pos_bot1 = bot.elegir_primera(self.juego.tablero)
        self._jugar(self.pos_bot1)
        self._despues(700, self._bot_segunda)

    def _bot_segunda(self):
        bot = self.juego.bot
        posicion = bot.elegir_segunda(self.juego.tablero, self.pos_bot1)
        resultado = self._jugar(posicion)
        if resultado == Resultado.PAREJA:
            self._programar_bot()       # acertó: el bot repite turno

    # --------------------------------------------------------------- dibujo
    def _actualizar(self, animar):
        """Redibuja marcadores, colección y cartas con el estado del juego."""
        self._dibujar_marcadores()
        self._dibujar_coleccion()
        interactiva = (self.juego.en_curso() and not self.juego.bloqueado
                       and not self.juego.turno_es_bot())
        for posicion, visual in self.cartas.items():
            carta = self.juego.tablero.obtener_carta(posicion)
            modo = self._modo_de(carta)
            if animar:
                visual.actualizar(modo, carta.simbolo, interactiva)
            else:
                visual.fijar(modo, carta.simbolo, interactiva)

    def _modo_de(self, carta):
        """Traduce el estado de una Carta a cómo debe verse."""
        if carta.esta_emparejada():
            return "emparejada"
        if not carta.esta_oculta():
            return "visible"
        if self.juego.estado == EstadoPartida.PERDIDA and not self.juego.bloqueado:
            return "revelada"
        return "oculta"

    def _dibujar_marcadores(self):
        t = self.tema
        juego = self.juego
        if juego.es_solitario():
            restantes = juego.intentos_restantes
            urgente = restantes <= 3
            self.lbl_intentos.configure(text=str(restantes),
                                        fg=t["error"] if urgente else t["texto"])
            self.puntos.delete("all")
            for i in range(juego.max_intentos):
                x = i * 15 + 1
                if i < restantes:
                    color = t["error"] if urgente else t["acento"]
                    self.puntos.create_oval(x, 1, x + 11, 12, fill=color, outline=color)
                else:
                    self.puntos.create_oval(x, 1, x + 11, 12, outline=t["borde"], width=2)
            self.lbl_parejas.configure(
                text=f"{juego.parejas_encontradas()} / {juego.tablero.total_parejas()}")
        else:
            for i in range(len(self.paneles)):
                panel, etiqueta = self.paneles[i]
                etiqueta.configure(text=str(juego.jugadores[i].parejas))
                es_su_turno = juego.en_curso() and juego.turno == i
                panel.configure(highlightbackground=t["acento"] if es_su_turno else t["borde"])

    def _dibujar_coleccion(self):
        """Una casilla por concepto: se ilumina cuando se encuentra su pareja."""
        t = self.tema
        encontrados = []
        for posicion in self.cartas:
            carta = self.juego.tablero.obtener_carta(posicion)
            if carta.esta_emparejada() and carta.simbolo not in encontrados:
                encontrados.append(carta.simbolo)
        self.coleccion.delete("all")
        simbolos = self.juego.tablero.simbolos_usados
        ancho_total = len(simbolos) * 28 - 6
        x0 = (self.ANCHO - ancho_total) / 2
        for i, clave in enumerate(simbolos):
            x = x0 + i * 28
            if clave in encontrados:
                color = CONCEPTOS[clave][1]
                rect_redondeado(self.coleccion, x, 3, x + 22, 25, 5, fill=color, outline=color)
                dibujar_icono(self.coleccion, clave, x + 11, 14, 15, t["oscuro"])
            else:
                rect_redondeado(self.coleccion, x, 3, x + 22, 25, 5,
                                fill=t["panel"], outline=t["borde"])
                self.coleccion.create_text(x + 11, 14, text="?", fill=t["suave"],
                                           font=(FUENTE, 9, "bold"))

    def _mostrar_mensaje(self, texto, clave_color):
        self.lbl_mensaje.configure(text=texto, fg=self.tema[clave_color])

    def _mostrar_fin_si_corresponde(self):
        """Mensajes de victoria, derrota o resultado final."""
        juego = self.juego
        total = juego.tablero.total_parejas()
        if juego.estado == EstadoPartida.GANADA:
            self._mostrar_mensaje(
                f"¡Ganaste! Encontraste las {total} parejas en {juego.intentos_usados()} intentos.", "ok")
        elif juego.estado == EstadoPartida.PERDIDA:
            self._mostrar_mensaje(
                f"Perdiste. Se acabaron los intentos. Encontraste "
                f"{juego.parejas_encontradas()} de {total} parejas.", "error")
        elif juego.estado == EstadoPartida.FINALIZADA:
            ganador = juego.ganador()
            if ganador is None:
                self._mostrar_mensaje(
                    f"¡Empate! Cada jugador encontró {juego.jugadores[0].parejas} parejas.", "info")
            else:
                if ganador is juego.jugadores[0]:
                    otro = juego.jugadores[1]
                else:
                    otro = juego.jugadores[0]
                self._mostrar_mensaje(
                    f"¡Gana {ganador.nombre}! {ganador.parejas} parejas contra {otro.parejas}.", "ok")

    # --------------------------------------------------------- celebración
    def _celebrar(self):
        """Fin de la partida: ola dorada, título de colores y confeti."""
        posiciones = self.juego.tablero.posiciones()
        for i in range(len(posiciones)):
            self._despues(i * 70, self._brillar_carta, posiciones[i])
        self.banner.itemconfigure(self.id_titulo, text="★  ¡FIN DE LA PARTIDA!  ★")
        self._ciclo_titulo(0)
        self._lanzar_confeti()

    def _brillar_carta(self, posicion):
        self.cartas[posicion].brillar(2)

    def _ciclo_titulo(self, i):
        colores = [datos[1] for datos in CONCEPTOS.values()]
        if self.juego.en_curso():
            return      # se reinició la partida
        self.banner.itemconfigure(self.id_titulo, fill=colores[i % len(colores)])
        self._despues(130, self._ciclo_titulo, i + 1)

    def _lanzar_confeti(self):
        colores = [datos[1] for datos in CONCEPTOS.values()]
        self.confeti = []
        for i in range(45):
            x = random.randint(0, self.ANCHO)
            y = random.randint(-60, 0)
            item = self.banner.create_rectangle(x, y, x + 6, y + 9, fill=random.choice(colores),
                                                outline="", tags="confeti")
            self.confeti.append([item, random.randint(-2, 2), random.randint(3, 7)])
        self._mover_confeti(0)

    def _mover_confeti(self, cuadro):
        if cuadro >= 40:
            self.banner.delete("confeti")
            return
        for particula in self.confeti:
            self.banner.move(particula[0], particula[1], particula[2])
        self._despues(40, self._mover_confeti, cuadro + 1)


class Aplicacion:
    """Ventana principal: cambia entre el menú y la pantalla de juego."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.configuracion = Configuracion()
        self.pantalla = None
        raiz.title("Memoria POO")
        raiz.resizable(False, False)
        self.mostrar_menu()

    def mostrar_menu(self):
        self._quitar_pantalla()
        self._poner_pantalla(MenuInicio(self.raiz, self))

    def mostrar_juego(self, juego):
        """Muestra la pantalla de juego. Si `juego` es None, empieza una partida nueva."""
        self._quitar_pantalla()
        self._poner_pantalla(PantallaJuego(self.raiz, self, self.configuracion, juego))

    def _quitar_pantalla(self):
        if self.pantalla is not None:
            self.pantalla.destroy()
            self.pantalla = None

    def _poner_pantalla(self, pantalla):
        self.pantalla = pantalla
        self.raiz.configure(bg=TEMAS[self.configuracion.tema]["fondo"])
        pantalla.pack()
        self._centrar_ventana()

    def _centrar_ventana(self):
        self.raiz.update_idletasks()
        ancho = self.raiz.winfo_reqwidth()
        alto = self.raiz.winfo_reqheight()
        x = (self.raiz.winfo_screenwidth() - ancho) // 2
        y = (self.raiz.winfo_screenheight() - alto) // 4
        self.raiz.geometry(f"+{max(x, 0)}+{max(y, 0)}")


# =============================================================================
#  PUNTO DE ENTRADA
# =============================================================================

def main():
    raiz = tk.Tk()
    Aplicacion(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()