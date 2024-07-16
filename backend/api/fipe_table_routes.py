from flask import Flask, jsonify, request
from services.fipe_table_service import Fipe_table_service

def fipe_table_routes(app):
    ### Rota para buscar as marcas disponíveis da fipe
    @app.route('/searchFipeBrands', methods=['GET'])
    def handle_search_fipe_brands():
        response = Fipe_table_service.search_brands()

        if response is None:
            return jsonify({'message': 'Erro ao buscar marcas!!'}), 500
        else:
            return jsonify({'brands_list': response}), 200
        

    @app.route('/searchFipeModels/<int:brand_id>', methods=['GET'])
    def handle_search_file_models(brand_id):
        if brand_id:
            
            response = Fipe_table_service.search_models_by_brand(brand_id)

            if response is None:
                return jsonify({'message': 'Erro ao buscar modelos!'}), 500
            else:
                return jsonify({'models_list': response}), 200
            
        else:
            return jsonify({'message': 'O id da marca não foi passado corretamente!'}), 401