"""
MEMORIA POO - Juego de memoria con Python y Tkinter (versión básica)
====================================================================
Las parejas son conceptos de la Programación Orientada a Objetos.

Modos de juego:  Solitario | 2 jugadores
Dificultades:    Fácil (3x4) | Normal (4x4) | Difícil (4x5)
También se pueden cambiar los nombres de los jugadores.

ORGANIZACIÓN DEL ARCHIVO (de arriba hacia abajo)
------------------------------------------------
DATOS               conceptos, iconos, niveles y colores (diccionarios)

PARTE 1 - LÓGICA (no usa Tkinter, no dibuja nada)
    Configuracion   lo que el jugador elige en el menú
    Carta           una carta: su concepto y su estado
    Tablero         el conjunto de cartas (filas x columnas)
    Jugador         nombre y parejas de quien juega
    JuegoMemoria    las REGLAS: turnos, parejas, intentos, fin de la partida

PARTE 2 - INTERFAZ (Tkinter)
    Boton           un botón con colores
    CartaVisual     una carta dibujada en pantalla
    MenuInicio      pantalla donde se eligen las opciones
    PantallaJuego   pantalla donde se juega
    Aplicacion      cambia entre el menú y la pantalla de juego

IDEA CLAVE: la lógica NO sabe nada de ventanas ni colores, y la interfaz NO
decide las reglas. La interfaz le pregunta a JuegoMemoria qué pasó con cada
clic y, según la respuesta, muestra lo que corresponda.
"""

import random
import tkinter as tk


# =============================================================================
#  DATOS (diccionarios con la información del juego)
# =============================================================================

# concepto -> (nombre que se ve, color de la carta, explicación al hacer pareja)
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

# concepto -> icono (un emoji, que en Python es simplemente un texto)
ICONOS = {
    "clase": "📋",             # plantilla
    "objeto": "📦",            # algo concreto
    "herencia": "🌳",          # árbol: padres e hijos
    "polimorfismo": "🎭",      # muchas caras
    "encapsulamiento": "🔒",   # datos protegidos
    "abstraccion": "🔍",       # ver solo lo esencial
    "metodo": "🔧",            # una acción
    "atributo": "🔖",          # etiqueta con un dato
    "constructor": "🔨",       # construye el objeto
    "interfaz": "📜",          # contrato
}

# Cada dificultad: filas, columnas, intentos (solo en solitario) y
# milisegundos que se ven dos cartas que NO coinciden.
NIVELES = {
    "Fácil":   {"filas": 3, "columnas": 4, "intentos": 12, "espera": 1500},
    "Normal":  {"filas": 4, "columnas": 4, "intentos": 14, "espera": 1000},
    "Difícil": {"filas": 4, "columnas": 5, "intentos": 16, "espera": 700},
}

# Colores del juego (un diccionario). Las pantallas los leen con TEMA["clave"].
TEMA = {
    "fondo": "#12142B", "texto": "#EDEFFF", "seleccion": "#3B4488",
    "oculta": "#3B4488", "oculta_texto": "#EDEFFF",
    "boton": "#FFD43B", "boton_texto": "#2B2400",
    "ok": "#5EE08A", "error": "#FF7B7B",
}

TITULO = "{ }  MEMORIA POO"
FUENTE = "Helvetica"
COLOR_LETRA_CARTA = "#1B1E3A"


# =============================================================================
#  PARTE 1 - LÓGICA DEL JUEGO
# =============================================================================

class Configuracion:
    """Guarda lo que el jugador elige en el menú."""

    def __init__(self):
        self.modo = "Solitario"
        self.dificultad = "Normal"
        self.nombre1 = "Jugador 1"
        self.nombre2 = "Jugador 2"


class Carta:
    """Una carta del tablero: guarda su concepto y su estado."""

    def __init__(self, concepto):
        self.concepto = concepto
        self.estado = "oculta"          # "oculta", "visible" o "emparejada"

    def esta_oculta(self):
        return self.estado == "oculta"

    def esta_emparejada(self):
        return self.estado == "emparejada"

    def voltear(self):
        self.estado = "visible"

    def ocultar(self):
        self.estado = "oculta"

    def emparejar(self):
        self.estado = "emparejada"

    def coincide_con(self, otra):
        """True si las dos cartas tienen el mismo concepto."""
        return self.concepto == otra.concepto


