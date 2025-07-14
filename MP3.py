import yt_dlp

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

# Ejemplo de uso
url = input("Introduce la URL del video de YouTube: ")
descargar_mp3_con_ytdlp(url, 'E:/Music/XD')
