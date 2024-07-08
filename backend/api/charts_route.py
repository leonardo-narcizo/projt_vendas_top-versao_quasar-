import matplotlib
matplotlib.use('Agg')  # Configuração do matplotlib para uso em ambientes sem display
from flask import Flask, jsonify, request, send_file
from services.users import Usuario, SECRET_KEY
from db.db_config import conectar_db
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import io
from functools import wraps
import jwt


# Decorador para exigir token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token é necessário!'}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']

            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify({'error': 'Erro de conexão com o banco de dados.'}), 500
            
            cursor.execute('SELECT user_type FROM usuarios WHERE username = %s', (current_user,))
            user_type = cursor.fetchone()[0]

            if user_type != 'empresa':
                return jsonify({'message': 'Você não possui permissões para acessar insights!'}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 403

        return f(current_user, *args, **kwargs)

    return decorated

def criar_rotas_graficos(app):

    @app.route('/verificar_permissao', methods=['POST'])
    def verificar_permissao():
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token é necessário!'}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']

            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify({'error': 'Erro de conexão com o banco de dados.'}), 500
            
            cursor.execute('SELECT user_type FROM usuarios WHERE username = %s', (current_user,))
            user_type = cursor.fetchone()[0]

            if user_type == 'empresa':
                return jsonify({'message': 'Permissão concedida!', 'user_type': user_type}), 200
            else:
                return jsonify({'message': 'Você não possui permissões para acessar insights!', 'user_type': user_type}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 403

    @app.route('/grafico_compras', methods=['POST'])
    @token_required
    def grafico_compras(current_user):
        data = request.json

        if 'username' in data and 'inicio' in data and 'fim' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify({'error': 'Erro de conexão com o banco de dados.'}), 500

            cursor.execute('SELECT DATE(data_compra), COUNT(*) FROM carros WHERE usuario_id = (SELECT id FROM usuarios WHERE username = %s) AND data_compra BETWEEN %s AND %s GROUP BY DATE(data_compra)', (data['username'], data['inicio'], data['fim']))
            resultados = cursor.fetchall()

            datas, quantidades = zip(*resultados) if resultados else ([], [])

            # Limpar a figura
            plt.clf()

            plt.figure(figsize=(8, 9))
            plt.bar(datas, quantidades, width=4)
            plt.title('Quantidade de Carros Comprados por Dia')
            plt.ylabel('Quantidade')
            max_quantidade = max(quantidades) if quantidades else 0
            plt.yticks(np.arange(0, max_quantidade + 1, 1))
            plt.xlabel('Data da Compra')
            datas_formatadas = [datetime.strptime(str(data), '%Y-%m-%d').strftime('%d/%m/%Y') for data in datas]
            plt.xticks(ticks=datas, labels=datas_formatadas, rotation=45, ha='right') 

            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)

            conexao_db.close()

            return send_file(img_bytes, mimetype='image/png')
        else:
            return jsonify({'error': 'Dados de entrada incompletos.'}), 400

    @app.route('/grafico_vendas', methods=['POST'])
    @token_required
    def grafico_vendas(current_user):
        data = request.json

        if 'username' in data and 'inicio' in data and 'fim' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify({'error': 'Erro de conexão com o banco de dados.'}), 500

            cursor.execute('''
                SELECT DATE(data_compra), COUNT(*) 
                FROM carros 
                WHERE id_antigo_dono = (SELECT id FROM usuarios WHERE username = %s) 
                AND data_compra BETWEEN %s AND %s 
                GROUP BY DATE(data_compra)
            ''', (data['username'], data['inicio'], data['fim']))
            resultados = cursor.fetchall()

            datas, quantidades = zip(*resultados) if resultados else ([], [])

            # Limpar a figura
            plt.clf()

            plt.figure(figsize=(8, 9))
            plt.bar(datas, quantidades, width=0.9)
            plt.title('Quantidade de Carros Vendidos por Dia')
            plt.ylabel('Quantidade')
            max_quantidade = max(quantidades) if quantidades else 0
            plt.yticks(np.arange(0, max_quantidade + 1, 1))
            plt.xlabel('Data da Venda')
            datas_formatadas = [datetime.strptime(str(data), '%Y-%m-%d').strftime('%d/%m/%Y') for data in datas]
            plt.xticks(ticks=datas, labels=datas_formatadas, rotation=45, ha='right') 

            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)

            conexao_db.close()

            return send_file(img_bytes, mimetype='image/png')
        else:
            return jsonify({'error': 'Dados de entrada incompletos.'}), 400




    @app.route('/grafico_lucro', methods=['POST'])
    def grafico_lucro():
        data = request.json

        if 'username' in data and 'inicio' in data and 'fim' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify({'error': 'Erro de conexão com o banco de dados.'}), 500

            cursor.execute('SELECT SUM(preco_venda - preco_compra) FROM carros WHERE usuario_id = (SELECT id FROM usuarios WHERE username = %s) AND data_venda BETWEEN %s AND %s', (data['username'], data['inicio'], data['fim']))
            total_lucro = cursor.fetchone()[0]

            conexao_db.close()

            plt.bar(['Lucro'], [total_lucro])
            plt.title('Lucro Obtido')
            plt.ylabel('Valor (R$)')
            plt.xlabel('Ações')

            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)

            return send_file(img_bytes, mimetype='image/png')