class Tablero:
    """Conjunto de cartas organizadas en filas x columnas."""

    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.conceptos_usados = []      # los conceptos elegidos para esta partida
        self.cartas = []                # lista con todas las cartas
        self.mezclar()

    def total_parejas(self):
        return (self.filas * self.columnas) // 2

    def mezclar(self):
        """Elige conceptos al azar, crea 2 cartas de cada uno y las mezcla."""
        todos = list(CONCEPTOS.keys())
        self.conceptos_usados = random.sample(todos, self.total_parejas())
        lista = self.conceptos_usados * 2       # cada concepto aparece 2 veces
        random.shuffle(lista)
        self.cartas = []
        for concepto in lista:
            self.cartas.append(Carta(concepto))

    def obtener_carta(self, fila, columna):
        """Devuelve la carta que está en esa fila y esa columna."""
        return self.cartas[fila * self.columnas + columna]

    def conceptos_emparejados(self):
        """Lista de los conceptos cuya pareja ya se encontró."""
        lista = []
        for carta in self.cartas:
            if carta.esta_emparejada() and carta.concepto not in lista:
                lista.append(carta.concepto)
        return lista


class Jugador:
    """Una persona que juega."""

    def __init__(self, nombre):
        self.nombre = nombre
        self.parejas = 0


class JuegoMemoria:
    """Las reglas del juego. Conoce el estado de la partida.

    No dibuja nada. Cada clic se procesa en seleccionar() y devuelve un texto
    que dice qué pasó: "primera", "pareja", "no_pareja", "invalida",
    "bloqueado" o "terminada".
    """

    def __init__(self, configuracion):
        nivel = NIVELES[configuracion.dificultad]
        self.modo = configuracion.modo
        self.tablero = Tablero(nivel["filas"], nivel["columnas"])
        self.max_intentos = nivel["intentos"]
        self.espera = nivel["espera"]

        self.jugadores = [Jugador(configuracion.nombre1)]
        if self.modo == "2 jugadores":
            self.jugadores.append(Jugador(configuracion.nombre2))
        self.reiniciar()

    # ------------------------------------------------------------ estado
    def reiniciar(self):
        """Deja la partida como nueva."""
        self.tablero.mezclar()
        for jugador in self.jugadores:
            jugador.parejas = 0
        self.turno = 0                                  # índice del jugador que juega
        self.primera = None                             # primera carta del intento
        self.segunda = None                             # segunda carta del intento
        self.intentos_restantes = self.max_intentos     # solo cuenta en solitario
        self.bloqueado = False                          # True mientras se ven 2 cartas distintas
        self.estado = "en curso"                        # "en curso", "ganada", "perdida", "finalizada"

    def en_curso(self):
        return self.estado == "en curso"

    def es_solitario(self):
        return self.modo == "Solitario"

    def jugador_actual(self):
        return self.jugadores[self.turno]

    def jugador_siguiente(self):
        return self.jugadores[(self.turno + 1) % len(self.jugadores)]

    def parejas_encontradas(self):
        total = 0
        for jugador in self.jugadores:
            total = total + jugador.parejas
        return total

    def intentos_usados(self):
        return self.max_intentos - self.intentos_restantes

    def ganador(self):
        """En 2 jugadores: devuelve al ganador, o None si hay empate."""
        a = self.jugadores[0]
        b = self.jugadores[1]
        if a.parejas > b.parejas:
            return a
        if b.parejas > a.parejas:
            return b
        return None

    # ------------------------------------------------------------ reglas
    def seleccionar(self, fila, columna):
        """Procesa el clic sobre una carta y devuelve qué pasó."""
        if not self.en_curso():
            return "terminada"
        if self.bloqueado:
            return "bloqueado"

        carta = self.tablero.obtener_carta(fila, columna)
        if not carta.esta_oculta():
            return "invalida"           # ya estaba boca arriba: no cambia nada

        carta.voltear()

        # Primera carta del intento
        if self.primera is None:
            self.primera = carta
            return "primera"

        # Segunda carta: aquí se cuenta el intento
        jugador = self.jugador_actual()
        if self.es_solitario():
            self.intentos_restantes = self.intentos_restantes - 1

        if self.primera.coincide_con(carta):
            self.primera.emparejar()
            carta.emparejar()
            jugador.parejas = jugador.parejas + 1       # el jugador repite turno
            self.primera = None
            self._comprobar_fin()
            return "pareja"

        # No coinciden: se bloquea el tablero hasta llamar a ocultar_pendientes()
        self.segunda = carta
        self.bloqueado = True
        self._comprobar_fin()
        return "no_pareja"

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
                self.estado = "ganada"
            else:
                self.estado = "finalizada"
        elif self.es_solitario() and self.intentos_restantes == 0:
            self.estado = "perdida"


