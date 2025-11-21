from flask import Blueprint, request, jsonify
from services import user as user_service


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    try:
        user = user_service.authenticate(data)
        if user is None:
            return jsonify({'error': 'Credenciales inválidas'}), 401
        return jsonify({'user': user}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400