from flask import url_for
from flask import redirect
from flask import current_app
from flask import session
from flask import jsonify

from supabase import Client as SupaBaseClient

from models.user_model import UserCreateModel

from utils.jwt_handler import generate_jwt_access_token
from utils.jwt_handler import generate_jwt_refresh_token
from utils.jwt_handler import generate_jwt_encode

class AuthService:
 
    def __init__(self, supabase_client: SupaBaseClient):

        self.supabase = supabase_client
        pass
 
    def auth_user_test( self, email:str ):
        check_user_in_db = self.supabase.from_(current_app.config['SUPABASE_TABLE_USER']).select('*').eq('email', email).execute(); 
        return check_user_in_db.data[0]

    def initiate_login(self, email, password):
 
        check_user_in_db = self.supabase.from_(current_app.config['SUPABASE_TABLE_USER']).select('*').eq('email', email).execute(); 

        if not check_user_in_db.data[0] :
            return redirect(
                url_for('auth.login_failed_route', error='User does not exist')
            )
        
        if not  check_user_in_db.data[0]['password'] == password:
            return redirect(
                url_for('auth.login_failed_route', error='Authentication Failed: Incorrect Password')
            )
        
        user_id = check_user_in_db.data[0]['id']
        user_avatar = check_user_in_db.data[0]['avatar_url']
        user_email = check_user_in_db.data[0]['email']      
        user_name = check_user_in_db.data[0]['name']      
        user_role = check_user_in_db.data[0]['role']      

        access_token = generate_jwt_access_token(user_id=user_id)
        refresh_token = generate_jwt_refresh_token(user_id=user_id)

        session['user'] = check_user_in_db.data[0]
        session['jwt_access_token'] = access_token
        session['jwt_refresh_token'] = refresh_token

        return {
            'user': {
                'user-id': user_id,
                'user-email': user_email,
                'user_name': user_name,
                'user_avatar': user_avatar,
                'user-role': user_role
            },
            'tokens': {
                'access-token': access_token,
                'refresh-token': refresh_token
            },      
        }


    def create_account(self, email, password): 
        check_user_in_db = self.supabase.from_(current_app.config['SUPABASE_TABLE_USER']).select('*').eq('email', email).execute(); 

        if check_user_in_db.data :
            return redirect(
                url_for('auth.login_failed_route', error='User exists')
            )
        
        new_user = UserCreateModel(
            email=email,
            password=password,
            role='user'
        )
        
        create_user_response = self.supabase.from_(current_app.config['SUPABASE_TABLE_USER']).insert(new_user.model_dump(mode='json')).execute()

        if not create_user_response: 
            return redirect(
                url_for('auth.signup_failed_route', error='Sign Up Failed Somehow')
            )
        
        return redirect(
            url_for('auth.signup_success_route')
        )
