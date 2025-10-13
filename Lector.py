import re

# Ruta del archivo de guardado
input_file = r"C:\Users\rutos\AppData\Roaming\Citra\sdmc\Nintendo 3DS\00000000000000000000000000000000\00000000000000000000000000000000\title\00040000\00112f00\data\00000001\game.ie4"
output_file = r"C:\Users\rutos\Desktop\jugadores_filtrados.csv"

with open(input_file, "rb") as f:
    data = f.read()

# Extraer cadenas ASCII
utf8_strings = re.findall(rb"[ -~]{3,}", data)
utf8_strings = [s.decode("utf-8", errors="ignore") for s in utf8_strings]

# Extraer cadenas UTF-16LE
utf16_strings = re.findall(rb"(?:[\x20-\x7E]\x00){3,}", data)
utf16_strings = [s.decode("utf-16le", errors="ignore") for s in utf16_strings]

# Unir
all_strings = utf8_strings + utf16_strings

# Filtrar: solo palabras con letras, espacios y mayúscula inicial
posibles_nombres = []
for s in all_strings:
    if re.match(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*$", s):
        if 3 <= len(s) <= 25:
            posibles_nombres.append(s)

# Quitar duplicados
posibles_nombres = sorted(set(posibles_nombres))

# Guardar en CSV
with open(output_file, "w", encoding="utf-8") as f:
    for nombre in posibles_nombres:
        f.write(nombre + "\n")

print(f"Se han extraído {len(posibles_nombres)} posibles nombres de jugadores a {output_file}")
