from flask import Blueprint, jsonify

# Definimos el blueprint
salas_bp = Blueprint('salas', __name__, url_prefix='/salas')

# Endpoint de prueba
@salas_bp.route('/', methods=['GET'])
def listar_salas():
    return jsonify({"message": "Endpoint /salas funcionando"})
