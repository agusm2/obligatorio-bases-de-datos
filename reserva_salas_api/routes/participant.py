from flask import Blueprint, request, jsonify
from services import participant as participant_service
from utils.validation import validar_email

# Definimos el blueprint para las rutas de participant
participant_bp = Blueprint('participant', __name__, url_prefix='/participant')

@participant_bp.route('/', methods=['GET'])
def get_all():
    try:
        items = participant_service.get_all()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@participant_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    if validar_email(data.get('email')) is False:
        return jsonify({'error': 'Email inválido'}), 400
    try:
        obj = participant_service.create(data)
        return jsonify(obj), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@participant_bp.route('/<string:ci>', methods=['PUT'])
def update(ci):
    data = request.get_json()
    if validar_email(data.get('email')) is False:
        return jsonify({'error': 'Email inválido'}), 400
    try:
        result = participant_service.update({'ci': ci}, data)
        if result is None:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@participant_bp.route('/<string:ci>', methods=['DELETE'])
def delete(ci):
    try:
        result = participant_service.delete({'ci': ci})
        if result is None:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400