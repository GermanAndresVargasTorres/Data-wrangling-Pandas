"""
Carga y procesa los datos de ventas e inventario para analizar la distribución de ventas.

Este script principal es responsable de cargar y combinar los datos de ventas de diferentes cadenas 
(Alkosto, Falabella, Jumbo, Éxito) almacenados en Excel, así como el inventario desde una base de datos de Access. 
Luego, realiza una serie de transformaciones y cálculos para crear un formato específico de ventas que se exporta
a una base de datos en SQL y finalmente realiza un análisis de distribución de ventas por cadena, línea de producto 
y punto de venta.

Ejemplo:
>>> Abrir y ejecutar el archivo desde Python IDLE o ingresar en el shell:
>>> exec(open('Cargar_ventas_a_SQL.py').read())
>>> print(df_ventas)
           TIPO TIPO2  CANAL   CADENA  ...      FECHA    MES CORE STORE PROMOTER
0       OFFLINE    SO  HYPER  ALKOSTO  ... 2021-01-10  ENERO         NO       NO
1       OFFLINE    SO  HYPER  ALKOSTO  ... 2021-01-10  ENERO         NO       NO
2       OFFLINE    SO  HYPER  ALKOSTO  ... 2021-01-10  ENERO         NO       NO
3       OFFLINE    SO  HYPER  ALKOSTO  ... 2021-01-10  ENERO         NO       NO
4       OFFLINE    SO  HYPER  ALKOSTO  ... 2021-01-10  ENERO         NO       NO
...         ...   ...    ...      ...  ...        ...    ...        ...      ...
183785  OFFLINE    SO  HYPER    EXITO  ... 2021-07-30  JULIO         SI       SI
183786      NaN    SO    NaN      NaN  ... 2021-07-27  JULIO        NaN      NaN
183787  OFFLINE    SO  HYPER    EXITO  ... 2021-07-30  JULIO         NO       NO
183788  OFFLINE    SO  HYPER    EXITO  ... 2021-07-26  JULIO         NO       SI
183789  OFFLINE    SO  HYPER    EXITO  ... 2021-07-29  JULIO         NO       NO

[183790 rows x 23 columns]
>>> print(porcentajes_por_sede)
CADENA   LINEA       PUNTO DE VENTA     
ALKOSTO  Acc         AKIPI                  1.000000
         Accesorios  AK170                  0.027564
                     AKB30                  0.039462
                     AKB68                  0.068738
                     AKBAR                  0.019603
                                              ...   
JUMBO    Ultrawide   Jumbo Calle 170        0.292135
                     Jumbo De La 65         0.033708
                     Jumbo E_commerce       0.438202
                     Jumbo Santa Ana        0.168539
                     Jumbo Valle De Lili    0.067416
Name: UNIDADES, Length: 6501, dtype: float64	
"""

import os
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine

from CargarFalabella import *
from CargarJumbo import *
from CargarExito import *
from CargarInventario import *
from AsignarInfoFecha import *


# Rutas a las carpetas
carpeta_ventas = os.path.join(os.getcwd(), 'Ventas')
carpeta_target = os.path.join(os.getcwd(), 'TG')

# Variables para la conexion a la base de datos
servidor_sql = 'GERMAN'
db_sql = 'PruebaDB'
tabla_sql_ventas = 'Ventas'

# Variables para los archivos
archivo_alkosto = '\\VENTAS ALKOSTO.xlsx'
archivo_falabella = '\\VENTAS FALABELLA.xlsx'
carpeta_jumbo = '\\jumbo'
archivo_exito = '\\EXITO.xlsx'
archivo_inventario = '\\BASE_INVENTARIO.accdb'
archivo_target = '\\BASE TARGET.xlsx'


# PASO 1 - CREACION DEL FORMATO DE VENTAS


# Cargar las ventas de cada cadena a su propio dataframe
df_alkosto = pd.read_excel(carpeta_ventas + archivo_alkosto, parse_dates = ['FECHA'])
df_falabella = CargarFalabella(carpeta_ventas + archivo_falabella)
df_jumbo = CargarJumbo(carpeta_ventas + carpeta_jumbo)
df_exito = CargarExito(carpeta_ventas + archivo_exito)

# Unir todas las ventas en un único dataframe
df_ventas_simple = pd.concat([df_alkosto, df_falabella, df_jumbo, df_exito], 
	ignore_index = True)

