from jwt import encode
from jwt import decode
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

from flask import current_app

from typing import Optional

from utils.exceptions import JwtError
from utils.exceptions import JwtExpiredError
from utils.exceptions import JwtInvalidTokenError

import datetime

def generate_jwt_access_token( user_id:str ) -> str:
    
    # payload = {
    #     'user_id': user_id,
    #     'role': user_role,
    #     'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    # }

    # token = encode( payload, current_app.config['JWT_SECRET_KEY'], algorithm=['HS256'])
    access_token = create_access_token(
        identity=user_id,
        expires_delta=datetime.timedelta(hours=1),

    )
    return access_token

def generate_jwt_refresh_token( user_id:str ):
    refresh_token = create_refresh_token(
        identity=user_id,
        expires_delta=datetime.timedelta(days=7)
    )
    return refresh_token

def generate_jwt_encode(payload):

    encoded_payload = encode( payload, current_app.config['JWT_SECRET_KEY'], algorithm=['HS256'])
    return encoded_payload

def decode_jwt_token( token:str ): 
    try:
 
        decoded = decode( token, key=current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return decoded

    except ExpiredSignatureError:
        raise JwtExpiredError()
    
    except InvalidTokenError:
        raise JwtInvalidTokenError()
    
    except Exception:
        raise JwtError()