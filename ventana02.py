import tkinter as tk
from tkinter import messagebox
    
def sumar():
    a = int(txtNumUno.get())
    b = int(txtNumDos.get())
    lblResultado.config(text=f"Resultado: {a+b}")

def restar():
    a = int(txtNumUno.get())
    b = int(txtNumDos.get())
    lblResultado.config(text=f"Resultado: {a-b}")

def multiplicar():
    a = int(txtNumUno.get())
    b = int(txtNumDos.get())
    lblResultado.config(text=f"Resultado: {a*b}")

def dividir():
    a = int(txtNumUno.get())
    b = int(txtNumDos.get())
    if b == 0:
        messagebox.showerror(message="No se puede dividir entre 0")
    else:
        lblResultado.config(text=f"Resultado: {a/b}")

ventana = tk.Tk()
ventana.title("Calculadora POO")
ventana.geometry("300x200+500+100")
ventana.resizable(False, False)

lblNumUno = tk.Label(ventana, text="Numero Uno", font=100)
lblNumDos = tk.Label(ventana, text="Numero Dos", font=100)
lblResultado = tk.Label(ventana, text="Resultado:", font=200, background="Green", padx=20, pady=5, fg="white")

txtNumUno = tk.Entry(ventana, width=25)
txtNumDos = tk.Entry(ventana, width=25)

btnSumar = tk.Button(ventana, text="Sumar", width=16, command=sumar)
btnRestar = tk.Button(ventana, text="Restar", width=16, command=restar)
btnMultiplicar = tk.Button(ventana, text="Multiplicar", width=16, command=multiplicar)
btnDividir = tk.Button(ventana, text="Dividir", width=16, command=dividir)

lblNumUno.grid(row=0, column=0, padx=5, pady=5)
txtNumUno.grid(row=0, column=1, padx=5, pady=5)

lblNumDos.grid(row=1, column=0, padx=5, pady=5)
txtNumDos.grid(row=1, column=1, padx=5, pady=5)

btnSumar.grid(row=2, column=0, padx=5, pady=5)
btnRestar.grid(row=2, column=1, padx=5, pady=5)
btnMultiplicar.grid(row=3, column=0, padx=5, pady=5)
btnDividir.grid(row=3, column=1, padx=5, pady=5)

lblResultado.grid(row=4, column=0, padx=5, pady=10, columnspan=2)

ventana.mainloop()