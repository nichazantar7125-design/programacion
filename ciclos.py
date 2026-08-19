# Acumulador
suma = 0

# Ciclo for para sumar 5 números ingresados por el usuario
for i in range(5):
    num = int(input(f"Ingresa el número {i+1}: "))
    suma = suma + num

print(f"El resultado de la suma es: {suma}")