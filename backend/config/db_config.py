import mysql.connector
from mysql.connector import Error

# Função para se conectar ao mysql
def conectar_db():
    try:
        conexao_db = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'projt_carros'
            )

        cursor = conexao_db.cursor()

        return conexao_db, cursor # A ordem deve ser mantida no código principal
    except Error as e:
        return None, {'[erro do banco]': str(e)} # Conexão mal-sucedida retorna uma tupla:
                                                 # Primeiro o None
                                                 # Depois o erro que é uma instância do mysql convertido para string