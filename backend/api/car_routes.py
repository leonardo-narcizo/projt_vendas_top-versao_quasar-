from flask import Flask, jsonify, request
import datetime
from services.users import Usuario, SECRET_KEY
from db.db_config import conectar_db
import base64




def car_routes(app):
    ### Rota para obter a lista 'Carros'
    @app.route('/carros', methods=['GET'])
    def mostrar_carros():
        conexao_db, cursor = conectar_db()

        # Verificando se há erro na conexão com o banco
        if conexao_db is None:
            return jsonify(cursor), 500
        
        cursor.execute('SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id')

        rows = cursor.fetchall()

        carros = []    
        for row in rows:
        
            carros.append(
                {
                'id': row[0],
                'marca': row[1],
                'modelo': row[2],
                'ano': row[3] ,
                'quilometragem': row[4],
                'preco': row[5],
                'proprietario': row[9]
                }
            )
        
        conexao_db.close()

        return jsonify({'lista_carros': carros})
        

    ### Rota para criar um carro novo

    # Proximos passos: Começar um projeto dentro do google cloud dai pegar a imagem codificada em base64 q chega la do frontend
    # e dai decodificar p binário novamente as imagens aq na API e armazenar dentro da pasta de uploads
    # e então fazer c q isso tudo seja armazenado na nuvem
    # Dai no banco na coluna 'car_image' será guardado apenas o caminho da imagem, p n sobrecarregar o banco(pois são grandes as imagens)

    ##### ROta completa cmomenada: 
#     @app.route('/criarCarro', methods=['POST'])
# def criar_carro():
#     data = request.json

#     if 'marca' in data and 'modelo' in data and 'ano' in data and 'quilometragem' in data and 'preco' in data and 'car_image' in data and 'username' in data:
#         conexao_db, cursor = conectar_db()

#         if conexao_db is None:
#             return jsonify(cursor), 500

#         # Decode the base64 image
#         if ',' in data['car_image']:
#             imagem_bytes = base64.b64decode(data['car_image'].split(',')[1])
#         else:
#             imagem_bytes = base64.b64decode(data['car_image'])

#         # Save the image to the filesystem
#         filename = secure_filename(f"{data['username']}_{data['modelo']}.png")
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         with open(file_path, 'wb') as f:
#             f.write(imagem_bytes)

#         # Atrelando o novo carro ao proprietário, através do username
#         id_usuario = Usuario.get_user_id(data['username'])  # Isso retorna o id do usuário que está logado

#         # Inserindo o carro no estoque, e ainda inserindo qual é o seu proprietário
#         cursor.execute('INSERT INTO carros (marca, modelo, ano, quilometragem, preco, usuario_id, car_image_path) VALUES (%s, %s, %s, %s, %s, %s, %s)',
#                        [data['marca'], data['modelo'], data['ano'], data['quilometragem'], data['preco'], id_usuario, file_path])
#         conexao_db.commit()
#         conexao_db.close()

