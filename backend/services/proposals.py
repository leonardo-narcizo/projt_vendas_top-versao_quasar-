from db.db_config import conectar_db
from .date_service import formatar_data_brasileira
from .users import Usuario
from flask import jsonify
import datetime
from mysql.connector import Error

class Proposta:
    def __init__(self, id_carro, id_proprietario, id_comprador, descricao, preco_proposto):
        self.id_carro = id_carro
        self.id_proprietario = id_proprietario
        self.id_comprador = id_comprador
        self.descricao = descricao
        self.preco_proposto = preco_proposto
        self.data_proposta = datetime.datetime.now()
        self.situacao = 'nao_vista'

    def criar_proposta(self):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                INSERT INTO propostas (id_carro, id_proprietario, id_usuario_comprador, descricao, preco_proposto, data_proposta, situacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (self.id_carro, self.id_proprietario, self.id_comprador, self.descricao, self.preco_proposto, self.data_proposta, self.situacao))

            conexao_db.commit()
            cursor.close()
            return jsonify({'message': 'Proposta enviada com sucesso!'}), 201
        except Exception as e:
            return jsonify({'message': str(e)})
        

    @staticmethod
    def listar_propostas_recebidas(usuario_id, situacao):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                SELECT p.id_proposta, p.id_carro, c.marca, c.modelo, p.id_proprietario, c.id_antigo_dono, p.id_usuario_comprador, u.username AS comprador_username, p.data_proposta, p.descricao, p.preco_proposto, p.situacao, p.conclusao
                FROM propostas p
                JOIN usuarios u ON p.id_usuario_comprador = u.id
                JOIN carros c ON p.id_carro = c.id
                WHERE p.id_proprietario = %s AND p.situacao = %s
            ''', (usuario_id, situacao))
            rows = cursor.fetchall()

            propostas = []

            for row in rows:
                propostas.append({
                    'id_proposta': row[0],
                    'id_carro': row[1],
                    'marca': row[2],
                    'modelo': row[3],
                    'id_proprietario': row[4],
                    'id_antigo_dono': row[5],
                    'proprietario_username': Usuario.get_username_by_id(row[4]), #muda p dono atual legítmo
                    'comprador_username': row[7],
                    'data_proposta': formatar_data_brasileira(row[8]),
                    'descricao': row[9],
                    'preco_proposto': row[10],
                    'situacao': row[11],
                    'conclusao': row[12]
                })

            cursor.close()

            if not propostas:
                return None
            
            return jsonify({'lista_propostas': propostas})

            
        except Exception as e:
            return jsonify({'message': str(e)})


    @staticmethod
    def listar_propostas_enviadas(usuario_id, situacao):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                SELECT p.id_proposta, p.id_carro, c.marca, c.modelo, p.id_proprietario, p.id_usuario_comprador, u.username AS proprietario_username, p.data_proposta, p.descricao, p.preco_proposto, p.situacao, p.conclusao
                FROM propostas p
                JOIN usuarios u ON p.id_proprietario = u.id
                JOIN carros c ON p.id_carro = c.id
                WHERE id_usuario_comprador = %s AND p.situacao = %s
            ''', (usuario_id, situacao))
            rows = cursor.fetchall()

            propostas = []

            for row in rows:
                propostas.append({
                    'id_proposta': row[0],
                    'id_carro': row[1],
                    'marca': row[2],
                    'modelo': row[3],
                    'id_proprietario': row[4],
                    'comprador_username': Usuario.get_username_by_id(row[5]),
                    'proprietario_username': row[6],
                    'data_proposta': formatar_data_brasileira(row[7]),
                    'descricao': row[8],
                    'preco_proposto': row[9],
                    'situacao': row[10],
                    'conclusao': row[11]
                })

            cursor.close()

            if not propostas:
                return None
            
            return jsonify({'lista_propostas': propostas})

            
        except Error as e:
            return jsonify({'message': str(e)})
        

    @staticmethod
    def rejeitar_proposta(id_proposta):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                UPDATE propostas
                SET situacao = 'encerrada', conclusao = 'recusada'
                WHERE id_proposta = %s
            ''', (id_proposta,))

            conexao_db.commit()
            cursor.close()

            return jsonify({'message': 'Proposta recusada com sucesso!'})

        except Exception as e:
            return jsonify({'message': str(e)})
        

    @staticmethod
    def aceitar_proposta(id_proposta):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                UPDATE propostas
                SET situacao = 'encerrada', conclusao = 'aceita'
                WHERE id_proposta = %s
            ''', (id_proposta,))

            conexao_db.commit()
            cursor.close()

            return jsonify({'message': 'Proposta aceita com sucesso!'})

        except Exception as e:
            return jsonify({'message': str(e)})
        

    @staticmethod
    def cancelar_proposta(id_proposta):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                DELETE FROM propostas
                WHERE id_proposta = %s
            ''', (id_proposta,))

            conexao_db.commit()
            cursor.close()

            return jsonify({'message': 'Proposta cancelada com sucesso!'})

        except Exception as e:
            return jsonify({'message': str(e)})
        

    @staticmethod
    def negociar_proposta(id_proposta):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                UPDATE propostas
                SET situacao = 'em_negociacao'
                WHERE id_proposta = %s
            ''', (id_proposta,))

            conexao_db.commit()
            cursor.close()

            return jsonify({'message': 'Proposta colocada em negociação!'})

        except Exception as e:
            return jsonify({'message': str(e)})
