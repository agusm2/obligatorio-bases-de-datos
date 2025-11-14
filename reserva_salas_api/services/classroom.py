from models.classroom import Classroom


def get_all(limit=100, offset=0):
    """Devuelve una lista de aulas paginadas como dicts."""
    items = Classroom.list_all(limit=limit, offset=offset)
    return [c.to_dict() for c in items]

def create(data):
    """Crea una nueva aula a partir de un dict con claves en español.

    Espera: 'nombre_sala', 'edificio', 'capacidad', 'tipo_sala'
    """
    name = data.get('name')
    building = data.get('building')
    capacity = data.get('capacity')
    room_type = data.get('room_type', 'libre') # default 'libre'
    obj = Classroom.get_by_pk(name, building)
    if obj:
        return None
    obj = Classroom.create(name=name, building=building, capacity=capacity, room_type=room_type)
    return obj.to_dict()


def update(classroom_id, data):
    """Actualiza un aula.

    classroom_id puede ser (nombre, edificio) o un dict con esas claves.
    """
    if isinstance(classroom_id, dict):
        name = classroom_id.get('name')
        building = classroom_id.get('building')

    obj = Classroom.get_by_pk(name, building)
    if not obj:
        return None
    obj.update(capacity=data.get('capacity'), room_type=data.get('room_type'))
    return obj.to_dict()


def delete(classroom_id):
    if isinstance(classroom_id, dict):
        name = classroom_id.get('name')
        building = classroom_id.get('building')
    else:
        return None

    obj = Classroom.get_by_pk(name, building)
    if not obj:
        return None
    obj.delete()
    return {'message': 'Eliminada'}