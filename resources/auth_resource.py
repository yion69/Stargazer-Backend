from flask import request
from flask import jsonify
from flask import Blueprint
from flask import session
from flask import current_app
from flask import request

from flask_restful import Api
from flask_restful import Resource

from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

class AuthLoginResource(Resource):

    def __init__(self):
        super().__init__()
        self.AuthService = AuthService(current_app.supabase)
        pass

    def get(self):
        req = self.authService.auth_user_test(email='thutanaing55@gmail.com')
        return jsonify(req)
    
    def post(self):
        try: 
            if not request.is_json:
                return {
                    'message': 'Request must be JSON',
                    'error': 'Content-Type must be application/json',
                } , 400
 
            data = request.get_json()

            email = data.get('email')
            password = data.get('password')

            response = self.AuthService.initiate_login(email=email, password=password);

            return {
                'message': 'Authentication Successful',
                'body': response
            }, 200
        
        except Exception as err:
            return {
                'message': 'Error Occured',
                'error': str(err)
            }
        
class AuthSignUpResource(Resource):
    def get(self):
        authService = AuthService(current_app.supabase)
        create_account_response = authService.create_account('abcd@gmail.com', 'abcd')
        return create_account_response

api.add_resource(AuthLoginResource, '/login')
api.add_resource(AuthSignUpResource, '/signup')

@auth_bp.route('/login-failed')
def login_failed_route():
    
    return jsonify({
        
        'message': 'Auth failed please try again'
        
    }), 401

def login_success_route():

    response_data = session['user']
     
@auth_bp.route('/signup-success')
def signup_success_route():
     
     return jsonify({
        'message': 'Sign Up Successful'
    }), 202

@auth_bp.route('/signup-failed')
def signup_failed_route():
     
     error_message = request.args.get('error')
     return jsonify({
        'message': error_message
    }), 406