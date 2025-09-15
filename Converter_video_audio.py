import ffmpeg
import os

def convertir_video(archivo_entrada, carpeta_salida, nuevo_nombre, formato_salida):
    # Asegurar que el archivo de entrada existe
    if not os.path.isfile(archivo_entrada):
        print("❌ El archivo de entrada no existe.")
        return

    # Crear la ruta del archivo convertido
    archivo_salida = os.path.join(carpeta_salida, f"{nuevo_nombre}.{formato_salida}")

    try:
        ffmpeg.input(archivo_entrada).output(archivo_salida).run()
        print(f"✅ Conversión finalizada. Guardado en: {archivo_salida}")
    except ffmpeg.Error as e:
        print("❌ Error en la conversión:", e)

def convertir_video_con_resolucion(entrada, salida, ancho, alto):
    try:
        (
            ffmpeg
            .input(entrada)
            .output(salida, vf=f'scale={ancho}:{alto}')
            .run()
        )
        print(f"✅ Video convertido a resolución {ancho}x{alto}")
    except ffmpeg.Error as e:
        print("❌ Error en la conversión:", e)

def convertir_audio_con_config(entrada, salida, sample_rate, bitrate, canales, volumen):
    try:
        # Si volumen es distinto de 1.0, aplicamos filtro volume
        stream = ffmpeg.input(entrada)
        if volumen != 1.0:
            stream = stream.filter('volume', volumen)
        (
            stream
            .output(salida, ar=sample_rate, ac=canales, audio_bitrate=bitrate)
            .run()
        )
        print(f"✅ Audio convertido: {salida} (volumen ajustado a {volumen})")
    except ffmpeg.Error as e:
        print("❌ Error en la conversión:", e)

def menu():
    choice="0"
    while choice!="4":
        print("\nMenú de opciones: ")
        print("1. Convertir formato")
        print("2. Cambiar resolución (video)")
        print("3. Cambiar calidad (audio)")
        print("4. Salir")
        choice=input("Elegir opción: ")
        if choice=="1":
            ruta_origen = input("Ruta completa del archivo de entrada: ").strip('"')
            carpeta_destino = input("Carpeta de destino para el archivo convertido: ").strip('"')
            nombre_nuevo = input("📝 Nombre del nuevo archivo (sin extensión): ")
            formato = input("🎵 Formato de salida (ej. mp3, wav, mp4): ")
            convertir_video(ruta_origen, carpeta_destino, nombre_nuevo, formato)
        elif choice=="2":
            archivo_origen=input("Ruta completa del archivo de entrada: ").strip('"')
            archivo_destino = input("Ruta de destino para el archivo convertido (introducir nueva ruta y nuevo nombre): ").strip('"')
            ancho=int(input("Nuevo ancho del vídeo: "))
            alto=int(input("Nuevo alto del vídeo: "))
            convertir_video_con_resolucion( archivo_origen,archivo_destino,ancho,alto)
        elif choice=="3":
            archivo_origen = input("Ruta completa del archivo de entrada: ").strip('"')
            archivo_destino = input("Ruta de destino para el archivo convertido (introducir ruta y nuevo nombre): ").strip('"')
            rate=int(input("Sample_rate (calidad del sonido-> ej. 44100Hz=calidad CD): "))
            bit=input("Nuevo Bitrate (Cantidad de datos por segundo-> ej: 128k, 320k): ")
            canales=int(input("Nuevo Número de canales (Mono (1) o estéreo (2)): "))
            volume=float(input("Cambiar Volumen (ej: 1.5=150%): "))
            convertir_audio_con_config(archivo_origen,archivo_destino,rate,bit,canales,volume)
        elif choice == "4":
            print("Saliendo del programa...")
        else:
            print("Opción no válida. Intenta de nuevo.")

menu()