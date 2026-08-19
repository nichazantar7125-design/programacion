def suma(a, b):
    return a + b    

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b == 0:
        return "Error: División por cero no permitida."
    else:
        return a / b

def main():
    print(suma(9, 10))
    print(resta(4, 1))
    print(multiplicacion(5, 4))
    print(division(5, 0))

# 4 + 8 * 5
print(suma(4, multiplicacion(8, 5)))

# 4 * 8 / 2 + 4
print(suma(division(multiplicacion(4, 8), 2), 4))

# (8 + 7) / 3 * (6 - 2)
print(multiplicacion(division(suma(8, 7), 3), resta(6, 2)))

if __name__ == "__main__":
    main()