# Cargar el inventario a un dataframe
df_inventario = CargarInventario(archivo_inventario)

# Descartar las columnas de inventario que deberán ser recalculadas/reasignadas
df_inventario.drop(['TIPO2', 'UNIDADES', 'VALOR TOTAL', 'NUMERO SEMANA', 'FECHA', 'MES'], 
	axis = 1, inplace = True)

# Construir tabla con información de producto
df_productos = df_inventario.drop_duplicates(subset = ['EAN'], keep = 'first')
df_productos = df_productos[['EAN', 'REFERENCIA HOMOLOGADA', 'CATEGORIA', 'SUBCATEGORIA', 
	'LINEA', 'SUBLINEA']]

# Construir tabla con información de sedes
df_sedes = df_inventario.drop_duplicates(subset = ['PUNTO DE VENTA'], keep = 'first')
df_sedes = df_sedes[['PUNTO DE VENTA', 'HOMOLOGA ALMACEN', 'TIPO', 'CANAL', 'CADENA', 'SUBCADENA',
        'REGIONAL', 'CIUDAD', 'CORE STORE', 'PROMOTER']]

# Hacer dos LEFT JOIN para asociar la información de producto y sede a las ventas
df_ventas = pd.merge(df_ventas_simple, df_productos, how = 'left', on = ['EAN'])
df_ventas = pd.merge(df_ventas, df_sedes, how = 'left', on = ['PUNTO DE VENTA'])

# Agregar información para columnas TIPO2, NUMERO SEMANA y MES
df_ventas['TIPO2'] = 'SO'   # Código para ventas
df_ventas = AsignarInfoFecha(df_ventas)

# Reorganizar las columnas según el formato de ventas
df_ventas = df_ventas.reindex(columns = ['TIPO', 'TIPO2', 'CANAL', 'CADENA', 'SUBCADENA',
 	'PUNTO DE VENTA', 'HOMOLOGA ALMACEN', 'EAN', 'MODELO', 'REFERENCIA HOMOLOGADA', 
 	'CATEGORIA', 'SUBCATEGORIA', 'LINEA', 'SUBLINEA', 'UNIDADES', 'VALOR TOTAL', 
 	'REGIONAL', 'CIUDAD', 'NUMERO SEMANA', 'FECHA', 'MES', 'CORE STORE', 'PROMOTER'])

# Crear la cadena de conexión con Windows Authentication
cadena_conexion_sql = f'mssql+pyodbc://{servidor_sql}/{db_sql}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

# Crear el motor de conexión SQLAlchemy
motor_sql = create_engine(cadena_conexion_sql)

# Exportar el dataframe a la tabla de ventas en SQL
df_ventas.to_sql(tabla_sql_ventas, motor_sql, if_exists = 'replace', index = False)


# PASO 2 - CALCULO DE DISTRIBUCION DE VENTAS POR CADENA, LINEA DE PRODUCTO Y PUNTO DE VENTA


# Calcular los totales de unidades vendidas por cadena y linea
totales_por_linea = df_ventas.groupby(['CADENA', 'LINEA'])['UNIDADES'].sum()

# Calcular los totales de unidades vendidas por cadena, linea y venta
totales_por_sede = df_ventas.groupby(['CADENA', 'LINEA', 'PUNTO DE VENTA'])['UNIDADES'].sum()

# Comparar las dos series para encontrar el peso de cada punto de venta
idx = pd.IndexSlice
subconjuntos_linea = totales_por_linea.loc[idx[:, :]]   # Hallar los subconjuntos excluyendo el
                                                                     # indice del punto de venta para poder
                                                                     # realizar la división correctamente
porcentajes_por_sede = (totales_por_sede / subconjuntos_linea)


# PROXIMA FASE - CREACION DEL FORMATO DE TARGET
'''
# Cargar el target a un dataframe
df_target = pd.read_excel(carpeta_target + archivo_target)

# Cambiar los nombres de las dos primeras columnas para que coincidan con los indices de la serie de porcentajes
df_target = df_target.rename(columns = {"CLIENTE": "CADENA", "LINEA LG": "LINEA"})

# Convertir las dos primeras columnas en índices para poder operar el dataframe con la serie
df_target = df_target.set_index(['CADENA', 'LINEA'])

# Hallar el target de unidades a vender en cada sede mensualmente
#monthly_target_units = df_target.mul(porcentajes_por_sede, level=['CADENA', 'LINEA'])
'''