from models.participant import Participant


def get_all(limit=100, offset=0):
    """Devuelve una lista de participantes paginadas como dicts."""
    items = Participant.list_all(limit=limit, offset=offset)
    result = []
    for c in items:
        # Compatibilidad: si el modelo devuelve directamente Participant instances
        # (antes), o si devolvemos {'participant': Participant, 'programas': [...]}
        if isinstance(c, dict) and 'participant' in c:
            participant_obj = c['participant']
            programas = c.get('programas', [])
            result.append({**participant_obj.to_dict(), 'programas': programas})
        else:
            # asumimos que c es una Participant
            result.append(c.to_dict())
    return result


def create(data):
    """Crea un nuevo participante.

    Acepta claves en inglés ('ci', 'name', 'surname', 'email') por consistencia con el servicio de classroom.
    Devuelve None si ya existe (la ruta transformará eso en 409).
    """
    ci = data.get('ci')
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')

    # Si ya existe, devolvemos None para que la capa de rutas maneje el 409
    obj = Participant.get_by_pk(ci)
    if obj:
        return None

    programas = data.get('programas')  # opcional
    obj = Participant.create(ci, name, surname, email, programas=programas, password=password)

    # devolver representación incluyendo programas (si existen)
    result = obj.to_dict()
    result['programas'] = Participant.get_programs(ci)
    return result


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


def add_sancion(ci, fecha_fin, fecha_inicio=None):
    """Delegar la creación de sanción al modelo Participant.

    Devuelve dict con los datos de la sanción creada, o None si participante no existe.
    Puede lanzar ValueError en caso de datos inválidos y mysql.connector.IntegrityError si la BD rechaza la inserción.
    """
    return Participant.add_sancion(ci, fecha_fin, fecha_inicio)