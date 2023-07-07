import pandas as pd
import datetime as dt

def CargarFalabella(NombreArchivo):
    """
    Carga y combina los datos de ventas de Falabella desde un archivo con dos hojas.

    Parámetros:
    - NombreArchivo (str): Nombre del archivo que contiene las hojas de datos de ventas de Falabella.

    Retorna:
    - df_falabella (pandas.DataFrame): DataFrame que contiene los datos combinados de ventas de Falabella.

    Esta función carga las hojas del archivo especificado en dos DataFrames separados: uno para los montos y otro para las unidades.
    Luego, transforma los DataFrames a un formato estrecho, donde las sucursales se convierten en atributos utilizando la función `pd.melt()`.
    A continuación, se eliminan las filas que no tienen valores en las columnas 'VALOR TOTAL' y 'UNIDADES'.
    Después, se realiza una unión (JOIN) entre los dos DataFrames utilizando la función `pd.merge()`.
    La columna 'FECHA' se convierte del formato serial de Excel a un objeto datetime utilizando una conversión basada en el número de días.
    Luego, las columnas se reorganizan para seguir la misma estructura que los otros archivos.
    Por último, el DataFrame resultante se devuelve como resultado.

    Ejemplo:
    >>> carpeta_ventas = os.path.join(os.getcwd(), 'Ventas')
    >>> archivo_falabella = '\\VENTAS FALABELLA.xlsx'
    >>> df_falabella = CargarFalabella(carpeta_ventas + archivo_falabella)
    >>> print(df_falabella)
          PUNTO DE VENTA            EAN  ... VALOR TOTAL      FECHA
    0              ACQUA  8806098683802  ...   1165700.0 2021-01-04
    1              ACQUA  8806098695058  ...   2465600.4 2021-01-04
    2              ACQUA  8806084321121  ...     -4300.0 2021-01-05
    3              ACQUA  8806091002860  ...   -134300.0 2021-01-05
    4              ACQUA  8806098077700  ...   2465700.0 2021-01-05
    ...              ...            ...  ...         ...        ...
    18322       WTC CALI  8806098656950  ...   1165700.0 2021-07-31
    18323       WTC CALI  8806098674664  ...   3365700.0 2021-07-31
    18324       WTC CALI  8806098720187  ...    365700.0 2021-07-31
    18325       WTC CALI  8806091240118  ...   2165700.0 2021-08-01
    18326       WTC CALI  8806098456260  ...    415700.0 2021-08-01

    [18327 rows x 6 columns]
    """

    # Cargar cada hoja del archivo a un dataframe separado
    df_monto = pd.read_excel(NombreArchivo, sheet_name = 0)
    df_unidades = pd.read_excel(NombreArchivo, sheet_name = 1)

    # Pasar las tablas a formato angosto (sucursales como atributo)
    df_monto = pd.melt(df_monto,
                       id_vars = df_monto.columns[[0, 1, 2]],
                       var_name = 'PUNTO DE VENTA',
                       value_name = 'VALOR TOTAL')

    df_unidades = pd.melt(df_unidades,
                          id_vars = df_unidades.columns[[0, 1, 2]],
                          var_name = 'PUNTO DE VENTA',
                          value_name = 'UNIDADES')

    # Remover filas sin valores
    df_monto = df_monto[df_monto['VALOR TOTAL'] != 0]
    df_unidades = df_unidades[df_unidades['UNIDADES'] != 0]

    # Hacer un JOIN entre las dos tablas
    df_falabella = pd.merge(df_monto, df_unidades)

    # Convertir la fecha serial de Excel a tipo datetime
    df_falabella['FECHA'] = df_falabella['FECHA'].apply(
        lambda x: dt.datetime.fromordinal(
            dt.datetime(1900, 1, 1).toordinal() + x - 2
            )
        )
    
    # Reorganizar las columnas para que sigan la misma estructura de los otros archivos
    df_falabella = df_falabella.reindex(columns = ['PUNTO DE VENTA', 'EAN', 'MODELO', 
        'UNIDADES', 'VALOR TOTAL', 'FECHA'])

    # Retornar el resultado
    return df_falabella