# =============================================================================
#  PARTE 2 - INTERFAZ GRÁFICA (Tkinter)
# =============================================================================

class Boton(tk.Label):
    """Botón hecho con un Label (así los colores se ven igual en todos los sistemas).

    HEREDA de tk.Label: un Boton "es un" Label, pero además hace algo al hacer clic.
    """

    def __init__(self, padre, texto, comando, tema, principal=False):
        if principal:
            fondo = tema["boton"]
            letra = tema["boton_texto"]
        else:
            fondo = tema["seleccion"]
            letra = tema["texto"]
        tk.Label.__init__(self, padre, text=texto, bg=fondo, fg=letra,
                          font=(FUENTE, 12, "bold"), padx=20, pady=6, cursor="hand2")
        self.comando = comando
        self.bind("<Button-1>", self._al_pulsar)

    def _al_pulsar(self, evento):
        self.comando()


class CartaVisual:
    """Una carta dibujada en pantalla.

    Es un Frame (el marco de la carta) con dos Label dentro:
    uno grande para el icono y otro pequeño para el nombre.
    No conoce las reglas: la pantalla le dice cómo debe verse con mostrar().
    """

    def __init__(self, padre, fila, columna, pantalla):
        self.fila = fila
        self.columna = columna
        self.pantalla = pantalla
        self.marco = tk.Frame(padre, bd=3, cursor="hand2")
        self.marco.grid(row=fila, column=columna, padx=4, pady=4)
        self.icono = tk.Label(self.marco, width=5, font=(FUENTE, 24))
        self.icono.pack(fill="x", pady=(6, 0))
        self.nombre = tk.Label(self.marco, width=17, font=(FUENTE, 9, "bold"))
        self.nombre.pack(fill="x", pady=(0, 6))
        # El clic puede caer sobre el marco o sobre cualquiera de los dos Label
        for pieza in (self.marco, self.icono, self.nombre):
            pieza.bind("<Button-1>", self._al_pulsar)

    def _al_pulsar(self, evento):
        self.pantalla.al_hacer_clic(self.fila, self.columna)

    def mostrar(self, carta, tema, revelar):
        """Pinta la carta según su estado. `revelar` es True cuando se pierde."""
        nombre, color, _ = CONCEPTOS[carta.concepto]
        icono = ICONOS[carta.concepto]
        if carta.esta_oculta() and not revelar:
            icono, texto, fondo, letra, relieve = "?", "", tema["oculta"], tema["oculta_texto"], "raised"
        elif carta.esta_oculta():
            texto, fondo, letra, relieve = nombre, tema["oculta"], color, "flat"
        elif carta.esta_emparejada():
            texto, fondo, letra, relieve = nombre + " ✔", color, COLOR_LETRA_CARTA, "sunken"
        else:
            texto, fondo, letra, relieve = nombre, color, COLOR_LETRA_CARTA, "raised"
        self.marco.configure(bg=fondo, relief=relieve)
        self.icono.configure(text=icono, bg=fondo, fg=letra)
        self.nombre.configure(text=texto, bg=fondo, fg=letra)


