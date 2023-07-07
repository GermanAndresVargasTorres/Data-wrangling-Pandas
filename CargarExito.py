import pandas as pd

def CargarExito(NombreArchivo):
    """
    Carga y combina los datos de ventas de Éxito desde un archivo con múltiples hojas.

    Parámetros:
    - NombreArchivo (str): Nombre del archivo que contiene las hojas de datos de ventas de Éxito.

    Retorna:
    - df_exito (pandas.DataFrame): DataFrame que contiene los datos combinados de ventas de Éxito.

    Esta función carga las hojas del archivo especificado en un diccionario de DataFrames, donde cada elemento del diccionario corresponde a una hoja.
    Luego, convierte el diccionario a una lista de DataFrames.
    A continuación, combina todos los DataFrames de la lista en uno solo usando la función `pd.concat()`.
    El resultado es un DataFrame que contiene los datos combinados de ventas de Éxito y se devuelve como resultado.

    Ejemplo:
    >>> carpeta_ventas = os.path.join(os.getcwd(), 'Ventas')
    >>> archivo_exito = '\\EXITO.xlsx'
    >>> df_exito = CargarExito(carpeta_ventas + archivo_exito)
    >>> print(df_exito)
                        PUNTO DE VENTA            EAN  ...   VALOR TOTAL      FECHA
    0            EXITO BARRANCABERMEJA  8806098363391  ...  1.702879e+06 2021-01-08
    1            EXITO BARRANCABERMEJA  8806087537789  ...  2.123897e+06 2021-01-08
    2                EXITO BUCARAMANGA  8806098363391  ...  1.580313e+06 2021-01-06
    3      EXITO BUENA VISTA (CV) BLLA  8806087537758  ...  3.231819e+06 2021-01-07
    4      EXITO BUENA VISTA (CV) BLLA  8806087537802  ...  2.924055e+06 2021-01-07
    ...                            ...            ...  ...           ...        ...
    24377               EXITO LAURELES  8806091241399  ...  9.062529e+06 2021-07-30
    24378         TIENDA VIRTUAL EXITO  8806091241399  ...  8.154921e+06 2021-07-27
    24379             EXITO CHIPICHAPE  8806091241399  ...  8.154921e+06 2021-07-30
    24380               EXITO SANDIEGO  8806098688791  ...  4.943940e+04 2021-07-26
    24381    EXITO NUEVO KENNEDY (CAF)  8806098688791  ...  4.943940e+04 2021-07-29

    [53184 rows x 6 columns]
    """

    # Crear un diccionario, donde cada elemento es un dataframe correspondiendo a una hoja del archivo de Excel
    dict_df_exito = pd.read_excel(NombreArchivo, sheet_name = None, parse_dates = ['FECHA'])

    # Convertir el diccionario a lista
    list_df_exito = list(dict_df_exito.values())

    # Concatenar los dataframe en la lista y retornar el resultado
    df_exito = pd.concat(list_df_exito)
    return df_exito