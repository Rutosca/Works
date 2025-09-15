from cryptography.fernet import Fernet

key = b'TU_CLAVE_SECRETA_EN_BYTES'
fernet = Fernet(key)

with open('mi_archivo.enc', 'rb') as f:
    encrypted = f.read()

decrypted = fernet.decrypt(encrypted)

with open('mi_archivo_descifrado.txt', 'wb') as f:
    f.write(decrypted)

