import secrets
from datetime import datetime, timezone
from supabase import Client as SupabaseClient
from authlib.integrations.flask_client import OAuth
from flask import url_for, session, redirect, current_app
from models.user_model import UserCreateModel, UserFullModel, UserUpdateModel


class GoogleAuthService:
    
    def __init__(self, oauth_client: OAuth, supabase_client: SupabaseClient):
        
        self.oauth = oauth_client
        self.supabase_client = supabase_client
        self.google_oauth_client = self.oauth.google
        pass

    def initiate_google_login(self):
        redirect_uri = url_for('google_auth.googleauthcallbackresource', _external=True)
        nonce = secrets.token_urlsafe(32)
        session['oauth_nonce'] = nonce
        return self.google_oauth_client.authorize_redirect(redirect_uri, nonce=nonce)
    
    def google_oauth_callback(self):
        try:
            token = self.google_oauth_client.authorize_access_token()
            expected_nonce = session.pop('oauth_nonce', None)
            if not expected_nonce:
                current_app.logger.error("Error: OAuth nonce not found in session or already used.")
                return redirect(url_for('google_auth.login_failed_route'))
            user_google_info = self.google_oauth_client.parse_id_token(token, nonce=expected_nonce)

            user_email = user_google_info.get('email')
            user_google_id = user_google_info.get('sub')
            user_name = user_google_info.get('name')
            user_avatar = user_google_info.get('picture')
            current_app.logger.info(f"{user_email}")

            if not user_email or not user_google_id:
                current_app.logger.error("Error user email or user google id not found")
                return redirect(url_for('google_auth.login_failed_route'))

            #Created the variable here to use in if else blocks that add or update user
            user_in_database = None

            try:
                response = self.supabase_client.from_(current_app.config['SUPABASE_TABLE_USER']).select('*').eq('google_id',
                user_google_id).execute()
                user_data = response.data[0] if response.data else None

                if not user_data and user_email:
                    response = self.supabase_client.from_(current_app.config['SUPABASE_TABLE_USER']).select('*').eq('email', user_email).execute()
                    user_data = response.data[0] if response.data else None

                if not user_data:
                    new_user_data = UserCreateModel(
                        email=user_email,
                        name=user_name,
                        google_id=user_google_id,
                        avatar_url=user_avatar,
                        role='user',
                        
                    )
                    user_create_response = self.supabase_client.from_(current_app.config['SUPABASE_TABLE_USER']).insert(new_user_data.model_dump(mode='json')).execute()
                    user_in_database = UserFullModel.model_validate(user_create_response.data[0])
                    current_app.logger.info(f'New user created in the database: {user_in_database.email}')

                else: 
                    update_user_data = UserUpdateModel(
                        email=user_email,
                        name=user_name,
                        google_id=user_google_id,
                        avatar_url=user_avatar,
                        last_login=datetime.now(timezone.utc)
                    )
                    user_update_response = self.supabase_client.from_(current_app.config['SUPABASE_TABLE_USER']).update(update_user_data.model_dump(mode='json')).eq('id',user_data['id']).execute()
                    user_in_database = UserFullModel.model_validate(user_update_response.data[0])
                    current_app.logger.info(f'Updated user info from the database: {user_in_database.email}')

            except Exception as err:
                current_app.logger.error(f'Error occured during account creation or update ==> {err}')
                return redirect(url_for('google_auth.login_failed_route'))

            session['user'] = user_in_database.model_dump()
            return redirect(url_for('google_auth.login_success_route'))

        except Exception as err:
            current_app.logger.error(f'Unexpected error occured during oauth callback ==> {err}')
            return redirect(url_for('google_auth.login_failed_route'))
    