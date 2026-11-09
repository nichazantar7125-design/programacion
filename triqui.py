import tkinter as tk

def marcar(boton):
    mark = "X"
    if boton == 0:
        b0.config(text=mark)
    elif boton == 1:
        b1.config(text=mark)
    elif boton == 2:
        b2.config(text=mark)
    elif boton == 3:
        b3.config(text=mark)
    elif boton == 4:
        b4.config(text=mark)
    elif boton == 5:
        b5.config(text=mark)
    elif boton == 6:
        b6.config(text=mark)
    elif boton == 7:
        b7.config(text=mark)
    elif boton == 8:
        b8.config(text=mark)

ventana = tk.Tk()
ventana.title("Juego del Triqui")
ventana.geometry("260x300+500+100")
ventana.resizable(False, False)
b0 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(0))
b1 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(1))
b2 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(2))
b3 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(3))
b4 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(4))
b5 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(5))
b6 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(6))
b7 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(7))
b8 = tk.Button(ventana, width=6, height=3, bg="#e49fc9", fg="white", font=500, command=lambda:marcar(8))

b0.grid(row=0, column=0, padx=10, pady=10)
b1.grid(row=0, column=1, padx=10, pady=10)
b2.grid(row=0, column=2, padx=10, pady=10)
b3.grid(row=1, column=0, padx=10, pady=10)
b4.grid(row=1, column=1, padx=10, pady=10)
b5.grid(row=1, column=2, padx=10, pady=10)
b6.grid(row=2, column=0, padx=10, pady=10)
b7.grid(row=2, column=1, padx=10, pady=10)
b8.grid(row=2, column=2, padx=10, pady=10)

ventana.mainloop()