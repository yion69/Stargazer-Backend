from typing import cast
from flask_restful import Resource, Api
from flask import Blueprint, jsonify, current_app, session
from services.google_auth_service import GoogleAuthService

google_auth_bp = Blueprint('google_auth', __name__)
api = Api(google_auth_bp)

class GoogleLoginResource(Resource):
    def get(self):
        try:
            google_auth_service = cast(GoogleAuthService, current_app.google_auth_service)
            google_redirect_response = google_auth_service.initiate_google_login()
            
            return google_redirect_response
        except Exception as err:
            current_app.logger.error(f'Error Occured : ErrorCode {err}')
            return {'message': 'Authentication initiation failed', 'error': str(err)}, 500

class GoogleAuthCallbackResource(Resource):
    def get(self):
        try:
            google_auth_service = cast(GoogleAuthService, current_app.google_auth_service)
            google_redirect_response = google_auth_service.google_oauth_callback()
            return google_redirect_response
        except Exception as err: 
            current_app.logger.error(f'Error Occured : ErrorCode {err}')
            return {'message': 'Authentication initiation failed', 'error': str(err)}, 500

api.add_resource(GoogleLoginResource, '/google_login')
api.add_resource(GoogleAuthCallbackResource, '/oauth_callback')

@google_auth_bp.route('/login-success')
def login_success_route():
    if 'user' in session:
        return jsonify(session['user']), 200
    else:
        return jsonify({
            'message': 'Not authenticated or session expired'
        }), 401

@google_auth_bp.route("/login-failed")
def login_failed_route():
    return jsonify({
        'message': 'Google login failed please try again'
    }), 400