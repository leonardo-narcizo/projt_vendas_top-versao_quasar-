### esse módulo terá a funcao que atualmente está contida na rota '/preco' da API

from users import conectar_db
from flask import jsonify

# Formato geral será:

def comparador(valor_min, valor_max, coluna, data):

    # Lidando com os os dois precos, retornando um intervalo de preço    
    if valor_min in data and valor_max in data:
        conexao_db, cursor = conectar_db()

        if conexao_db is None:
            return jsonify(cursor), 500
        
        cursor.execute(f'SELECT * FROM carros WHERE {coluna} >= %s AND {coluna} <= %s ORDER BY {coluna} ASC', (data[valor_min], data[valor_max]))
        rows = cursor.fetchall()

        carros = []

        for row in rows:
            carros.append({
                'id': row[0],
                'marca': row[1],
                'modelo': row[2],
                'ano': row[3],
                'quilometragem': row[4],
                'preco': row[5]                 
            })

        conexao_db.close()

        if not rows:
            return jsonify({'lista_carros': 'Ops! Não há carros nesse intervalo de preço'})
        else:
            return jsonify({'lista_carros': carros})


    # Se apenas o preço mínimo for enviado na requisição
    elif valor_min in data:
        conexao_db, cursor = conectar_db()
        
        if conexao_db is None:
             return jsonify(cursor), 500
         
        cursor.execute(f'SELECT * FROM carros WHERE {coluna} >= %s ORDER BY {coluna} ASC', (data[valor_min],))
        rows = cursor.fetchall()

        carros = []
        for row in rows:
            carros.append({
                'id': row[0],
                'marca': row[1],
                'modelo': row[2],
                'ano': row[3],
                'quilometragem': row[4],
                'preco': row[5]
            })

        conexao_db.close()

        if not rows:
            return jsonify({'lista_carros': f'Não há carros com preço maior do que {data['preco_minimo']} reais'})
        else:
            return jsonify({'lista_carros': carros})
        

    # Se apenas o valor máximo for enviado na requisição
    elif valor_max in data:
        conexao_db, cursor = conectar_db()

        if conexao_db is None:
            return jsonify(cursor), 500
        
        cursor.execute(f'SELECT * FROM carros WHERE {coluna} <= %s ORDER BY {coluna} ASC', (data['preco_maximo'],))
        rows = cursor.fetchall()

        carros = []
        for row in rows:
            carros.append({
                'id': row[0],
                'marca': row[1],
                'modelo': row[2],
                'ano': row[3],
                'quilometragem': row[4],
                'preco': row[5]               
            })

        conexao_db.close()


# essa função recebe 4 parâmetros 
# 1-valor_min: valor minimo que a coluna assume
# 2=valor_max: valor máximo que a coluna assume
# 3-coluna: o nome da coluna do bnco de dados, que será ultilizada. Serão preco, quilometragem e ano
# 4-data: este parâmetro esta em observação p/ ver se será colocado aqui, ou deixado diretamente na API principal, e representa o body da requisição o texto JSON
