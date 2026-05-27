import mysql.connector

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",      
            user="root",           
            password="s3rv3r", 
            database="clinica_db"  
        )
        return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None