import tkinter as tk

def sumar():
    try:
        numero_uno = float(txtNumeroUno.get())
        numero_dos = float(txtNumeroDos.get())
        resultado = numero_uno + numero_dos
        print("La suma es", resultado)
    except ValueError:
        print("Por favor ingresa números válidos")

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