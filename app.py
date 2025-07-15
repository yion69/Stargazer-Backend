from flask import Flask
from config import Config
from supabase import create_client, Client
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token

load_dotenv()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)

    app.logger.info(f"Supabase client initialzed with URL ==> {Config.SUPABASE_URL}")

    jwt = JWTManager(app);

    oauth = OAuth(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'},
        jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    )

    supabase_url = app.config['SUPABASE_URL']
    supabase_key = app.config['SUPABASE_KEY']

    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL or Key not found in configuration. Check .env and config.py")
    
    supabase_client = create_client(supabase_url, supabase_key)

    # Important App Instances
    app.oauth = oauth
    app.supabase = supabase_client
    app.jwt = jwt
    
    # Services Initializationj
    from services.auth_service import AuthService
    app.auth_service = AuthService(supabase_client=app.supabase)
    
    from services.google_auth_service import GoogleAuthService
    app.google_auth_service = GoogleAuthService(oauth_client=app.oauth, supabase_client=app.supabase)

    # Resources Blueprint
    from resources.google_auth_resource import google_auth_bp
    from resources.item_resource import item_bp
    from resources.auth_resource import auth_bp

    # Blueprint Registration
    app.register_blueprint(item_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(google_auth_bp, url_prefix='/google_auth')

    # Don't user these routes
    @app.route('/')
    def HelloWorld():
        return ("<h1>This still works</h1>")

    return app

if __name__ == '__main__':

    app = create_app()
    app.run(debug=True)
