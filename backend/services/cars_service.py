from db.db_config import conectar_db
from services.users import Usuario
from flask import jsonify
import datetime
from services.date_service import formatar_data_brasileira


class CarsService:

    @staticmethod
    def search_latest_sold_cars():

        conexao_db, cursor = conectar_db()

        if conexao_db is None:
            return jsonify(cursor), 500

        try:
            cursor.execute('''
                           SELECT *
                           FROM carros
                           WHERE usuario_id IS NOT NULL AND id_antigo_dono IS NOT NULL
                           ORDER BY data_compra DESC
                           LIMIT 3
                           ''')
            
            rows = cursor.fetchall()

            lastest_sold_cars = []

            if not rows:
                return None

            for row in rows:
                lastest_sold_cars.append({
                    'marca': row[1],
                    'modelo': row[2],
                    'ano': row[3],
                    'quilometragem': row[4],
                    'vendido por': row[5],
                    'Novo Proprietário': Usuario.get_username_by_id(row[7]),
                    'Proprietário anterior': Usuario.get_username_by_id(row[8]),
                    'car_image_path': row[9]
                })
            cursor.close()

            return jsonify({'lastest_sold_cars': lastest_sold_cars}), 200

            
        except Exception as e:
            return jsonify({'message': 'Erro interno do servidor', 'error': str(e)}), 500

