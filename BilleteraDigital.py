class BilleteraDigital:
    def __init__(self, propietario, saldo, limite_diario):
        self.propietario = propietario
        self._saldo = saldo
        self._limite_diario = limite_diario
        self._gastado_hoy = 0
        self._compras_exitosas = 0

    @property
    def saldo(self):
        return self._saldo

    @property
    def limite_diario(self):
        return self._limite_diario

    @limite_diario.setter
    def limite_diario(self, nuevo_limite):
        if nuevo_limite >= 50000 and nuevo_limite <= 500000:
            self._limite_diario = nuevo_limite

    def recargar(self, monto):
        if monto > 0 and monto <= 1000000:
            self._saldo += monto
            return True
        else:
            return False

    def puede_comprar(self, valor):
        if valor <= 0:
            return False
        if valor >= 100000:
            valor = valor * 0.90
        if valor <= self._saldo:
            if self._gastado_hoy + valor <= self._limite_diario:
                return True
        return False

    def comprar(self, valor):
        if self.puede_comprar(valor):
            if valor >= 100000:
                valor = valor * 0.90
            self._saldo = self._saldo - valor
            self._gastado_hoy = self._gastado_hoy + valor
            self._compras_exitosas = self._compras_exitosas + 1
            if self._compras_exitosas % 3 == 0:
                self._saldo = self._saldo + 10000
            return True
        return False

    def estado(self):
        porcentaje = self._gastado_hoy / self._limite_diario * 100
        if porcentaje < 50:
            return "NORMAL"
        elif porcentaje < 80:
            return "PRECAUCIÓN"
        elif porcentaje < 100:
            return "CERCA DEL LÍMITE"
        else:
            return "LÍMITE ALCANZADO"

    def nuevo_dia(self):
        self._gastado_hoy = 0
        self._compras_exitosas = 0

# Prueba
billetera = BilleteraDigital("Laura", 300000, 250000)
billetera.comprar(50000)
billetera.comprar(120000)
billetera.comprar(40000)
print("Saldo disponible:", billetera.saldo)
print("Dinero gastado:", billetera._gastado_hoy)
print("Compras exitosas:", billetera._compras_exitosas)
print("Estado:", billetera.estado())
print("Compra de 300000:", billetera.comprar(300000))

