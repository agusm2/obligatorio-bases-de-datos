from models.user import User
from models.participant import Participant


def authenticate(data):
    """Authenticate user credentials.

    Returns user dict on success or None on failure.
    """
    correo = data.get("user")
    password = data.get("passwd")
    if not correo or password is None:
        return None

    user = User.get_by_pk(correo)
    if not user:
        return None
    if user.password != str(password):
        return None

    user_dict = user.to_dict()

    participante = Participant.get_by_email(correo)
    if participante:
        programas = Participant.get_programs(participante.ci)
        user_dict["programas"] = programas
        user_dict["ci"] = participante.ci
    else:
        user_dict["programas"] = []

    # Return dictionary including role and sancionado flag
    if hasattr(user, "fecha_fin_sancion"):
        user_dict["fecha_fin_sancion"] = user.fecha_fin_sancion

    return user_dict
