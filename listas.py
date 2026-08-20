def main():
    print("Manejo de listas")
    frutas = ['Fresa', 'Banano', 'Pera', 'Uvas']
    frutas.append('Durazno') # Adiciona al final
    frutas.insert(1,'Piña') # Inserta un dato
    frutas[0] = 'Fresa Cherry' # Modifica un dato
    frutas.remove('Banano') # Elimina un dato
    frutaEliminada = frutas.pop(2) # Elimina un dato por indice
    print("Fruta eliminada: ", frutaEliminada)
    # print (frutas, len(frutas))
   
    # Recorrer la lista
    for fruta in frutas:
        print(fruta)

main()