class CuentaBancaria:
    def __init__(self, nombre, saldo, estado):
        self.nombre = nombre
        self.saldo = saldo
        self.estado = estado

    def mostrar(self):
        if self.estado:
            estado = "Activa"
        else:
            estado = "Inactiva"

        print("**** INFORMACIÓN DE LA CUENTA ****")
        print(f"Nombre  : {self.nombre}")
        print(f"Saldo   : {self.saldo}")
        print(f"Estado  : {estado}")
       

    def depositar(self, valor):
        if not self.estado:
            print("No se puede realizar el depósito. La cuenta está inactiva.")
        elif valor <= 0:
            print("El valor del depósito debe ser mayor que cero.")
        elif valor > 10000000:
            print("El depósito no puede ser superior a $10.000.000.")
        else:
            self.saldo += valor
            print(f"Depósito realizado correctamente: {valor}")
            print(f"Nuevo saldo: ${self.saldo}")

    def retirar(self, valor):
        if not self.estado:
            print("No se puede realizar el retiro. La cuenta está inactiva.")
        elif valor <= 0:
            print("El valor del retiro debe ser mayor que cero.")
        elif valor > self.saldo:
            print("No se puede realizar el retiro. Saldo insuficiente.")
        else:
            self.saldo -= valor
            print(f"Retiro realizado correctamente: {valor}")
            print(f"Nuevo saldo: {self.saldo}")

    def cambiarNombre(self, nombre):
        if nombre.strip() == "":
            print("No se puede cambiar el nombre. El nombre no puede estar vacío.")
        else:
            self.nombre = nombre
            print(f"Nombre cambiado correctamente a: {self.nombre}")

    def activar(self):
        self.estado = True
        print("La cuenta ha sido activada correctamente.")

    def desactivar(self):
        self.estado = False
        print("La cuenta ha sido desactivada correctamente.")

# PRUEBAS

print("CUENTA 1")

cuenta1 = CuentaBancaria("Laura Gómez", 500000, True)
cuenta1.mostrar()

print("1. Depósito válido:")
cuenta1.depositar(200000)

print("2. Depósito superior a $10.000.000:")
cuenta1.depositar(15000000)

print("3. Retiro válido:")
cuenta1.retirar(100000)

print("4. Retiro superior al saldo:")
cuenta1.retirar(10000000)

print("5. Desactivar cuenta:")
cuenta1.desactivar()

print("6. Depósito con cuenta inactiva:")
cuenta1.depositar(50000)

print("7. Retiro con cuenta inactiva:")
cuenta1.retirar(50000)

print("8. Activar nuevamente la cuenta:")
cuenta1.activar()

print("9. Cambiar nombre correctamente:")
cuenta1.cambiarNombre("Laura Sofía Gómez")

print("10. Intentar cambiar el nombre por un texto vacío:")
cuenta1.cambiarNombre("   ")

print("11. Información final de la cuenta:")
cuenta1.mostrar()

print("CUENTA 2")

cuenta2 = CuentaBancaria("Carlos Perez", 1000000, True)
cuenta2.mostrar()

print("Depósito en cuenta 2:")
cuenta2.depositar(500000)

print("Retiro en cuenta 2:")
cuenta2.retirar(250000)

print("Desactivando cuenta 2:")
cuenta2.desactivar()

print("Intentando retirar con cuenta 2 inactiva:")
cuenta2.retirar(100000)

print("Información final de cuenta 2:")
cuenta2.mostrar()

# Integrantes:
# Nicole Isabela Chazatar Inagan
# Ashlynn Nicole Santader Achicanoy
