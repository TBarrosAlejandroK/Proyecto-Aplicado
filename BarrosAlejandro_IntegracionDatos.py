# =====================================================
# PROYECTO: Calidad del Aire en la ciudad de Quito
# Script: Integración con Base de Datos SQL (SQLite)
# Autor: Kevin Alejandro Barros Travez
# ====================================================

# ==========================================                              ==========================================================================
# 1. IMPORTACIÓN DE LIBRERÍAS                                             COMENTARIOS
# ==========================================                              ==========================================================================
import pandas as pd                                                       #Librería principal para el manejo de datos 
import sqlite3                                                            #Librería de Python para trabajar con bases de datos SQL

# ==========================================
# 2. CARGA Y PRPARACIÓN DEL DATASET
# ==========================================

def cargar_info(dataset):                                                 #Función que recibe como argumento la ruta del archivo del dataset
    try:                                                                  #Sentencia establecida para el manejo de excepciones 
        df = pd.read_excel(dataset)                                       #Conversión del archivo del dataset a un DataFrame

        df.columns = ["date", "NO2", "SO2", "CO", "O3",
                      "PM25", "rain", "temperature",
                      "solar_radiation", "wind_speed", "humidity"]        #Reenombramiento de las columnas

        df['date'] = pd.to_datetime(df['date'])                           #Conversión de la columna date a un formato de fecha real

        print("Los datos has sido cargados correctamente")                #Confirmación de que el DataFrame tiene información
        return df                                                         #Devolución del DataFrame para ser usado en funciones

    except Exception as error:                                            #Sentencia para capturar una excepción
        print("Error al cargar datos:", error)                            #Confirmación y presentación en caso de que se genere una excepción
        return None                                                       #Devolución de un valor None en caso de capturar un error


# ========================================================
# 2. GENERACIÓN DE UNA BASE DE DATOS Y CONSULTAS SQL
# ========================================================

def base_sql(df):                                                         #Defición de una función que recibe como argumento el DataFrame para ser usado en consultas SQL
    try:                                                                  #Sentencia establecida para el manejo de excepciones 
        connect_to_sql = sqlite3.connect("proyecto_aire.db")              #Crea una base de datos SQLite con el nombre de archivo "proyecto_aire.db"

        df.to_sql("calidad_aire", connect_to_sql, if_exists="replace", index=False) #Almacenamiento del DataFrame como tabla SQL

        query1 = """
        SELECT AVG(PM25) as Promedio_PM25,
               AVG(NO2) as Promedio_NO2
        FROM calidad_aire
        """

        consulta1 = pd.read_sql(query1, connect_to_sql)                    #Ejecución de la consulta 1 y devolución del resultado como DataFrame
 
        print("\nConsulta SQL 1 (Promedios generales):")                     #Visualización de la consulta 1
        print(consulta1)

        if 'date' in df.columns:

            query2 = """
            SELECT
               strftime('%Y-%m', date) AS mes,
               AVG(PM25) AS Promedio_PM25
            FROM calidad_aire
            GROUP BY mes
            ORDER BY mes
            """

            consulta2 = pd.read_sql(query2, connect_to_sql)                #Ejecución de la consulta 2 y devolución del resultado como DataFrame

            print("\n Consulta SQL 2 (PM2.5 promedio por mes):")           #Visualización de la consulta 2
            print(consulta2)

        connect_to_sql.close()                                             #Cierre de la conexión con la base de datos SQL

    except Exception as error:                                             #Sentencia para capturar una excepción
        print("Error en la consulta SQL:", error)                          #Confirmación y presentación en caso de que se genere una excepción

# ==========================================
# 4. ANÁLISIS EXPLORATORIO ADICIONAL
# ==========================================

def analisis_sql(df):                                                      #Definción de una función que recibe como argumento el DataFrame para generar analisis de variables
    try:
        connect_to_sql = sqlite3.connect("proyecto_aire.db")               #Abre la base de datos SQL nombrada como "proyecto_aire.db"

        df.to_sql("calidad_aire", connect_to_sql, if_exists="replace", index=False)  #Almacenamiento del DataFrame como tabla SQL

        query3 = "SELECT PM25, NO2 FROM calidad_aire"
        consulta3 = pd.read_sql(query3, connect_to_sql)                     #Ejecución de la consulta 3 y devolución del resultado como DataFrame

        correlacion = consulta3.corr().iloc[0, 1]                           #Calcula la correlacion entre las columnas 0 y 1 correspondientes a PM2.5 y NO2
        print(f"\nCorrelación entre PM2.5 & NO2: {correlacion:.2f}")

        connect_to_sql.close()                                              #Cierre de la conexión con la base de datos SQL

    except Exception as error:                                              #Sentencia para capturar una excepción
        print("Error al calcular la correlación:", error)                   #Confirmación y presentación en caso de que se genere una excepción


# ==========================================
# 5. PROGRAMA PRINCIPAL
# ==========================================

def main():                                                                 #Definición de una función principal para ejecutar las funciones antes definidas
    ruta = "Data_2023_2024_elCrisis.xlsx"                                   #Definición del nombre del dataset

    df = cargar_info(ruta)                                                  #Cargar el dataset en un DataFrame

    if df is not None:                                                      #Verificar si el dataset se cargo correctamente
        base_sql(df)                                                        #Almacenar los datos en la función para SQL
        analisis_sql(df)                                                        #Calcular la correlacion usando SQL

if __name__ == "__main__":                                                  #Ejecución del script
    main()
