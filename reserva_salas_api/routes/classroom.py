from flask import Blueprint, request, jsonify
from services import classroom as classroom_service

# Definimos el blueprint para las rutas de classroom
classroom_bp = Blueprint('classroom', __name__, url_prefix='/classroom')

@classroom_bp.route('/', methods=['GET'])
def get_all():
    try:
        items = classroom_service.get_all()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@classroom_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    try:
        result = classroom_service.create(data)
        if result is None:
            return jsonify({'error': 'El aula ya existe'}), 409
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@classroom_bp.route('/<string:name>/<string:building>', methods=['PUT'])
def update(name, building):
    data = request.get_json()
    try:
        result = classroom_service.update({'name': name, 'building': building}, data)
        if result is None:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@classroom_bp.route('/<string:name>/<string:building>', methods=['DELETE'])
def delete(name, building):
    try:
        result = classroom_service.delete({'name': name, 'building': building})
        if result is None:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400