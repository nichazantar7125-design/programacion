class Objeto:
    def __init__(self, precio, cantidad):
        self.__precio = precio
        self.__cantidad = cantidad

    # Getters
    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def precio(self):
        return self.__precio

    # Setters
    @cantidad.setter
    def cantidad(self, nuevaCantidad):
        if(nuevaCantidad >= 0):
            self.__cantidad = nuevaCantidad
        else:
            raise ValueError("La cantidad debe ser mayor o igual a 0")

    @precio.setter
    def precio(self, nuevoPrecio):
        if(nuevoPrecio >= 0):
            self.__precio = nuevoPrecio
        else:
            raise ValueError("El precio debe ser mayor o igual a 0")

    # Helpers
    @property
    def total(self):
        return self.__cantidad * self.__precio
        
    def mostrar(self):
        print(f"Cantidad: {self.__cantidad} | Precio: ${self.__precio} | TOTAL: ${self.total}")
        
o1 = Objeto (5000, 3)
try:
    o1.cantidad = -3
    o1.cantidad = 5
    o1.precio = -2000
    o1.mostrar()
except Exception as e:
    print(e)
