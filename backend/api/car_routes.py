from flask import Flask, jsonify, request
import datetime
from services.users import Usuario, SECRET_KEY
from services.cars_service import CarsService
from db.db_config import conectar_db
from google.cloud import storage
import uuid
import os
import time

storage_client = storage.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
bucket_name = 'images_car_sp'






def car_routes(app, socketio):
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
                'proprietario': row[10],
                'car_image': row[9]
                }
            )
        
        conexao_db.close()

        return jsonify({'lista_carros': carros})
    

    ### Rota para cadastrar novo carro
    @app.route('/criarCarro', methods=['POST'])
    def criar_carro():
        try:
            start_time = time.time()
            # Recebe os dados do formulário e a imagem do carro
            marca = request.form.get('marca')
            modelo = request.form.get('modelo')
            ano = request.form.get('ano')
            quilometragem = request.form.get('quilometragem')
            preco = request.form.get('preco')
            username = request.form.get('username')
            car_image = request.files.get('car_image')

            # Validação dos dados
            if not marca or not modelo or not ano or not quilometragem or not preco or not username or not car_image:
                return jsonify({'message': 'Preencha todos os campos e anexe uma imagem'}), 400

            # Gerar um nome único para o arquivo no Cloud Storage
            filename = str(uuid.uuid4()) + '-' + car_image.filename
            blob = storage_client.bucket(bucket_name).blob(filename)

            upload_start = time.time()
            # Upload da imagem para o Google Cloud Storage
            blob.upload_from_file(car_image)
            upload_end = time.time()

            print(f"Time taken for upload: {upload_end - upload_start} seconds")

            # Tornar o objeto público
            blob.make_public()

            # Obter a URL pública da imagem
            url_imagem = blob.public_url

            # Salvar apenas a URL da imagem no banco de dados
            # Implemente a lógica para salvar no banco de dados MySQL aqui
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify(cursor), 500
            
            # Atrelando o novo carro ao proprietário, através do username
            id_usuario = Usuario.get_user_id(username)  # Isso retorna o id do usuário que está logado
            db_start = time.time()
            # Inserindo o carro no estoque, e ainda inserindo qual é o seu proprietário
            cursor.execute('INSERT INTO carros (marca, modelo, ano, quilometragem, preco, usuario_id, car_image_path) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                       (marca, modelo, ano, quilometragem, preco, id_usuario, url_imagem))
            conexao_db.commit()
            conexao_db.close()
            db_end = time.time()

            print(f"Time taken for DB operations: {db_end - db_start} seconds")

            end_time = time.time()
            print(f"Total time taken: {end_time - start_time} seconds")

            return jsonify({'message': 'Carro cadastrado para venda!', 'url_imagem': url_imagem}), 201

        except Exception as e:
            return jsonify({'message': str(e)}), 500


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

        if 'comprador_username' in data and 'id_carro' in data and 'preco_proposto' in data:
            conexao_db, cursor = conectar_db()

            if conexao_db is None:
                return jsonify(cursor), 500

            try:
                id_usuario = Usuario.get_user_id(data['comprador_username'])  # Isso retorna o id do usuário que está logado

                cursor.execute('SELECT * FROM carros WHERE id = %s', (data['id_carro'],))
                carro = cursor.fetchone()

                if carro:
                    id_novo_antigo_dono = carro[7]

                    # Atualiza o proprietário do carro
                    cursor.execute('UPDATE carros SET usuario_id = %s, id_antigo_dono = %s WHERE id = %s', 
                                (id_usuario, id_novo_antigo_dono, data['id_carro']))

                    # Atualiza a data de compra
                    data_atual = datetime.datetime.now()
                    cursor.execute('UPDATE carros SET data_compra = %s WHERE id = %s', 
                                (data_atual, data['id_carro']))

                    # Atualiza o preço do carro
                    cursor.execute('UPDATE carros SET preco = %s WHERE id = %s', 
                                (data['preco_proposto'], data['id_carro']))

                    # Confirma a transação
                    conexao_db.commit()

                    # Emitindo que um novo carro foi vendido
                    socketio.emit('new_sold_car', {'carro_vendido': 'verdadeiro'})
                    print('vendido carro emitido')

                    return jsonify({'message': 'carro vendido com sucesso!'}), 200
                else:
                    return jsonify({'message': '[erro] carro não encontrado.'}), 404
            except Exception as e:
                conexao_db.rollback()
                print(f'Erro ao vender carro: {e}')
                return jsonify({'message': '[erro] Erro ao vender carro.'}), 500
            finally:
                cursor.close()
                conexao_db.close()
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
            

            
    # Amanhã muda essa rota p socket, pois conforme ocorram trnasações, atualiza a homePage la do frontend automáticamente
    @app.route('/lastestSoldCars', methods=['GET'])
    def handle_lastest_sold_cars():
        response = CarsService.search_latest_sold_cars()

        if response is None:
            return jsonify({'message': 'Erro ao buscar carros'}), 400
        else:
            return response
