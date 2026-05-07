from jose import jwt, JWTError, ExpiredSignatureError
import requests
import os
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")


def get_supabase_public_key():
    if not supabase_url:
        raise ValueError("SUPABASE_URL environment variable is not set")
    jwks_url = f"{supabase_url}/auth/v1/.well-known/jwks.json"
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()

def require_auth (f):
    @wraps(f)
    def decorated (*args, **kwargs):
        auth_header = request.headers.get('Authorization');
        if not auth_header or not auth_header.startswith ('Bearer '):
            return jsonify ({'error': 'Authorization header missing or invalid'}), 401
        token = auth_header.split(' ')[1]
        try:
            jwks = get_supabase_public_key()
            decoded = jwt.decode(
                token,
                jwks,
                algorithms=['RS256', 'ES256'],
                audience='authenticated',
                issuer=f"{supabase_url}/auth/v1"
            )
            request.user_id = decoded.get('sub')
        except ExpiredSignatureError:
            return jsonify ({'error': 'Token has expired'}), 401
        except JWTError:
            return jsonify ({'error':'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated
    

