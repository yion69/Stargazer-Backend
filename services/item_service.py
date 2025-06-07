from flask import current_app
from http import HTTPStatus
from flask import current_app
from postgrest.exceptions import APIError
from utils.exceptions import NotFoundError
from models.item_model import ItemModelFull

class ItemService:
    
    @staticmethod
    def create_item( name, price, brand, rating, sold, images ):
        try: 
            data = {
                'item_name': name,
                'item_price': price,
                'item_brand': brand,
                'item_rating': rating,
                'item_sold': sold,
                'item_images': images,
            }
            response = current_app.supabase.table('clothing_item').insert(data).execute()
            if response.data:
                return ItemModelFull(**response.data[0]).model_dump()
        except Exception as err:
            print(f'Error Occured : ErrorCode {err}')
            raise RuntimeError("Unexpected error occured during item creation --> create_item()")
        except APIError as err:
            print(f'Error Occured : ErrorCode {err}')
            raise RuntimeError("Progrest Api error occured during item creation --> create_item()")
            
    @staticmethod
    def get_all_item():
        try:           
            response = current_app.supabase.table('clothing_item').select('*').execute()
            if not response.data:
                raise APIError
            validated_items = [ItemModelFull(**item).model_dump() for item in response.data]
            return validated_items   
        except Exception as err:
            print(f'Error Occured : ErrorCode {err}')
            raise RuntimeError("Unexpected error occured during item creation --> create_item()")
        except APIError as err:
            if err.code == HTTPStatus.NOT_ACCEPTABLE:
                print(f'Error Occured : ErrorCode {err}')
                raise RuntimeError("Unexcepted error occured during item creation --> get_single_item()")
            else:
                print(f'Error Occured : ErrorCode {err}')
                raise RuntimeError("Progrest Api error occured during item creation --> create_item()")
    
    @staticmethod
    def get_single_item(item_id: str):
        try:        
            response = current_app.supabase.table('clothing_item').select('*').eq('item_id', item_id).single().execute()

            if response.data:
                return ItemModelFull(**response.data).model_dump()

        except Exception as err: 
            print(f'Error Occured : ErrorCode {err}')
            raise RuntimeError("Unexcepted error occured during item creation --> get_single_item()")
        except APIError as err:
            if err.status_code == HTTPStatus.NOT_ACCEPTABLE:
                raise NotFoundError(f"Resource not found: Item with id:{item_id} not_found")
            else:
                current_app.logger.error(f"Supabase API error fetching item {item_id} (Status: {err.status_code}):{err.message}")
                raise APIError(f"Supabase API error: {err.message}", status_code=err.status_code)
            
    @staticmethod
    def delete_item(item_id: str):
        try: 
            response = current_app.supabase.table('clothing_item').delete().eq('item_id', item_id).execute()
            return response.data
        except Exception as err: 
            print(f'Error Occured : ErrorCode {err}')
            raise RuntimeError("Unexcepted error occured during item deletion --> delete_item()")
        except APIError as err:
            if err.status_code == HTTPStatus.NOT_ACCEPTABLE:
                raise NotFoundError(f"Resource not found: Item with id:{item_id} not_found")
            else:
                current_app.logger.error(f"Supabase API error fetching item {item_id} (Status: {err.status_code}):{err.message}")
                raise APIError(f"Supabase API error: {err.message}", status_code=err.status_code)

                