import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser, messagebox
import os
import json

ARCHIVO_GUARDADO = "apps.json"

# Cargar apps desde archivo si existe
def cargar_apps():
    if os.path.exists(ARCHIVO_GUARDADO):
        with open(ARCHIVO_GUARDADO, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Inicial por defecto
        return {
            "Bloc de Notas": ["notepad.exe", "#f0f0f0"],
            "Calculadora": ["calc.exe", "#f0f0f0"]
        }

# Guardar apps en archivo JSON
def guardar_apps():
    with open(ARCHIVO_GUARDADO, "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=4)

# Diccionario con apps: nombre -> [ruta, color]
apps = cargar_apps()

# Ventana principal
ventana = tk.Tk()
ventana.title("Lanzador de Aplicaciones")
ventana.geometry("450x600")
ventana.resizable(False, False)

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

def lanzar_app(ruta):
    try:
        os.startfile(ruta)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la aplicación:\n{e}")

def cambiar_color(nombre):
    nuevo_color = colorchooser.askcolor(title="Elige un color")[1]
    if nuevo_color:
        apps[nombre][1] = nuevo_color
        guardar_apps()
        actualizar_botones()

def eliminar_app(nombre):
    confirmacion = messagebox.askyesno("Eliminar aplicación", f"¿Eliminar '{nombre}' del lanzador?")
    if confirmacion:
        del apps[nombre]
        guardar_apps()
        actualizar_botones()

def actualizar_botones():
    for widget in frame_botones.winfo_children():
        widget.destroy()

    for nombre, (ruta, color) in apps.items():
        fila = tk.Frame(frame_botones)
        fila.pack(pady=3, fill="x", padx=5)

        boton_lanzar = tk.Button(fila, text=nombre, command=lambda r=ruta: lanzar_app(r),
                                 bg=color, width=30, anchor="w")
        boton_lanzar.pack(side="left", padx=2)

        boton_color = tk.Button(fila, text="🎨", width=3, command=lambda n=nombre: cambiar_color(n))
        boton_color.pack(side="left", padx=2)

        boton_eliminar = tk.Button(fila, text="❌", width=3, command=lambda n=nombre: eliminar_app(n))
        boton_eliminar.pack(side="left", padx=2)

def agregar_app():
    ruta = filedialog.askopenfilename(title="Selecciona la aplicación", filetypes=[("Ejecutables", "*.exe")])
    if ruta:
        nombre = simpledialog.askstring("Nombre", "Nombre para mostrar:")
        if nombre:
            color = colorchooser.askcolor(title="Elige color del botón")[1] or "#f0f0f0"
            apps[nombre] = [ruta, color]
            guardar_apps()
            actualizar_botones()

# Etiqueta
tk.Label(ventana, text="Lanzador de Aplicaciones", font=("Arial", 14, "bold")).pack(pady=5)

# Botón de agregar
btn_agregar = tk.Button(ventana, text="➕ Añadir nueva aplicación", command=agregar_app)
btn_agregar.pack(pady=10)

# Cargar interfaz
actualizar_botones()

# Ejecutar
ventana.mainloop()

