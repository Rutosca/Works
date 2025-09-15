import pandas as pd
from rapidfuzz import fuzz


def cargar_excel(nombre_archivo, columna):
    df = pd.read_excel(nombre_archivo)
    return df[columna].dropna().astype(str).tolist()


def comparar_listas(lista_pequena, lista_grande, umbral=80):
    faltantes = []

    for item_peq in lista_pequena:
        # Buscamos la mejor coincidencia en la lista grande
        mejor_similitud = 0
        for item_gra in lista_grande:
            similitud = fuzz.token_set_ratio(item_peq, item_gra)
            if similitud > mejor_similitud:
                mejor_similitud = similitud

        # Si la mejor coincidencia es menor que el umbral, lo consideramos faltante
        if mejor_similitud < umbral:
            faltantes.append(item_peq)

    return faltantes


def guardar_diferencias(faltantes, nombre_archivo_salida):
    df = pd.DataFrame(faltantes, columns=["Canciones faltantes"])
    df.to_excel(nombre_archivo_salida, index=False)
    print(f"Guardado {len(faltantes)} canciones en '{nombre_archivo_salida}'")


def main():
    archivo_grande = "Canciones_1.xlsx"
    archivo_pequeno = "Canciones_2.xlsx"
    columna = "Canciones"  # Cambia aquí por el nombre real de la columna en tus archivos
    umbral_similitud = 80  # Puedes subir o bajar el porcentaje

    lista_grande = cargar_excel(archivo_grande, columna)
    lista_pequena = cargar_excel(archivo_pequeno, columna)

    faltantes = comparar_listas(lista_pequena, lista_grande, umbral_similitud)
    guardar_diferencias(faltantes, "diferencias.xlsx")


if __name__ == "__main__":
    main()

