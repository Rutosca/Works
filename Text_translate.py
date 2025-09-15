from googletrans import Translator
import os

translator = Translator()

def traducir_texto_manual():
    texto = input("Introduce el texto que quieres traducir: ")
    idioma_destino = input("Código del idioma destino (ej: en, fr, de, it): ").lower()
    resultado = translator.translate(texto, dest=idioma_destino)
    print(f"\nTexto traducido:\n{resultado.text}\n")

def traducir_archivo_txt():
    ruta = input("Ruta del archivo .txt a traducir: ").strip('"')
    idioma_destino = input("Código del idioma destino (ej: en, fr, de, it): ").lower()

    if not os.path.isfile(ruta):
        print("❌ Archivo no encontrado.")
        return

    with open(ruta, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    resultado = []
    for linea in lineas:
        if linea.strip():  # No traduce líneas vacías
            traducida = translator.translate(linea.strip(), dest=idioma_destino).text
            resultado.append(traducida)
        else:
            resultado.append("")

    nombre_salida = os.path.splitext(ruta)[0] + f"_traducido_{idioma_destino}.txt"
    with open(nombre_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(resultado))

    print(f"✅ Archivo traducido guardado como: {nombre_salida}\n")

def traducir_subtitulos_srt():
    ruta = input("Ruta del archivo .srt a traducir: ").strip('"')
    idioma_destino = input("Código del idioma destino (ej: en, fr, de, it): ").lower()

    if not os.path.isfile(ruta):
        print("❌ Archivo no encontrado.")
        return

    with open(ruta, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    resultado = []
    for linea in lineas:
        if "-->" in linea or linea.strip().isdigit() or linea.strip() == "":
            resultado.append(linea.strip())
        else:
            traducida = translator.translate(linea.strip(), dest=idioma_destino).text
            resultado.append(traducida)

    nombre_salida = os.path.splitext(ruta)[0] + f"_traducido_{idioma_destino}.srt"
    with open(nombre_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(resultado))

    print(f"✅ Subtítulos traducidos guardados como: {nombre_salida}\n")


def menu():
    while True:
        print("\n--- Traductor automático ---")
        print("1. Traducir texto manual")
        print("2. Traducir archivo .txt")
        print("3. Traducir archivo .srt")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            traducir_texto_manual()
        elif opcion == "2":
            traducir_archivo_txt()
        elif opcion == "3":
            traducir_subtitulos_srt()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


menu()
