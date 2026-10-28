import tkinter as tk

def click():
    print("El ususario se llama", texto.get())

# Creacion ventana
ventana= tk.Tk()
ventana.title("Mi primer juego")
ventana.geometry("300x300")
# Creacion boton
boton = tk.Button(ventana, text="Mi primer boton", command=click)
boton.pack()
boton.place(x=100, y=500)
# Creacion caja de texto
texto = tk.Entry(ventana, width=30)
texto.pack(pady=30)

ventana.mainloop()