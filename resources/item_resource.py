from flask import Blueprint, jsonify, current_app
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
            item = ItemService.create_item('johndoe', 2002, 'johneldenring', 69.9, 69, {})
            return jsonify(item)
        except Exception as err:
            current_app.logger.error(f"Error Occured : ErrorCode {err}")
            raise

class ItemSingleResource(Resource): 
    def get(self, item_id):
        try:
            item = ItemService.get_single_item(item_id)
            return jsonify(item)
        except Exception as err:
            current_app.logger.error(f'Error Occured : ErrorCode {err}')
            raise

    def delete(self, item_id):
        try:
            item = ItemService.delete_item(item_id)
            return jsonify(item)
        except Exception as err:
            current_app.logger.error(f'Error Occured : ErrorCode {err}')
            raise

api.add_resource(ItemResource, '/items')
api.add_resource(ItemSingleResource, '/items/<string:item_id>')