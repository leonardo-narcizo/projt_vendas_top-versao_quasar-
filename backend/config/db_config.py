import mysql.connector
from mysql.connector import Error
import os


# Função para se conectar ao mysql
def conectar_db():
    try:
        conexao_db = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
            )

        cursor = conexao_db.cursor()

        return conexao_db, cursor # A ordem deve ser mantida no código principal
    except Error as e:
        return None, {'[erro do banco]': str(e)} # Conexão mal-sucedida retorna uma tupla:
                                                 # Primeiro o None
                                                 # Depois o erro que é uma instância do mysql convertido para string