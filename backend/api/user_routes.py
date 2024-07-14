from flask import Flask, jsonify, request
from services.users import Usuario, SECRET_KEY
from config.db_config import conectar_db


def user_routes(app):
    ### Rota para entrar em uma conta, usando a classe Usuário
    @app.route('/entrar', methods=['GET', 'POST'])
    def entrar_conta():
        data = request.json

        if 'username' in data and 'password' in data:
            
            # Declarando que se os dados da requisição forem bem sucedidos, o usuario vira uma nova instânica da classe 'Usuario'
            usuario = Usuario(data['username'], data['password'])

            # Autenticando o usuário inserido pelos input do frontend
            response = usuario.autenticar()
            return response # Já está convertida em json no módulo 'users'
        
        else:
            return jsonify({'message': 'Erro ao entrar! Estão faltando campos na requisição'})
        

    ### Rota para criar um novo usuário, usando a classe 'Usuário'
    @app.route('/criarConta', methods=['POST'])
    def criar_conta():
        data = request.json

        if 'new_username' in data and 'new_password' in data:
            
            # Tratando possivel cnpj q vem na request
            if 'cnpj' in data:
                response = Usuario.criar_usuario(data['new_username'], data['new_password'], data['cnpj'])

                return response
            
            # Criando uma nova instância da classe 'Usuario' para acessar o método estático que insere o novo usuário no banco
            response = Usuario.criar_usuario(data['new_username'], data['new_password'])

            return response
        
        # Tratando possiveis erros ao criar conta
        else:
            return jsonify({'message': 'Não foi possivel criar a sua conta. Verifique se preencheu os campo corretamente.'}), 400