#         return jsonify({'message': 'Carro cadastrado para venda!'}), 201
#     else:
#         return jsonify({'message': 'Não foi possível cadastrar o seu carro! Verifique os campos e tente novamente'}), 400


    @app.route('/criarCarro', methods=['POST'])
    def criar_carro():
        data = request.json

        if 'marca' in data and 'modelo' in data and 'ano' in data and 'quilometragem' in data and 'preco' in data and 'car_image' in data and 'username' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify(cursor), 500
            
            if ',' in data['car_image']:
                imagem_bytes = base64.b64decode(data['car_image'].split(',')[1])
            else:
                # Lidar com o erro ou retornar uma resposta apropriada
                return jsonify({'message': 'Formato inválido da imagem Base64'}), 400
                # Convertendo a imagem q virá em base64 para formato binário novamente
                imagem_bytes = base64.b64decode(data['car_image'].split(',')[1])  # Remove o prefixo 'data:image/png;base64,'
            
            
            # Atrelando o novo carro ao proprietário, através do username
            id_usuario = Usuario.get_user_id(data['username']) # Isso retorna o id do usuário que está logado

            # Inserindo o carro no estoque, e ainda inserindo qual é o seu proprietário
            cursor.execute('INSERT INTO carros (marca, modelo, ano, quilometragem, preco, usuario_id, car_image) VALUES (%s, %s, %s, %s, %s, %s, %s)', [data['marca'], data['modelo'], data['ano'], data['quilometragem'], data['preco'], id_usuario, imagem_bytes])
            conexao_db.commit()
            conexao_db.close()

            return jsonify({'message': 'carro cadastrado para venda!' }), 201
            
        else:
            return jsonify({'message': 'Não foi possivel cadastrar o seu carro! Verifique os campos e tente novamente'}), 400


    ### Rota para atualizar carro existente
    @app.route('/atualizarCarro/<int:id>', methods=['PATCH'])
    def atualizar_carro(id):
        data = request.json

        conexao_db, cursor = conectar_db()
        if conexao_db is None:
            return jsonify(cursor), 500
        
        cursor.execute('SELECT * FROM carros')
        carros = cursor.fetchall()
        carro_encontrado = False # Carro encontrado começa falso, e deve ficar True caso o id do parâmetro bata com o id de algum carro
        for carro in carros:
            if carro[0] == id: # Verficando se a coluna 'id' fethone([0]) da tupla carro, é igual ao 'id' passado como parâmetro 
                cursor.execute('UPDATE carros SET marca = %s, modelo = %s, ano = %s, quilometragem = %s, preco = %s WHERE id = %s', (data['marca'], data['modelo'], data['ano'], data['quilometragem'], data['preco'], carro[0]))
                conexao_db.commit()
                carro_encontrado = True
                break

        cursor.close()

        if not carro_encontrado:
            return jsonify({'message': '[erro] carro não encontrado.'}), 404
        else:
            return jsonify({'message': 'carro atualizado com sucesso!'}), 200
            
        
    ### Rota para comprar um carro (Quando o usuario logado atualmente compra um carro, requisitando esse endPoint,
    ### ele em vez de deletar o carro clicado, ira mudar na tabela carros: a coluna 'usuario_id' para o atual usuario,
    ### armazenado no localStorage do html la no frontend)
    @app.route('/sellCar', methods=['PATCH'])
    def handle_sell_car():
        data = request.json

        if 'comprador_username' in data and 'id_carro' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify(cursor), 500

            id_usuario = Usuario.get_user_id(data['comprador_username']) # Isso retorna o id do usuário que está logado

            cursor.execute('SELECT * FROM carros WHERE id = %s', (data['id_carro'],))
            carro = cursor.fetchone()

            if carro:
                id_novo_antigo_dono = carro[7]
                cursor.execute('UPDATE carros SET usuario_id = %s, id_antigo_dono = %s WHERE id = %s', 
                            (id_usuario, id_novo_antigo_dono, data['id_carro']))
                conexao_db.commit()

                # Depois da compra, atualizar a coluna 'data_compra' (essa coluna agr foi atualizda p type 'DATETIME')
                data_atual = datetime.datetime.now()

                cursor.execute('UPDATE carros SET data_compra = %s WHERE id = %s', 
                            (data_atual, data['id_carro']))
                conexao_db.commit()
                cursor.close()
                return jsonify({'message': 'carro vendido com sucesso!'}), 200
            else:
                return jsonify({'message': '[erro] carro não encontrado.'}), 404
        else:
            return jsonify({'message': '[erro] Dados insuficientes fornecidos.'}), 400


                
        

    ### Rota para retornar uma marca especifica
    @app.route('/marca', methods=['GET', 'POST'])
    def buscar_marca():
        data = request.json

        if 'marca' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify(cursor), 500
            
            cursor.execute('SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE marca = %s', (data['marca'],)) # Passando uma tupla com apenas um elemento, logo é preciso o uso da vírgula no final
            rows = cursor.fetchall()

            carros = []
            for row in rows:
                carros.append({
                    'id': row[0],
                    'marca': row[1],
                    'modelo': row[2],
                    'ano': row[3],
                    'quilometragem': row[4],
                    'preco': row[5],
                    'proprietario': row[9]
                })

            conexao_db.close()

            if not rows:
                return jsonify({
                    'lista_carros': [],
                    'message': 'fabricante não encontrada'}), 404
            else:
                return jsonify({'lista_carros': carros}), 200
            
            

    ### Rota para retornar modelos específicos
    @app.route('/modelo', methods=['POST'])
    def buscar_modelo():
        data = request.json

        if 'modelo' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify(cursor), 500
            
            cursor.execute('SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE modelo = %s', (data['modelo'],))
            rows = cursor.fetchall()

            carros = []
            for row in rows:
                carros.append({
                    'id': row[0],
                    'marca': row[1],
                    'modelo': row[2],
                    'ano': row[3],
                    'quilometragem': row[4],
                    'preco': row[5],
                    'proprietario': row[9]
                })

            conexao_db.close()

            if not rows:
                return jsonify({'lista_carros': [],
                                'message': 'modelo não encontrado'}), 404
            else:
                return jsonify({'lista_carros': carros}), 200
            

    ### Rota para retornar intervalo de preço
    @app.route('/preco', methods=['POST'])
    def buscar_intervalo_preco():
        data = request.json

        if 'preco_minimo' in data and 'preco_maximo' in data:
            preco_minimo = data['preco_minimo']
            preco_maximo = data['preco_maximo']

            # Verificando se os dois campos são não nulos
            if preco_minimo != "" and preco_maximo != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE preco >= %s AND preco <= %s ORDER BY preco ASC'
                params = (preco_minimo, preco_maximo)
                message = f'Ops! Não há carros nesse intervalo de preço'

            # Verificando se foi passado apenas o campo 'preco_minimo'
            elif preco_minimo != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE preco >= %s ORDER BY preco ASC'
                params = (preco_minimo,)
                message = f'Não há carros com preço maior do que {preco_minimo} reais'
            
            # Verificando se foi passado apenas o campo 'preco_maximo'
            elif preco_maximo != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE preco <= %s ORDER BY preco ASC'
                params = (preco_maximo,)
                message = f'Não há carros com o preço menor que {preco_maximo}'

            conexao_db, cursor = conectar_db()
            if conexao_db is None:
                return jsonify(cursor), 500

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conexao_db.close()

            carros = [{
                'id': row[0],
                'marca': row[1],
                'modelo': row[2],
                'ano': row[3],
                'quilometragem': row[4],
                'preco': row[5],
                'proprietario': row[9]
            } for row in rows]

            if not carros:
                return jsonify({'lista_carros': [],
                                'message': message}), 404
            else:
                return jsonify({'lista_carros': carros})
            

    ### Rota para retornar intervalo de ano
    @app.route('/ano', methods=['POST'])
    def buscar_intervalo_ano():
        data = request.json

        if 'ano_minimo' in data and 'ano_maximo' in data:
            ano_minimo = data['ano_minimo']
            ano_maximo = data['ano_maximo']

            # Verificando se os dois campos são não nulos
            if ano_minimo != "" and ano_maximo != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE ano >= %s AND ano <= %s ORDER BY ano ASC'
                params = (ano_minimo, ano_maximo)
                message = f'Ops! Não há carros nesse intervalo de ano'

            # Verificando se foi passado apenas o campo 'ano_minimo'
            elif ano_minimo != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE ano >= %s ORDER BY ano ASC'
                params = (ano_minimo,)
                message = f'Não há carros lançados em anos superiores ao ano de {ano_minimo}'
            
            # Verificando se foi passado apenas o campo 'ano_maximo'
            elif ano_maximo != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE ano <= %s ORDER BY ano ASC'
                params = (ano_maximo,)
                message = f'Não há carros lançados antes de {ano_maximo}'

            conexao_db, cursor = conectar_db()
            if conexao_db is None:
                return jsonify(cursor), 500

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conexao_db.close()

            carros = [{
                'id': row[0],
                'marca': row[1],
                'modelo': row[2],
                'ano': row[3],
                'quilometragem': row[4],
                'preco': row[5],
                'proprietario': row[9]
            } for row in rows]

            if not carros:
                return jsonify({'lista_carros': [],
                                'message': message}), 404
            else:
                return jsonify({'lista_carros': carros})
            

    # Rota para retornar intervalo de quilometragem
    @app.route('/quilometragem', methods=['POST'])
    def buscar_intervalo_quilometragem():
        data = request.json

        if 'quilometragem_minima' in data and 'quilometragem_maxima' in data:
            quilometragem_minima = data['quilometragem_minima']
            quilometragem_maxima = data['quilometragem_maxima']

            # Verificando se os dois campos são não nulos
            if quilometragem_minima != "" and quilometragem_maxima != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE quilometragem >= %s AND quilometragem <= %s ORDER BY quilometragem ASC'
                params = (quilometragem_minima, quilometragem_maxima)
                message = f'Ops! Não há carros nesse intervalo de quilometragem'

            # Verificando se foi passado apenas o campo 'quilometragem_minima'
            elif quilometragem_minima != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE quilometragem >= %s ORDER BY quilometragem ASC'
                params = (quilometragem_minima,)
                message = f'Não há carros com quilometragem maior que {quilometragem_minima}'

            # Verificando se foi passado apenas o campo 'quilometragem_maxima'
            elif quilometragem_maxima != "":
                query = 'SELECT carros.*, usuarios.username FROM carros LEFT JOIN usuarios ON carros.usuario_id = usuarios.id WHERE quilometragem <= %s ORDER BY quilometragem ASC'
                params = (quilometragem_maxima,)
                message = f'Não há carros com quilometragem menor que {quilometragem_maxima}'

            conexao_db, cursor = conectar_db()
            if conexao_db is None:
                return jsonify(cursor), 500

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conexao_db.close()

            carros = [{
                'id': row[0],
                'marca': row[1],
                'modelo': row[2],
                'ano': row[3],
                'quilometragem': row[4],
                'preco': row[5],
                'proprietario': row[9]
            } for row in rows]

            if not carros:
                return jsonify({'lista_carros': [],
                                'message': message}), 404
            else:
                return jsonify({'lista_carros': carros})