class MenuInicio:
    """Pantalla de inicio: se elige modo, dificultad y nombres."""

    def __init__(self, raiz, app):
        self.app = app
        self.configuracion = app.configuracion
        self.tema = TEMA
        c = self.configuracion
        t = self.tema

        self.marco = tk.Frame(raiz, bg=t["fondo"])
        self.marco.pack(padx=40, pady=20)

        # Variables de Tkinter: guardan la opción elegida en cada selector
        self.var_modo = tk.StringVar(value=c.modo)
        self.var_dificultad = tk.StringVar(value=c.dificultad)
        self.entrada1 = None
        self.entrada2 = None

        self._crear_titulo()
        self._crear_selector("MODO DE JUEGO", self.var_modo, ("Solitario", "2 jugadores"))
        self._crear_selector("DIFICULTAD", self.var_dificultad, tuple(NIVELES.keys()))
        self._crear_nombres()
        self._crear_informacion()
        Boton(self.marco, "▶  JUGAR", self._jugar, t, True).pack(pady=(14, 6))
        self._crear_ayuda()

    def cerrar(self):
        self.marco.destroy()

    def _crear_titulo(self):
        t = self.tema
        tk.Label(self.marco, text=TITULO, bg=t["fondo"], fg=t["texto"],
                 font=(FUENTE, 26, "bold")).pack(pady=(0, 2))
        tk.Label(self.marco, text="Empareja los conceptos de la Programación Orientada a Objetos",
                 bg=t["fondo"], fg=t["texto"], font=(FUENTE, 10)).pack(pady=(0, 10))
        # Fila decorativa: un cuadrito de color por cada concepto
        fila = tk.Frame(self.marco, bg=t["fondo"])
        fila.pack()
        for clave in CONCEPTOS:
            color = CONCEPTOS[clave][1]
            tk.Label(fila, text=ICONOS[clave], bg=color, width=3,
                     font=(FUENTE, 14)).pack(side="left", padx=2)

    def _crear_selector(self, titulo, variable, opciones):
        """Un título y una fila de opciones para elegir una."""
        t = self.tema
        tk.Label(self.marco, text=titulo, bg=t["fondo"], fg=t["texto"],
                 font=(FUENTE, 9, "bold")).pack(pady=(10, 2))
        fila = tk.Frame(self.marco, bg=t["fondo"])
        fila.pack()
        for opcion in opciones:
            tk.Radiobutton(fila, text=opcion, value=opcion, variable=variable,
                           indicatoron=False, command=self._al_elegir,
                           bg=t["fondo"], fg=t["texto"], selectcolor=t["seleccion"],
                           activebackground=t["seleccion"], activeforeground=t["texto"],
                           font=(FUENTE, 11, "bold"), padx=12, pady=4,
                           bd=0, highlightthickness=0).pack(side="left", padx=3)

    def _crear_nombres(self):
        c = self.configuracion
        t = self.tema
        fila = tk.Frame(self.marco, bg=t["fondo"])
        fila.pack(pady=(12, 2))
        tk.Label(fila, text="Jugador 1:", bg=t["fondo"], fg=t["texto"],
                 font=(FUENTE, 10, "bold")).pack(side="left", padx=(0, 4))
        self.entrada1 = self._nueva_entrada(fila, c.nombre1)
        if c.modo == "2 jugadores":
            tk.Label(fila, text="Jugador 2:", bg=t["fondo"], fg=t["texto"],
                     font=(FUENTE, 10, "bold")).pack(side="left", padx=(14, 4))
            self.entrada2 = self._nueva_entrada(fila, c.nombre2)

    def _nueva_entrada(self, padre, texto):
        entrada = tk.Entry(padre, width=13, font=(FUENTE, 11), justify="center")
        entrada.insert(0, texto)
        entrada.pack(side="left")
        return entrada

    def _crear_informacion(self):
        c = self.configuracion
        nivel = NIVELES[c.dificultad]
        pares = (nivel["filas"] * nivel["columnas"]) // 2
        texto = f"{nivel['filas']}×{nivel['columnas']}  ·  {pares} parejas"
        if c.modo == "Solitario":
            texto = texto + f"  ·  {nivel['intentos']} intentos"
        tk.Label(self.marco, text=texto, bg=self.tema["fondo"], fg=self.tema["boton"],
                 font=(FUENTE, 11, "bold")).pack(pady=(10, 0))

    def _crear_ayuda(self):
        lineas = ("Voltea dos cartas por intento y encuentra sus parejas.",
                  "Solitario: tienes un número limitado de intentos.",
                  "2 jugadores: juegan por turnos; si aciertas, repites.",
                  "Gana quien encuentre más parejas.")
        for linea in lineas:
            tk.Label(self.marco, text=linea, bg=self.tema["fondo"], fg=self.tema["texto"],
                     font=(FUENTE, 9)).pack()

    # ---------------------------------------------------------- eventos
    def _guardar_opciones(self):
        """Guarda en la configuración todo lo que el jugador eligió o escribió."""
        c = self.configuracion
        c.modo = self.var_modo.get()
        c.dificultad = self.var_dificultad.get()
        nombre = self.entrada1.get().strip()
        if nombre != "":
            c.nombre1 = nombre
        else:
            c.nombre1 = "Jugador 1"
        if self.entrada2 is not None:
            nombre = self.entrada2.get().strip()
            if nombre != "":
                c.nombre2 = nombre
            else:
                c.nombre2 = "Jugador 2"

    def _al_elegir(self):
        """Al cambiar una opción se guarda todo y se vuelve a dibujar el menú."""
        self._guardar_opciones()
        self.app.mostrar_menu()

    def _jugar(self):
        self._guardar_opciones()
        self.app.mostrar_juego()


