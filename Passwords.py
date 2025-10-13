import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

# Archivo donde guardaremos la sal para derivar la clave
ARCHIVO_SALT = "salt.bin"
# Archivo donde guardaremos las contraseñas cifradas
ARCHIVO_DATOS = "passwords.enc"

def generar_o_cargar_salt():
    if os.path.exists(ARCHIVO_SALT):
        with open(ARCHIVO_SALT, "rb") as f:
            salt = f.read()
    else:
        salt = os.urandom(16)  # 16 bytes de sal aleatoria
        with open(ARCHIVO_SALT, "wb") as f:
            f.write(salt)
    return salt

def derivar_clave(contraseña: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    clave = base64.urlsafe_b64encode(kdf.derive(contraseña.encode()))
    return clave

def cifrar_datos(clave: bytes, datos: bytes) -> bytes:
    f = Fernet(clave)
    return f.encrypt(datos)

def descifrar_datos(clave: bytes, datos_cifrados: bytes) -> bytes:
    f = Fernet(clave)
    return f.decrypt(datos_cifrados)

def guardar_passwords(clave: bytes, diccionario_passwords: dict):
    datos = str(diccionario_passwords).encode()  # Convertir dict a bytes (simple)
    datos_cifrados = cifrar_datos(clave, datos)
    with open(ARCHIVO_DATOS, "wb") as f:
        f.write(datos_cifrados)

def cargar_passwords(clave: bytes) -> dict:
    if not os.path.exists(ARCHIVO_DATOS):
        return {}
    with open(ARCHIVO_DATOS, "rb") as f:
        datos_cifrados = f.read()
    datos = descifrar_datos(clave, datos_cifrados)
    diccionario = eval(datos.decode())  # Convertir bytes a dict (ojo con eval, usar json es mejor)
    return diccionario

def main():
    print("Gestor de contraseñas seguro")
    salt = generar_o_cargar_salt()
    contraseña_maestra = input("Introduce la contraseña maestra: ")
    clave = derivar_clave(contraseña_maestra, salt)

    passwords = cargar_passwords(clave)

    while True:
        print("\nOpciones:")
        print("1. Añadir contraseña")
        print("2. Ver contraseña")
        print("3. Salir")
        opcion = input("Elige opción: ")

        if opcion == "1":
            servicio = input("Servicio/Nombre: ")
            pwd = input("Contraseña: ")
            passwords[servicio] = pwd
            guardar_passwords(clave, passwords)
            print(f"Contraseña para '{servicio}' guardada.")
        elif opcion == "2":
            servicio = input("Servicio/Nombre: ")
            if servicio in passwords:
                print(f"Contraseña para '{servicio}': {passwords[servicio]}")
            else:
                print("Servicio no encontrado.")
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()

