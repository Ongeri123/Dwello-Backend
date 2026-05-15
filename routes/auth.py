from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
auth_bp = Blueprint("auth_bp", __name__)

supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(supabase_url, supabase_service_key)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    role = data.get('role')

    if not all([email, password, name, role]):
        return jsonify({'error': 'Missing required fields'}), 400
    if not role in ['landlord', 'tenant']:
        return jsonify({'error': 'Invalid role'}), 400
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name,
                    "phone": phone,
                    "role": role,
                }
            }
        })
        user_id = response.user.id
        supabase.table('users').insert({
            'id': user_id,
            'name': name,
            'email': email,
            'phone': phone,
            'role': role
        }).execute()
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
     return jsonify({'error': 'Missing email or password'}), 400  
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        access_token = response.session.access_token
        refresh_token = response.session.refresh_token
        user_id = response.user.id
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
            "role": response.user.user_metadata.get('role'),
            "email": response.user.user_metadata.get('email'),
            "name": response.user.user_metadata.get('name')
        }), 200  
    except Exception as e:
        return jsonify({'error': 'Wrong email or password'}), 401