import jwt
from flask import request, jsonify
from functools import wraps

SECRET_KEY = 'vendastop2024!'

def verificar_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data['username']
    except:
        return None

# Middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Assumindo q o token vem c bearer + valor do token
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token é necessario!'}), 401

        try:
            username = verificar_token(token)
            if username is None:
                return jsonify({'message': 'Token inválido'}), 401
        except Exception as e:
            return jsonify({'message': 'Erro interno do servidor!', 'error': str(e)}), 500

        return f(username, *args, **kwargs)

    return decorated
