import requests


# Url base da API da tabela fipe
base_url = 'https://parallelum.com.br/fipe/api/v1/carros'

class Fipe_table_service:

    @staticmethod
    def search_brands():
        try:
            response = requests.get(f'{base_url}/marcas')
            response.raise_for_status()
            brands = response.json()
            print(f'marcas encontradas: {brands}')

            brands_list = []

            for brand in brands:
                brands_list.append({'brand_id': brand['codigo'], 'brand_name': brand['nome']})

            return brands_list
        
        except requests.exceptions.RequestException as e:
            print(f'Erro ao consultar marcas: {e}')
            return None
        

    @staticmethod
    def search_models_by_brand(brand_id):
        try:
            response = requests.get(f'{base_url}/marcas/{brand_id}/modelos')
            response.raise_for_status()
            data = response.json()
            models = data['modelos']

            models_list = []

            for model in models:
                models_list.append({'model_id': model['codigo'], 'model_name': model['nome']})

            return models_list

        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar modelos: {e}")
            return None
