from flask import Flask, jsonify, request
from services.users import Usuario, SECRET_KEY
from services.proposals import Proposta
from config.db_config import conectar_db

def proposals_route(app):

    @app.route('/sendProposal', methods=['POST'])
    def sendProposal():
        data = request.json

        if 'id_carro' in data and 'nome_proprietario' in data and 'nome_comprador' in data and 'descricao' in data and 'preco_proposto' in data:
            conexao_db, cursor = conectar_db()
            
            if conexao_db is None:
                return jsonify(cursor), 500
            
            # Pegando o id do comprador
            id_usuario = Usuario.get_user_id(data['nome_comprador'])
            id_proprietario = Usuario.get_user_id(data['nome_proprietario'])
            # Declarando q se os dados vieram todos no body da request, é criada uma nova instânica da classe 'Proposta'

            proposta = Proposta(data['id_carro'], id_proprietario, id_usuario, data['descricao'], data['preco_proposto'])
            response = Proposta.criar_proposta(proposta)

            return response
        
        else:
            return jsonify({'message': 'Erro ao enviar proposta! Preencha todos os campos corretamente.'}), 400
        

    @app.route('/showReceivedProposals', methods=['POST'])
    def showReceivedProposals():
        data = request.json
        print("Data received in showReceivedProposals:", data)

        if 'username' in data and 'situacao' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify(cursor), 500
            
            nome_proprietario = data['username']
            id_proprietario = Usuario.get_user_id(nome_proprietario)
            situacao = data['situacao']

            if situacao == 'nao_vista' or situacao == 'em_negociacao' or situacao == 'encerrada':
                response = Proposta.listar_propostas_recebidas(id_proprietario, situacao)
                if situacao == 'nao_vista' and response == None:
                    return jsonify({
                        'lista_propostas': [],
                        'message': 'Todas as propostas recebidas ja foram lidas!'
                    })
                
                elif situacao == 'em_negociacao' and response == None:
                    return jsonify({
                        'lista_propostas': [],
                        'message': 'Nenhuma proposta recebida, esta em negocição.'
                    })
                elif situacao == 'encerrada' and response == None:
                    return jsonify({
                        'lista_propostas': [],
                        'message': 'Nenhuma proposta recebida, foi encerrada. '
                    })
                    
                else: return response


            else:
                return jsonify({
                    'lista_propostas': [],
                    'message': 'Escolha uma situação de proposta correta!'
                })
            

    @app.route('/showSentProposals', methods=['POST'])    
    def showSendProposals():
        data = request.json

        if 'username' in data and 'situacao' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify(cursor), 500
            
            nome_comprador = data['username']
            id_proprietario = Usuario.get_user_id(nome_comprador)
            situacao = data['situacao']

            if situacao == 'nao_vista' or situacao == 'em_negociacao' or situacao == 'encerrada':
                response = Proposta.listar_propostas_enviadas(id_proprietario, situacao)
                if situacao == 'nao_vista' and response == None:
                    return jsonify({
                        'lista_propostas': [],
                        'message': 'Todas as propostas enviadas ja foram lidas!'
                    })
                
                elif situacao == 'em_negociacao' and response == None:
                    return jsonify({
                        'lista_propostas': [],
                        'message': 'Nenhuma proposta enviada, esta em negocição.'
                    })
                elif situacao == 'encerrada' and response == None:
                    return jsonify({
                        'lista_propostas': [],
                        'message': 'Nenhuma proposta enviada, foi encerrada. '
                    })
                    
                else: return response

            else:
                return jsonify({
                    'lista_propostas': [],
                    'message': 'Escolha uma situação de proposta correta!'
                })
            

    @app.route('/rejectProposal', methods=['PATCH'])
    def rejectProposal():

        data = request.json

        if 'id_proposta' in data:

            id_proposta = data['id_proposta']
            response = Proposta.rejeitar_proposta(id_proposta)

            return response
        
        else:
            return jsonify({'Erro ao recusar proposta! A proposta não foi passada corretamente ao servidor.'})
        
    # A convenção de restfull apis, dfine q em rotas com verbo DELETE o id do recurso deve ser passado como parâmetro na URL
    @app.route('/cancelProposal/<int:id_proposta>', methods=['DELETE'])
    def cancelProposal(id_proposta):

        response = Proposta.cancelar_proposta(id_proposta)

        return response if response else jsonify({'Erro ao cancelar proposta! A proposta não foi passada corretamente ao servidor.'})
        
    @app.route('/negotiateProposal', methods=['PATCH'])
    def negotiate_proposal():
        data = request.json

        if 'id_proposta' in data:

            id_proposta = data['id_proposta']
            response = Proposta.negociar_proposta(id_proposta)

            return response
        
        else:
            return jsonify({'Erro ao negociar proposta! A proposta não foi passada corretamente ao servidor.'})
        
    @app.route('/acceptProposal', methods=['PATCH'])
    def accept_proposal():
        data = request.json

        if 'id_proposta' in data:
            
            id_proposta = data['id_proposta']
            response = Proposta.aceitar_proposta(id_proposta)

            return response
        
        else:
            return jsonify({'Erro ao aceitar proposta! A proposta não foi passada corretamente ao servidor.'})







            
