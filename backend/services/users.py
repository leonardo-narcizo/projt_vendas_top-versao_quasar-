from db.db_config import conectar_db
from flask import jsonify
import jwt
import bcrypt
import datetime

SECRET_KEY = 'vendastop2024!'



# Defindo a classe de usuário
class Usuario:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Método de autênticação
    def autenticar(self):
        # Conectar ao banco
        conexao_db, cursor = conectar_db()

        # Verificando se o usuário existe no banco
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (self.username,))
        user = cursor.fetchone()
        user_type = user[3]
        cursor.close()

        if user:
            stored_password = user[2]

            # Comparando senha enviada na request c/ senha aarmazena no banco
            if bcrypt.checkpw(self.password.encode('utf-8'), stored_password.encode('utf-8')):
                # Gerando token JWT para enviar ao client
                token = jwt.encode({'username': self.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SECRET_KEY)

                return jsonify({'token': token, 'user_type': user_type, 'message': 'Autenticação bem-sucedida!'})
            else:
                return jsonify({'message': 'Senha incorreta!'})
        else:
            return jsonify({'message': 'Usuário não encotrado!'})
        
    @staticmethod
    def verificar_token(token):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return data['username']
        except:
            return None
        
    @staticmethod   
    def get_user_id(username):
        conexao_db, cursor = conectar_db()

        # Pegando o id do usuário
        cursor.execute('SELECT id FROM usuarios WHERE username = %s', (username,))
        user_id = cursor.fetchone()
        cursor.close()

        if user_id:
            return user_id[0] # Retorna apenas o valor absoluto do ID
        else:
            return 'Usuário não encontrado!'
        
    @staticmethod # Método que da para acessar mesmo sem ser instância da classe
    def criar_usuario(username, password, cnpj=None):
        # Conectar novamente ao banco
        conexao_db, cursor = conectar_db()

        if cnpj:
            user_type = 'empresa'
        else:
            user_type = 'fisica'        

        # Gerar hash antes de armazenar senha
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Inserir novo usuário dentro do banco
        cursor.execute('INSERT INTO usuarios (username, password, user_type, cnpj) VALUES (%s, %s, %s, %s)', (username, hashed_password, user_type, cnpj))
        conexao_db.commit()
        cursor.close()

        return jsonify({'message': 'Usuário criado com sucesso!'})
    

    @staticmethod
    def get_username_by_id(id_usuario):
        conexao_db, cursor = conectar_db()

        # Pegando o username do usuário pelo seu id
        cursor.execute('SELECT username FROM usuarios WHERE id = %s', (id_usuario,))
        usuario_username = cursor.fetchone()
        cursor.close()

        if usuario_username:
            return usuario_username[0]
        else:
            return None

        
