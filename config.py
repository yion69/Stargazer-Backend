import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Config: 

    FRONTEND_URL=os.environ.get('FRONTEND_URL')
    SUPABASE_URL=os.environ.get('SUPABASE_URL')
    SUPABASE_KEY=os.environ.get('SUPABASE_KEY')

    SECRET_KEY=os.environ.get('SECRET_KEY') or "3f1fc6169b9d6c7d1773fcc44d4d799679fc51bb11a9af43"
    GOOGLE_CLIENT_ID=os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET=os.environ.get('GOOGLE_CLIENT_SECRET')

    SUPABASE_TABLE_ITEM=os.environ.get('SUPABASE_TABLE_ITEM')
    SUPABASE_TABLE_USER=os.environ.get('SUPABASE_TABLE_USER')

    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM='HS256'