import random
import tkinter as tk

PALABRAS = ["Clase", "Objeto", "Herencia", "Polimorfismo", "Encapsulamiento", "Abstracción"]

raiz = tk.Tk()
raiz.title("Memoria")

cartas = PALABRAS * 2
random.shuffle(cartas)

primera = None    
bloqueo = False 

def voltear(i):
    global primera, bloqueo
    if bloqueo or botones[i]["text"] != "?":  
        return
    botones[i].config(text=cartas[i])         
    if primera is None:
        primera = i                           
    elif cartas[primera] == cartas[i]:
        primera = None                       
    else:
        bloqueo = True                       
        raiz.after(1000, ocultar, primera, i)
        primera = None


def ocultar(a, b):
    global bloqueo
    botones[a].config(text="?")
    botones[b].config(text="?")
    bloqueo = False


botones = []
for fila in range(3):
    for columna in range(4):
        i = fila * 4 + columna
        b = tk.Button(raiz, text="?", width=16, height=3, font=("H", 12),
                      command=lambda i=i: voltear(i))
        b.grid(row=fila, column=columna, padx=3, pady=3)
        botones.append(b)

raiz.mainloop()