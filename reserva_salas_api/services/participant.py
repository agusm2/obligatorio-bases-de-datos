from models.participant import Participant


def get_all(limit=100, offset=0):
    """Devuelve una lista de participantes paginadas como dicts."""
    items = Participant.list_all(limit=limit, offset=offset)
    return [c.to_dict() for c in items]


def create(data):
    """Crea un nuevo participante.

    Acepta claves en inglés ('ci', 'name', 'surname', 'email') por consistencia con el servicio de classroom.
    Devuelve None si ya existe (la ruta transformará eso en 409).
    """
    ci = data.get('ci')
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')

    # Si ya existe, devolvemos None para que la capa de rutas maneje el 409
    obj = Participant.get_by_pk(ci)
    if obj:
        return None
    obj = Participant.create(ci, name, surname, email)
    return obj.to_dict()


def update(ci, data):
    """Actualiza un participante.

    ci puede ser un string o un dict con esa clave.
    """
    if isinstance(ci, dict):
        ci = ci.get('ci')

    obj = Participant.get_by_pk(ci)
    if not obj:
        return None
    obj.update(email=data.get('email'))
    return obj.to_dict()


def delete(ci):
    if isinstance(ci, dict):
        ci = ci.get('ci')
    else:
        ci = ci
    if not ci:
        return None

    obj = Participant.get_by_pk(ci)
    if not obj:
        return None
    obj.delete()
    return {'message': 'Eliminada'}