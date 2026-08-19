mensaje = "Variable externa"

def ejemplo():
    mensaje = "Variable local"
    return mensaje

print(ejemplo())
print(mensaje)