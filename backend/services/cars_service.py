from db.db_config import conectar_db
from services.users import Usuario
from flask import jsonify
import datetime
from services.date_service import formatar_data_brasileira


class CarsService:

    @staticmethod
    def search_latest_cars_sold():

        conexao_db, cursor = conectar_db()

        if conexao_db is None:
            return jsonify(cursor), 500

        try:
            cursor.execute(''''
                           SELECT *
                           FROM carros
                           ORDER BY id DESC
                           LIMIT 3
                           ''')
            
        except Exception as e:
            return jsonify({'message': 'Erro interno do servidor'}), 500

