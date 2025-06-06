from flask import Flask
from config import Config
from supabase import create_client, Client

from dotenv import load_dotenv

load_dotenv()

supabase_client: Client = None 

try:

    supabase_url = Config.SUPABASE_URL
    supabase_key = Config.SUPABASE_KEY

    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL or Key not found in configuration. Check .env and config.py")

    supabase_client = create_client(supabase_url, supabase_key)
    print("Supabase client initialized globally.") 

except Exception as e:
    print(f"Failed to initialize Supabase client globally: {e}")
    supabase_client = None
    raise 

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    app.logger.info(f"Supabase client initialzed with URL ==> {Config.SUPABASE_URL}")

    from resources.item_resource import item_bp

    app.register_blueprint(item_bp, url_prefix='/api')

    @app.route('/')
    def HelloWorld():
        return ("<h1>This still works</h1>")

    return app

if __name__ == '__main__':

    app = create_app()
    app.run(debug=True)
