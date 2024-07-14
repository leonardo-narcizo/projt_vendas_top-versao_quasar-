from datetime import datetime
from config.db_config import conectar_db

def formatar_data_brasileira(data):
    # Como o banco pode retornar um objeto 'datetime', primeiro verificamos se a data enviada no parâmetro, é uma instância de datetime. Ai converte a data para string.
    # Após isso, converte a data, p o formato brai=sileiro, p entao ser enviado p/ frontend 
    if isinstance(data, datetime):
        return data.strftime('%d/%m/%Y %H:%M:%S')
    try:
        data_obj = datetime.strptime(data, '%a, %d %b %Y %H:%M:%S %Z')
        return data_obj.strftime('%d/%m/%Y %H:%M:%S')
    except ValueError:
        return data
