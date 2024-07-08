from db.db_config import conectar_db
from services.users import Usuario
from flask import jsonify
import datetime
from services.date_service import formatar_data_brasileira

class ChatService:

    @staticmethod
    def save_message(id_chat, id_participante, conteudo, tipo_mensagem='texto'):
        conexao_db, cursor = conectar_db()

        try:
            data_envio = datetime.datetime.now()
            cursor.execute('''
                INSERT INTO mensagens_chat (id_chat, id_participante, conteudo, data_envio, tipo_mensagem)
                VALUES (%s, %s, %s, %s, %s)
            ''', (id_chat, id_participante, conteudo, data_envio, tipo_mensagem))

            conexao_db.commit()

            sent_message_id = cursor.lastrowid  # Pega o ID do último registro feito na tabela

            # Executa a query para pegar os detalhes do último registro inserido
            cursor.execute('''
                SELECT m.id_mensagem, m.id_participante, u.username, m.conteudo, m.data_envio, m.tipo_mensagem
                FROM mensagens_chat m
                JOIN usuarios u ON m.id_participante = u.id
                WHERE m.id_mensagem = %s
            ''', (sent_message_id,))

            last_message = cursor.fetchone()
            cursor.close()

            if last_message:
                return {
                    'id_mensagem': last_message[0],
                    'id_participante': last_message[1],
                    'username': last_message[2],
                    'conteudo': last_message[3],
                    'data_envio': formatar_data_brasileira(last_message[4]),
                    'tipo_mensagem': last_message[5]
                }
            else:
                return None
        except Exception as e:
            conexao_db.rollback()
            return False


    @staticmethod
    def get_chat_messages(id_chat):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                SELECT m.id_mensagem, m.id_participante, u.username, m.conteudo, m.data_envio, m.tipo_mensagem
                FROM mensagens_chat m
                JOIN usuarios u ON m.id_participante = u.id
                WHERE m.id_chat = %s
                ORDER BY m.data_envio ASC
            ''', (id_chat,))

            rows = cursor.fetchall()
            mensagens = []

            for row in rows:
                mensagens.append({
                    'id_mensagem': row[0],
                    'id_participante': row[1],
                    'username': row[2],
                    'conteudo': row[3],
                    'data_envio': formatar_data_brasileira(row[4]),
                    'tipo_mensagem': row[5]
                })

            cursor.close()
            return mensagens
        except Exception as e:
            return None

    @staticmethod
    def create_chat(id_proprietario, id_comprador, id_carro):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                INSERT INTO chats (id_proprietario, id_comprador, id_carro)
                VALUES (%s, %s, %s)
            ''', (id_proprietario, id_comprador, id_carro))

            conexao_db.commit()
            chat_id = cursor.lastrowid # Pega o id do último registro feito na tabela
            cursor.close()
            return chat_id
        except Exception as e:
            conexao_db.rollback()
            return None
        

    @staticmethod
    def get_buyer_chats(id_usuario):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                        SELECT chats.*, c.marca, c.modelo
                        FROM chats
                        INNER JOIN carros c
                        ON chats.id_carro = c.id
                        WHERE id_comprador = %s
                        ''', (id_usuario,))
            chat_data = cursor.fetchall()

            cursor.close()

            chats = []

            for chat in chat_data:
                chats.append(
                    {
                        'id_chat': chat[0],
                        'username_proprietario': Usuario.get_username_by_id(chat[1]),
                        'username_comprador': Usuario.get_username_by_id(chat[2]),
                        'id_carro': chat[3], # Futuramente criar 'cars_service' p pegar dados do carro por meio do id dele
                        'marca': chat[4],
                        'modelo': chat[5]
                    }
                )

           
            return chats

        except Exception as e:
            return None
        

    @staticmethod
    def get_seller_chats(id_usuario):
        conexao_db, cursor = conectar_db()

        try:
            cursor.execute('''
                        SELECT chats.*, c.marca, c.modelo
                        FROM chats
                        INNER JOIN carros c
                        ON chats.id_carro = c.id
                        WHERE id_proprietario = %s
                        ''', (id_usuario,))
            
            chat_data = cursor.fetchall()

            cursor.close()

            chats = []

            for chat in chat_data:
                chats.append(
                    {
                        'id_chat': chat[0],
                        'username_proprietario': Usuario.get_username_by_id(chat[1]),
                        'username_comprador': Usuario.get_username_by_id(chat[2]),
                        'id_carro': chat[3], # Futuramente criar 'cars_service' p pegar dados do carro por meio do id dele
                        'marca': chat[4],
                        'modelo': chat[5]
                    }
                )

            return chats

        except Exception as e:
            return None
