from flask import Blueprint, jsonify
from services import dashboard as dashboard_service

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/most_reserved_rooms', methods=['GET'])
def most_reserved_rooms():
    try:
        data = dashboard_service.most_reserved_rooms()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/most_demanded_turns', methods=['GET'])
def most_demanded_turns():
    try:
        data = dashboard_service.most_demanded_turns()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/avg_participants_per_room', methods=['GET'])
def avg_participants_per_room():
    try:
        data = dashboard_service.avg_participants_per_room()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/reservations_by_program_and_faculty', methods=['GET'])
def reservations_by_program_and_faculty():
    try:
        data = dashboard_service.reservations_by_program_and_faculty()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/occupation_percentage_by_building', methods=['GET'])
def occupation_percentage_by_building():
    try:
        data = dashboard_service.occupation_percentage_by_building()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/reservations_and_attendance_by_role_and_type', methods=['GET'])
def reservations_and_attendance_by_role_and_type():
    try:
        data = dashboard_service.reservations_and_attendance_by_role_and_type()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/sanctions_by_role_and_type', methods=['GET'])
def sanctions_by_role_and_type():
    try:
        data = dashboard_service.sanctions_by_role_and_type()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/usage_vs_cancelled', methods=['GET'])
def usage_vs_cancelled():
    try:
        data = dashboard_service.usage_vs_cancelled()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# consultas sugeridas
@dashboard_bp.route('/participants_with_multiple_sanctions', methods=['GET'])
def participants_with_multiple_sanctions():
    try:
        data = dashboard_service.participants_with_multiple_sanctions()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/users_most_no_show_or_cancel', methods=['GET'])
def users_most_no_show_or_cancel():
    try:
        data = dashboard_service.users_most_no_show_or_cancel()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@dashboard_bp.route('/least_used_rooms', methods=['GET'])
def least_used_rooms():
    try:
        data = dashboard_service.least_used_rooms()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
