from models.reservation import Reservation
from models.classroom import Classroom
from models.participant import Participant
import mysql.connector


def get_all(limit=100, offset=0):
    items = Reservation.list_all(limit=limit, offset=offset)
    return [r.to_dict() for r in items]


def get_by_id(id_reserva):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    d = obj.to_dict()
    d['participants'] = obj.list_participants()
    return d


def create(data):
    # data expects: nombre_sala, edificio, fecha (YYYY-MM-DD), id_turno
    nombre_sala = data.get('classroom_name')
    edificio = data.get('building')
    fecha = data.get('date')
    id_turno = data.get('id_turn')

    # Basic validation: classroom exists
    classroom = Classroom.get_by_pk(nombre_sala, edificio)
    if not classroom:
        raise ValueError('Classroom does not exist')

    # aceptar lista opcional de participantes (cedulas) en el payload: data['participants']
    participants = data.get('participants')

    obj = Reservation.create(nombre_sala=nombre_sala, edificio=edificio, fecha=fecha, id_turno=id_turno, participants=participants)
    return obj.to_dict()


def update(id_reserva, data):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    obj.update(
        nombre_sala=data.get('nombre_sala'),
        edificio=data.get('edificio'),
        fecha=data.get('fecha'),
        id_turno=data.get('id_turno'),
        estado=data.get('estado'),
        participants=data.get('participants')
    )
    return obj.to_dict()


def delete(id_reserva):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    obj.delete()
    return {'message': 'Deleted'}


def add_participant(id_reserva, ci):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    # check participant exists
    p = Participant.get_by_pk(ci)
    if not p:
        raise ValueError('Participant does not exist')

    # check capacity
    classroom = Classroom.get_by_pk(obj.nombre_sala, obj.edificio)
    if classroom and classroom.capacity is not None:
        parts = obj.list_participants()
        if len(parts) >= classroom.capacity:
            raise ValueError('Capacity exceeded')

    try:
        obj.add_participant(ci_participante=ci)
    except mysql.connector.IntegrityError:
        return None
    return {'message': 'Participant added'}


def remove_participant(id_reserva, ci):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    obj.remove_participant(ci)
    return {'message': 'Participant removed'}


def list_participants(id_reserva):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    return obj.list_participants()

def update_asistencia(id_reserva, ci_participante, asistencia):
    return Reservation.update_asistencia(id_reserva, ci_participante, asistencia)