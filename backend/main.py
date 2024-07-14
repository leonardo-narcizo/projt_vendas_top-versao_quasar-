from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from flask_socketio import SocketIO, emit
from datetime import datetime
from services.users import Usuario
from config.db_config import conectar_db

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'backend/googleCloudCredentials.json'

from api.charts_route import *
from api.proposals_route import *
from api.user_routes import *
from api.car_routes import *
from api.socket_routes import *
from api.news_routes import *

#### API config
app = Flask(__name__)
CORS(app)
app.json.sort_keys = False

### Config do socketIO
socketio = SocketIO(app, cors_allowed_origins="*")


### Importação rotas http
criar_rotas_graficos(app)
proposals_route(app)
user_routes(app)
news_routes(app)
car_routes(app, socketio)


### Importação rotas socket
socket_routes(socketio)

@socketio.on('connect')
def handle_connect():
    print('Conexão com o SocketIO detectada!')

@socketio.on('disconnect')
def handle_disconnect():
    print('Conexão sockeIO encerrada!')


if __name__ == '__main__':
    socketio.run(app, debug=True)

