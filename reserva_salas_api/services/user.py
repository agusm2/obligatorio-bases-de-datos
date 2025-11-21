from models.user import User


def authenticate(data):
	"""Authenticate user credentials.

	Returns user dict on success or None on failure.
	"""
	correo = data.get('user')
	password =  data.get('passwd')
	if not correo or password is None:
		return None

	user = User.get_by_pk(correo)
	if not user:
		return None
	if user.password != str(password):
		return None

	# Return dictionary including role and sancionado flag
	return user.to_dict()