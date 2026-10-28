import tkinter as tk

def sumar():
    print("La suma es")

ventana = tk.Tk()
ventana.title("Suma de numeros")
ventana.geometry("300x300")

txtNumeroUno = tk.Entry(ventana, width=10)
txtNumeroDos = tk.Entry(ventana, width=10)

txtNumeroUno.pack(pady=10)
txtNumeroDos.pack(pady=15)

btnSumar = tk.Button(ventana, text="Sumar", command=sumar)
btnSumar.pack(pady=20)

ventana.mainloop()