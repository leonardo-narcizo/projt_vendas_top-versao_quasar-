from config.db_config import conectar_db
from services.cars_service import CarsService
from flask import jsonify, request
from config.auth import token_required

def news_routes(app):
    @app.route('/lastestSoldCars', methods=['GET'])
    @token_required
    def handle_lastest_sold_cars(username):
        response = CarsService.search_latest_sold_cars()

        if response is None:
            return jsonify({'message': 'Erro ao buscar carros'}), 400
        else:
            return response
        