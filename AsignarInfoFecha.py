import pandas as pd
import datetime as dt
import locale

def AsignarInfoFecha(df_entrada):
	"""
    Asigna información adicional de fecha a un DataFrame basado en su columna 'FECHA'.

    Parámetros:
    - df_entrada (pandas.DataFrame): DataFrame de entrada con una columna 'FECHA'.

    Retorna:
    - df_entrada (pandas.DataFrame): DataFrame modificado con las columnas 'NUMERO SEMANA' y 'MES' agregadas.

    Esta función calcula el número de semana correspondiente para cada fecha en la columna 'FECHA' del DataFrame de entrada.
    Luego configura el locale a español y asigna el nombre en mayúsculas del mes correspondiente a la columna 'MES'.

    Ejemplo:
    >>> df = pd.DataFrame({'FECHA': ['2023-01-15', '2023-02-20', '2023-03-25']})
    >>> AsignarInfoFecha(df)
           FECHA 	  NUMERO SEMANA        MES
    0 2023-01-15            	W02      ENERO
    1 2023-02-20            	W08    FEBRERO
    2 2023-03-25            	W12      MARZO
    """

	# Calcular número de semana correspondiente
	df_entrada['NUMERO SEMANA'] = df_entrada['FECHA'].apply(
        lambda x: 'W' + x.strftime("%V"))

	# Configurar locale a Español
	locale.setlocale(locale.LC_TIME, 'es_ES')

	# Asignar el nombre de mes correspondiente en mayúsculas
	df_entrada['MES'] = df_entrada['FECHA'].dt.strftime('%B').str.upper()

	return df_entrada