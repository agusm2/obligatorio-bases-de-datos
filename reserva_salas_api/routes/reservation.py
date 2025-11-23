from flask import Blueprint, request, jsonify
from services import reservation as reservation_service

reservations_bp = Blueprint("reservation", __name__, url_prefix="/reservation")


@reservations_bp.route("/", methods=["GET"])
def get_all():
    try:
        items = reservation_service.get_all()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route("/<int:id_reserva>", methods=["GET"])
def get_one(id_reserva):
    try:
        obj = reservation_service.get_by_id(id_reserva)
        if obj is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(obj), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    try:
        obj = reservation_service.create(data)
        return jsonify(obj), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route("/<int:id_reserva>", methods=["PUT"])
def update(id_reserva):
    data = request.get_json()
    try:
        result = reservation_service.update(id_reserva, data)
        if result is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route("/<int:id_reserva>", methods=["DELETE"])
def delete(id_reserva):
    try:
        result = reservation_service.delete(id_reserva)
        if result is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route("/<int:id_reserva>/participants", methods=["POST"])
def add_participant(id_reserva):
    data = request.get_json()
    ci = data.get("ci")
    if not ci:
        return jsonify({"error": "ci is required"}), 400
    try:
        res = reservation_service.add_participant(id_reserva, ci)
        if res is None:
            return (
                jsonify({"error": "Could not add (already exists or FK invalid)"}),
                409,
            )
        return jsonify(res), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route("/<int:id_reserva>/participants/<string:ci>", methods=["DELETE"])
def remove_participant(id_reserva, ci):
    try:
        res = reservation_service.remove_participant(id_reserva, ci)
        if res is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route("/<int:id_reserva>/participants", methods=["GET"])
def list_participants(id_reserva):
    try:
        res = reservation_service.list_participants(id_reserva)
        if res is None:
            return jsonify({"error": "Not found"}), 404
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route(
    "/<int:id_reserva>/participants/<string:ci>/asistencia", methods=["PUT"]
)
def update_asistencia(id_reserva, ci):
    data = request.get_json()
    asistencia = data.get("asistencia")

    # Normalizar a bool
    if isinstance(asistencia, str):
        asistencia = asistencia.lower() in ("1", "true", "t", "yes", "si")

    try:
        res = reservation_service.update_asistencia(id_reserva, ci, asistencia)
        if res is None:
            return jsonify({"error": "Reserva o participante no encontrado"}), 404
        return jsonify({"message": "Asistencia actualizada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@reservations_bp.route("participant/<string:ci>", methods=["GET"])
def get_reservas_by_participant(ci):
    try:
        data = reservation_service.get_by_participant(ci)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
