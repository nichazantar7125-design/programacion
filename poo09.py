class Vehiculo:
    def __init__(self, placa, marca):
        self.placa = placa
        self.marca = marca

    def mostrar(self):
        print(f"Informacion Vehiculo: PLACA {self.placa} ({self.marca})")

class Automovil(Vehiculo):
    def dibujar(self):
        print("    ______")
        print("   /|_||_\\`.__")
        print("  (   _    _ _\\")
        print("  =`-(_)--(_)-'")

class Motocicleta(Vehiculo):
    def dibujar(self):
        print("    __o")
        print("  _ \\<_")
        print(" (_)/(_)")  

class Camion(Vehiculo):
    def dibujar(self):
        print(" ______________  ____")
        print("|              |/    \\")
        print("|    CARGA     |      |")
        print("|______________|______|")
        print("  (_)(_)       (_)  (_)")


a = Automovil("GDP499", "Honda CVR")
m = Motocicleta("CKB99B", "Honda ECO")
c = Camion("MPE271", "Kenworth")

a.mostrar()
a.dibujar()
print("=====================")
m.mostrar()
m.dibujar()
print("=====================")
c.mostrar()
c.dibujar()
