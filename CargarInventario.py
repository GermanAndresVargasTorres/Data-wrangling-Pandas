import os
import pandas as pd
import pyodbc


def CargarInventario(NombreArchivo):
	"""
    Carga los datos de inventario desde un archivo de Microsoft Access y los almacena en un DataFrame.

    Parámetros:
    - NombreArchivo (str): Nombre del archivo de inventario de Microsoft Access.

    Retorna:
    - df_inventario (pandas.DataFrame): DataFrame que contiene los datos de inventario.

    Esta función construye la ruta completa al archivo de inventario utilizando el directorio actual y el nombre del archivo especificado.
    Luego, crea la cadena de conexión para acceder al archivo de Access utilizando el controlador de Microsoft Access.
    A continuación, establece una conexión con el archivo de Access utilizando la cadena de conexión.
    Se extrae toda la información de la tabla 'INVENTARIO_2' en el archivo de Access y se almacena en un DataFrame de Pandas.
    Finalmente, se cierra la conexión y se devuelve el DataFrame de inventario como resultado.

    Ejemplo:
    >>> archivo_inventario = '\\BASE_INVENTARIO.accdb'
    >>> df_inventario = CargarInventario(archivo_inventario)
    >>> print(df_inventario)
	           TIPO  CANAL     CADENA  ...       CIUDAD CORE STORE PROMOTER
	0       OFFLINE  HYPER  FALABELLA  ...     MEDELLIN         SI       SI
	1       OFFLINE  HYPER  FALABELLA  ...       BOGOTA         NO       SI
	2       OFFLINE  HYPER  FALABELLA  ...         CALI         SI       SI
	3       OFFLINE  HYPER  FALABELLA  ...     MEDELLIN         SI       SI
	4          CEDI  HYPER  FALABELLA  ...       BOGOTA         NO       NO
	...         ...    ...        ...  ...          ...        ...      ...
	649623  OFFLINE  HYPER      EXITO  ...   VALLEDUPAR         NO       NO
	649624  OFFLINE  HYPER      EXITO  ...  SABANALARGA         NO       NO
	649625  OFFLINE  HYPER      EXITO  ...  SABANALARGA         NO       NO
	649626  OFFLINE  HYPER      EXITO  ...  SABANALARGA         NO       NO
	649627  OFFLINE  HYPER      EXITO  ...    CARTAGENA         NO       NO

	[649628 rows x 17 columns]
    """
	
	# Ruta al archivo de inventario
	archivo_inventario = os.getcwd() + NombreArchivo

	# Crear la cadena de conexión
	cadena_conexion_access = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={archivo_inventario}'

	# Conectar al archivo
	conn = pyodbc.connect(cadena_conexion_access)

	# Extraer toda la información de la tabla y almacenar en un dataframe
	sql_query = 'SELECT * FROM INVENTARIO_2'
	df_inventario = pd.read_sql(sql_query, conn)

	# Cerrar la conexión y retornar el dataframe
	conn.close()
	return df_inventario
