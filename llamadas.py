import os
import subprocess

llamadas = []

def limpiarPantalla():
    if os.name == "nt":
            subprocess.run(["cls"], shell=True)

def definirOperador(numero):
    if 1000 <= numero <= 2999:
        return  "CLARO"
    elif 3000 <= numero <= 6999:
        return "MOVISTAR"
    elif 7000 <= numero <= 9999:
        return "TIGO"

def ingresarLlamada():
    #limpiarPantalla()
    print("Ingresar Llamada")
    numero = int(input("Numero: "))
    minutos = int(input("Minutos: "))
    llamada = {
         "numero": numero,
         "minutos": minutos
    }
    llamadas.append(llamada)

def mostrar():
     limpiarPantalla()
     for llamada in llamadas:
          print("Numero  :", llamada["numero"])
          print("Minutos :", llamada["minutos"])
          print("Operador:", definirOperador(llamada["numero"]))
          print("******************************")
        
     input("Pulse ENTER para salir")

def main():
    flag = True
    while flag:
        limpiarPantalla()
        print("Gestion de llamadas")
        print("*** MENU PRINCIPAL ***")
        print("1. Ingresar datos")
        print("2. Mostrar llamadas")
        print("6. Salir")
        print()
        opt = int(input("Ingrese su opcion: "))
        if opt == 1:
            ingresarLlamada()
        elif opt == 2:
             mostrar()
        elif opt == 6:
            flag = False

main()