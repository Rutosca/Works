import yt_dlp
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

NOMBRE_ERRORES = "errores.txt"
MAX_CONCURRENT_DOWNLOADS = 5  # Número de descargas simultáneas

# Guardará los fallidos actuales
errores_descarga = []

def obtener_videos_playlist(url):
    """Extrae URLs de todos los vídeos de una playlist o devuelve el vídeo si es suelto"""
    opciones = {"extract_flat": True, "dump_single_json": True}
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            if "entries" in info:
                return [entry["url"] for entry in info["entries"] if entry and "url" in entry]
            else:
                return [url]
    except Exception as e:
        print(f"⚠️ Error extrayendo playlist {url}: {e}")
        return [url]

def descargar_video_infinito(url, carpeta_destino, formato):
    """Descarga un vídeo indefinidamente hasta que tenga éxito"""
    opciones_base = {
        "outtmpl": f"{carpeta_destino}/%(title)s.%(ext)s",
        "retries": 10,
        "fragment_retries": 10,
        "skip_unavailable_fragments": False,
    }

    if formato == "mp3":
        opciones_base.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }],
            "cookiefile": "cookies.txt",
        })
    elif formato == "mp4":
        opciones_base.update({
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        })
    else:
        print("Formato no válido.")
        return False

    intento = 0
    while True:
        intento += 1
        try:
            print(f"[Intento {intento}] Descargando: {url}")
            with yt_dlp.YoutubeDL(opciones_base) as ydl:
                ydl.download([url])
            print(f"✅ Descargado correctamente: {url}")
            return True
        except Exception as e:
            print(f"❌ Error en intento {intento} para {url}: {e}")
            time.sleep(2)  # Espera antes de reintentar
            if url not in errores_descarga:
                errores_descarga.append(url)

def guardar_errores(carpeta_destino):
    if errores_descarga:
        archivo = os.path.join(carpeta_destino, NOMBRE_ERRORES)
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(errores_descarga))
        print(f"\n⚠️ Enlaces problemáticos guardados en {archivo}")

# --- Programa principal ---
while True:
    formato = input("¿Quieres descargar en mp3 o mp4? ").lower().strip()
    if formato in ["mp3", "mp4"]:
        break
    else:
        print("Formato no válido. Escribe 'mp3' o 'mp4'.")

lista = []
e = 1
while True:
    print(f"{e}º video o playlist:")
    url = input("Introduce la URL (enter para terminar de añadir): ")
    if url:
        lista.append(url)
        e += 1
    else:
        break

ruta = input("Elegir ruta para guardar: ").strip('"')

# Expandir playlists a URLs individuales
urls_finales = []
for enlace in lista:
    urls_finales.extend(obtener_videos_playlist(enlace))

# Descargar en paralelo
with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
    futuros = {executor.submit(descargar_video_infinito, url, ruta, formato): url for url in urls_finales}
    for futuro in as_completed(futuros):
        pass  # cada hilo gestiona sus reintentos, aquí solo esperamos a que terminen

guardar_errores(ruta)
print("✅ Proceso finalizado")


