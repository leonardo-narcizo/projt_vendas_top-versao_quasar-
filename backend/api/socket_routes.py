from flask_socketio import SocketIO, emit, send, join_room, leave_room
from config.db_config import conectar_db
from services.users import Usuario
from services.chat_service import ChatService



def socket_routes(socketio):
    @socketio.on('create_chat')
    def handle_create_chat(data):
        print(data)
        if 'proprietario_username' in data and 'comprador_username' in data and 'id_carro' in data:

            id_proprietario = Usuario.get_user_id(data['proprietario_username'])
            id_comprador = Usuario.get_user_id(data['comprador_username'])
            response = ChatService.create_chat(id_proprietario, id_comprador, data['id_carro'])

            if response is None:
                emit('error', {'message': 'Erro ao criar chat!'})
            else:
                emit('chat_created', {'message': 'Chat criado com sucesso!', 'new_chat_id': response})

                
            
        else:
            emit('data_error', {'message': 'Dados inválidos para criar um novo chat!'})


    @socketio.on('show_buyer_chats')
    def handle_show_buyer_chats(data):
        print('Evento show_buyer_chats recebido:', data)
        if 'username' in data:
            id_usuario = Usuario.get_user_id(data['username'])
            response = ChatService.get_buyer_chats(id_usuario)

            if response is None:
                emit('error', {'message': 'Ocorreu um erro ao buscar suas conversas!'})
            else:
                emit('found_chats', {'chats': response})

        else:
            emit('data_error', {'message': 'Dados inválidos para buscar conversas!'})


    @socketio.on('show_seller_chats')
    def handle_show_seller_chats(data):
        print('Evento show_seller_chats recebido:', data)
        if 'username' in data:
            id_usuario = Usuario.get_user_id(data['username'])
            response = ChatService.get_seller_chats(id_usuario)

            if response is None:
                emit('error', {'message': 'Ocorreu um erro ao buscar suas conversas!'})
            else:
                emit('found_chats', {'chats': response})
                print('Response foi enviada')

        else:
            emit('data_error', {'message': 'Dados inválidos para buscar conversas!'})


    @socketio.on('show_chat_messages')
    def handle_show_chat_messages(data):
        if 'id_chat' in data:
            response = ChatService.get_chat_messages(data['id_chat'])

            if response is None:
                emit('error', {'message': 'Ocorre um erro ao buscar o historico de mensagens dessa conversa!'})
            else:
                emit('found_messages', {'messages': response})
                join_room(data['id_chat'])

        else:
            emit('data_error', {'message': 'É necessário o id do chat!'})
        

    @socketio.on('send_message')
    def handle_send_message(data):
        print('mensagem recebida p slavar')
        if 'id_chat' in data and 'username_participante' in data and 'conteudo' in data:
            id_participante = Usuario.get_user_id(data['username_participante'])
            response = ChatService.save_message(data['id_chat'], id_participante, data['conteudo'])
            if response is None or response is False:
                emit('error', {'message': 'Erro ao enviar mensagem!'})
            else:
                
                emit('sent_message', response, room=data['id_chat'])
        else:
            emit('data_error', {'message': 'Dados inválidos para enviar mensagem!'})


    # Definindo a rota para entrar em um chat
    @socketio.on('join_chat')
    def handle_join_chat(data):
        if 'id_chat' in data:
            join_room(data['id_chat'])
            emit('status', {'message': f'Entrou no chat {data["id_chat"]}'}, room=data['id_chat'])
        else:
            emit('data_error', {'message': 'ID do chat é necessário!'})

    # Definindo a rota para sair de um chat
    @socketio.on('leave_chat')
    def handle_leave_chat(data):
        if 'id_chat' in data:
            leave_room(data['id_chat'])
            emit('status', {'message': f'Saiu do chat {data["id_chat"]}'}, room=data['id_chat'])
        else:
            emit('data_error', {'message': 'ID do chat é necessário!'})