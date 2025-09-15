from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

with open('mi_archivo.txt', 'rb') as f:
    data = f.read()

encrypted = fernet.encrypt(data)

with open('mi_archivo.enc', 'wb') as f:
    f.write(encrypted)

print("Clave secreta:", key.decode())
