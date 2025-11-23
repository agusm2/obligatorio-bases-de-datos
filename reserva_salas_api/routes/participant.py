from flask import Blueprint, request, jsonify
from services import participant as participant_service
from utils.validation import validar_email
import mysql.connector

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
        if obj is None:
            return jsonify({'error': 'El participante ya existe'}), 409
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


@participant_bp.route('/<string:ci>/sancion', methods=['POST'])
def add_sancion(ci):
    """Endpoint para que un admin agregue una sanción manual a un participante.

    Body JSON esperado:
    {
      "fecha_fin": "YYYY-MM-DD",
      "fecha_inicio": "YYYY-MM-DD" (opcional) o "YYYY-MM-DD HH:MM:SS"
    }
    """
    data = request.get_json() or {}
    fecha_fin = data.get('fecha_fin')
    fecha_inicio = data.get('fecha_inicio')
    if not fecha_fin:
        return jsonify({'error': 'fecha_fin es obligatoria (YYYY-MM-DD)'}), 400
    try:
        res = participant_service.add_sancion({'ci': ci}, fecha_fin, fecha_inicio)
        if res is None:
            return jsonify({'error': 'Participante no encontrado'}), 404
        return jsonify(res), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except mysql.connector.IntegrityError as ie:
        # por ejemplo cuando la PK ya existe
        return jsonify({'error': str(ie)}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@participant_bp.route('/sanciones', methods=['GET'])
def get_sanciones():
    """Devuelve todas las sanciones. Soporta query params `limit` y `offset`."""
    try:
        # leer paginación opcional
        limit = request.args.get('limit', None)
        offset = request.args.get('offset', None)
        try:
            limit = int(limit) if limit is not None else 100
        except Exception:
            return jsonify({'error': 'limit debe ser un entero'}), 400
        try:
            offset = int(offset) if offset is not None else 0
        except Exception:
            return jsonify({'error': 'offset debe ser un entero'}), 400

        items = participant_service.get_sanciones(limit=limit, offset=offset)
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400