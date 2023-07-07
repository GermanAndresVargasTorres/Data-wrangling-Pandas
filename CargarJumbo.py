import os
import pandas as pd

def CargarJumbo(NombreCarpeta):
    """
    Carga y combina los datos de las archivos con las ventas mensuales de Jumbo.

    Parámetros:
    - NombreCarpeta (str): Nombre de la carpeta que contiene los archivos de ventas mensuales de Jumbo.

    Retorna:
    - df_jumbo (pandas.DataFrame): DataFrame que contiene los datos combinados de todas las ventas mensuales de Jumbo.

    Esta función toma el nombre de una carpeta y construye la ruta completa a esa carpeta dentro del directorio actual.
    Luego, itera sobre los archivos en la carpeta y carga cada archivo en un DataFrame de Pandas, agregándolos a una lista.
    Después, combina todos los DataFrames de la lista en uno solo usando la función `pd.concat()` y lo devuelve como resultado.

    Ejemplo:
    >>> carpeta_ventas = os.path.join(os.getcwd(), 'Ventas')
    >>> carpeta_jumbo = '\\jumbo'
    >>> df_jumbo = CargarJumbo(carpeta_ventas + carpeta_jumbo)
    >>> print(df_jumbo)
              PUNTO DE VENTA            EAN  ... VALOR TOTAL      FECHA
    0      Jumbo 20 De Julio  8806098384709  ...  2390691.30 2021-04-04
    1      Jumbo 20 De Julio  8806098384846  ...  3273044.25 2021-04-01
    2      Jumbo 20 De Julio  8806091006653  ...  5668002.24 2021-04-01
    3      Jumbo 20 De Julio  8806084321121  ...  1130187.09 2021-04-03
    4      Jumbo 20 De Julio  8806084321121  ...  1130187.09 2021-04-04
    ...                  ...            ...  ...         ...        ...
    50364      Jumbo Popayan  8806087047813  ...  9564450.00 2021-05-31
    50365  Metro Santa Lucia  8806087047790  ...  1069635.00 2021-05-31
    50366    Jumbo Unicentro  8806087047851  ...  1369635.00 2021-05-31
    50367   Jumbo E_commerce  8806087044287  ...  1615134.00 2021-05-31
    50368   Jumbo E_commerce  8806087043716  ...  1219698.00 2021-05-31

    [50369 rows x 6 columns]
    """

    # Ruta a la carpeta con las ventas mensuales de Jumbo
    carpeta_jumbo = os.path.join(os.getcwd(), NombreCarpeta)  # Create the full folder path

    # Crear un dataframe para cada archivo y agregarlo a la lista
    list_df_jumbo = []
    for archivo_mensual in os.listdir(carpeta_jumbo):
        ruta_archivo = os.path.join(carpeta_jumbo, archivo_mensual)
        df_mensual = pd.read_excel(ruta_archivo, parse_dates = ['FECHA'])
        list_df_jumbo.append(df_mensual)  

    # Concatenar los dataframe en la lista y retornar el resultado
    df_jumbo = pd.concat(list_df_jumbo, ignore_index = True)
    return df_jumbo