class PantallaJuego:
    """Pantalla donde se juega. Conecta los clics con JuegoMemoria."""

    def __init__(self, raiz, app, configuracion):
        self.raiz = raiz
        self.app = app
        self.configuracion = configuracion
        self.tema = TEMA
        self.juego = JuegoMemoria(configuracion)
        self.id_after = None        # temporizador pendiente (para poder cancelarlo)
        self.cartas = []            # lista de CartaVisual
        self.coleccion = {}         # concepto -> Label de la barra de colección

        t = self.tema
        self.marco = tk.Frame(raiz, bg=t["fondo"])
        self.marco.pack(padx=20, pady=10)

        self._crear_titulo()
        self._crear_marcadores()
        self._crear_tablero()
        self._crear_mensaje()
        self._crear_botones()

        if self.juego.es_solitario():
            self._mostrar_mensaje("Haz clic en una carta para empezar.", "texto")
        else:
            nombre = self.juego.jugador_actual().nombre
            self._mostrar_mensaje(f"Empieza {nombre}. Haz clic en una carta.", "texto")
        self.actualizar()

    def cerrar(self):
        """Antes de cerrar la pantalla se cancela el temporizador pendiente."""
        if self.id_after is not None:
            self.raiz.after_cancel(self.id_after)
            self.id_after = None
        self.marco.destroy()

    # ------------------------------------------------------ construcción
    def _crear_titulo(self):
        t = self.tema
        tk.Label(self.marco, text=TITULO, bg=t["fondo"], fg=t["texto"],
                 font=(FUENTE, 18, "bold")).pack()
        subtitulo = f"{self.juego.modo}  ·  {self.configuracion.dificultad}"
        tk.Label(self.marco, text=subtitulo, bg=t["fondo"], fg=t["texto"],
                 font=(FUENTE, 9)).pack()

        # Barra de colección: un cuadrito por concepto, se ilumina al hacer pareja
        fila = tk.Frame(self.marco, bg=t["fondo"])
        fila.pack(pady=6)
        for concepto in self.juego.tablero.conceptos_usados:
            etiqueta = tk.Label(fila, text="?", width=3, font=(FUENTE, 12, "bold"))
            etiqueta.pack(side="left", padx=2)
            self.coleccion[concepto] = etiqueta

    def _crear_marcadores(self):
        t = self.tema
        fila = tk.Frame(self.marco, bg=t["fondo"])
        fila.pack(pady=4)
        if self.juego.es_solitario():
            self.lbl_intentos = tk.Label(fila, bg=t["fondo"], fg=t["texto"],
                                         font=(FUENTE, 14, "bold"))
            self.lbl_intentos.pack(side="left", padx=15)
            self.lbl_parejas = tk.Label(fila, bg=t["fondo"], fg=t["texto"],
                                        font=(FUENTE, 14, "bold"))
            self.lbl_parejas.pack(side="left", padx=15)
        else:
            self.lbl_jugadores = []     # una etiqueta por jugador
            for jugador in self.juego.jugadores:
                etiqueta = tk.Label(fila, bg=t["fondo"], fg=t["texto"],
                                    font=(FUENTE, 14, "bold"))
                etiqueta.pack(side="left", padx=15)
                self.lbl_jugadores.append(etiqueta)

    def _crear_tablero(self):
        t = self.tema
        marco = tk.Frame(self.marco, bg=t["fondo"])
        marco.pack(pady=6)
        tablero = self.juego.tablero
        for fila in range(tablero.filas):
            for columna in range(tablero.columnas):
                self.cartas.append(CartaVisual(marco, fila, columna, self))

    def _crear_mensaje(self):
        t = self.tema
        self.lbl_mensaje = tk.Label(self.marco, text="", bg=t["fondo"], fg=t["texto"],
                                    font=(FUENTE, 12, "bold"), wraplength=480, height=2)
        self.lbl_mensaje.pack(pady=4)

    def _crear_botones(self):
        fila = tk.Frame(self.marco, bg=self.tema["fondo"])
        fila.pack(pady=(2, 10))
        Boton(fila, "↻  Reiniciar", self._reiniciar, self.tema, True).pack(side="left", padx=5)
        Boton(fila, "Menú", self._volver_menu, self.tema).pack(side="left", padx=5)

    # ------------------------------------------------------------- eventos
    def al_hacer_clic(self, fila, columna):
        """Lo llama una CartaVisual cuando le hacen clic."""
        jugador = self.juego.jugador_actual()
        resultado = self.juego.seleccionar(fila, columna)
        solitario = self.juego.es_solitario()

        if resultado == "primera":
            if solitario:
                self._mostrar_mensaje("Elige la segunda carta.", "texto")
            else:
                self._mostrar_mensaje(f"{jugador.nombre}: elige la segunda carta.", "texto")
        elif resultado == "pareja":
            concepto = self.juego.tablero.obtener_carta(fila, columna).concepto
            nombre, _, explicacion = CONCEPTOS[concepto]
            if solitario:
                quien = "Pareja encontrada"
            else:
                quien = f"{jugador.nombre} encontró una pareja"
            self._mostrar_mensaje(f"{quien} · {nombre}: {explicacion}", "ok")
        elif resultado == "no_pareja":
            if solitario:
                self._mostrar_mensaje("No coinciden. Memoriza las posiciones.", "error")
            else:
                siguiente = self.juego.jugador_siguiente().nombre
                self._mostrar_mensaje(f"No coinciden. Turno de {siguiente}.", "error")
            # Pasado el tiempo de espera, las dos cartas se vuelven a ocultar
            self.id_after = self.raiz.after(self.juego.espera, self._ocultar)
        elif resultado == "invalida":
            self._mostrar_mensaje("Esa carta ya está descubierta.", "error")
        # "bloqueado": durante la espera los clics se ignoran

        self._mostrar_fin()     # no hace nada si la partida sigue en curso
        self.actualizar()

    def _ocultar(self):
        """Se ejecuta cuando termina la espera: voltea las cartas y cambia el turno."""
        self.id_after = None
        self.juego.ocultar_pendientes()
        self.actualizar()

    def _reiniciar(self):
        if self.id_after is not None:
            self.raiz.after_cancel(self.id_after)
            self.id_after = None
        self.juego.reiniciar()
        if self.juego.es_solitario():
            self._mostrar_mensaje("Nueva partida. ¡Mucha suerte!", "texto")
        else:
            nombre = self.juego.jugador_actual().nombre
            self._mostrar_mensaje(f"Nueva partida. Empieza {nombre}.", "texto")
        self.actualizar()

    def _volver_menu(self):
        self.app.mostrar_menu()

    # --------------------------------------------------------------- dibujo
    def actualizar(self):
        """Redibuja marcadores, colección y cartas con el estado del juego."""
        juego = self.juego
        t = self.tema

        # Marcadores
        if juego.es_solitario():
            restantes = juego.intentos_restantes
            if restantes <= 3:
                color = t["error"]
            else:
                color = t["texto"]
            self.lbl_intentos.configure(text=f"Intentos restantes: {restantes}", fg=color)
            self.lbl_parejas.configure(
                text=f"Parejas: {juego.parejas_encontradas()} / {juego.tablero.total_parejas()}")
        else:
            for i in range(len(juego.jugadores)):
                jugador = juego.jugadores[i]
                if juego.en_curso() and juego.turno == i:
                    color = t["boton"]          # resalta a quien le toca
                else:
                    color = t["texto"]
                self.lbl_jugadores[i].configure(
                    text=f"{jugador.nombre}: {jugador.parejas}", fg=color)

        # Barra de colección
        encontrados = juego.tablero.conceptos_emparejados()
        for concepto in self.coleccion:
            etiqueta = self.coleccion[concepto]
            if concepto in encontrados:
                color = CONCEPTOS[concepto][1]
                etiqueta.configure(text=ICONOS[concepto], bg=color, fg=COLOR_LETRA_CARTA)
            else:
                etiqueta.configure(text="?", bg=t["oculta"], fg=t["oculta_texto"])

        # Cartas (si se perdió y ya no hay cartas esperando, se muestran todas)
        revelar = juego.estado == "perdida" and not juego.bloqueado
        for visual in self.cartas:
            carta = juego.tablero.obtener_carta(visual.fila, visual.columna)
            visual.mostrar(carta, t, revelar)

    def _mostrar_mensaje(self, texto, clave_color):
        self.lbl_mensaje.configure(text=texto, fg=self.tema[clave_color])

    def _mostrar_fin(self):
        """Mensajes de victoria, derrota o resultado final (si la partida terminó)."""
        juego = self.juego
        total = juego.tablero.total_parejas()
        if juego.estado == "ganada":
            self._mostrar_mensaje(
                f"¡Ganaste! Encontraste las {total} parejas en {juego.intentos_usados()} intentos.",
                "ok")
        elif juego.estado == "perdida":
            self._mostrar_mensaje(
                f"Perdiste. Se acabaron los intentos. "
                f"Encontraste {juego.parejas_encontradas()} de {total} parejas.", "error")
        elif juego.estado == "finalizada":
            ganador = juego.ganador()
            if ganador is None:
                self._mostrar_mensaje(
                    f"¡Empate! Cada jugador encontró {juego.jugadores[0].parejas} parejas.",
                    "texto")
            else:
                if ganador is juego.jugadores[0]:
                    otro = juego.jugadores[1]
                else:
                    otro = juego.jugadores[0]
                self._mostrar_mensaje(
                    f"¡Gana {ganador.nombre}! {ganador.parejas} parejas contra {otro.parejas}.",
                    "ok")


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
        self.raiz.configure(bg=TEMA["fondo"])
        self.pantalla = MenuInicio(self.raiz, self)

    def mostrar_juego(self):
        """Muestra la pantalla de juego con una partida nueva."""
        self._quitar_pantalla()
        self.raiz.configure(bg=TEMA["fondo"])
        self.pantalla = PantallaJuego(self.raiz, self, self.configuracion)

    def _quitar_pantalla(self):
        if self.pantalla is not None:
            self.pantalla.cerrar()
            self.pantalla = None


# =============================================================================
#  PUNTO DE ENTRADA
# =============================================================================

def main():
    raiz = tk.Tk()
    Aplicacion(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()