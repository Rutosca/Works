import yt_dlp
import time

def descargar_mp3_con_ytdlp(url, carpeta_destino):
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{carpeta_destino}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])


lista=[]
e=1
while True:
    print(f"{e}º video:")
    url = input("Introduce la URL del video de YouTube (enter para terminar de añadir): ")
    if url:#no está vacio
        lista.append(url)
        e+=1
    else:
        break
for i,enlace in enumerate(lista, start=1):
    descargar_mp3_con_ytdlp(enlace, 'E:/Music/XD')
    print(f"\nVideo {i}/{len(lista)} descargado. Siguiente...")
    time.sleep(3)
print("Proceso finalizado")