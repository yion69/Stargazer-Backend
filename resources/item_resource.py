from flask import Blueprint, jsonify, current_app, request
from flask_restful import Api, Resource
from services.item_service import ItemService

item_bp = Blueprint('items', __name__)
api = Api(item_bp)

class ItemResource(Resource):
    def get(self):
        try:
            items = ItemService.get_all_item()
            return jsonify(items)
        except Exception as err:
            current_app.logger.error(f"Error Occured : ErrorCode {err}")
            raise
    
    def post(self):
        try:
            if not request.is_json:
                current_app.logger.warning("Attempted POST without JSON content type.")
                return {"message": "Request must be JSON", "error": "Content-Type must be application/json"}, 400
            
            data = request.get_json()

            image_1 = data.get('image_1')
            image_2 = data.get('image_2')
            name = data.get('heading')
            brand = data.get('subheading')
            price = data.get('price')

            item = ItemService.create_item(
                name,
                price, 
                brand, 
                4.69, 
                69, 
                [   
                    image_1, 
                    image_2
                ]
            )
            return jsonify(item)
        except Exception as err:
            current_app.logger.error(f"Error Occured : ErrorCode {err}")
            return {"message": "idk man", "error": str(err)}, 400

class ItemSingleResource(Resource): 
    def get(self, item_id):
        try:
            item = ItemService.get_single_item(item_id);
            return jsonify(item)
        except Exception as err:
            current_app.logger.error(f"Error Occured : ErrorCode {err}")
            return {"message": "idk man", "error": str(err)}, 400

    def delete(self, item_id):
        try:
            item = ItemService.delete_item(item_id)
            return jsonify(item)
        except Exception as err:
            current_app.logger.error(f'Error Occured : ErrorCode {err}')
            raise

api.add_resource(ItemResource, '/items')
api.add_resource(ItemSingleResource, '/items/<string:item_id>')