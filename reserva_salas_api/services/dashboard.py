from models.dashboard import Dashboard


def most_reserved_rooms():
    return Dashboard.most_reserved_rooms()


def most_demanded_turns():
    return Dashboard.most_demanded_turns()


def avg_participants_per_room():
    return Dashboard.avg_participants_per_room()


def reservations_by_program_and_faculty():
    return Dashboard.reservations_by_program_and_faculty()


def occupation_percentage_by_building():
    return Dashboard.occupation_percentage_by_building()


def reservations_and_attendance_by_role_and_type():
    return Dashboard.reservations_and_attendance_by_role_and_type()


def sanctions_by_role_and_type():
    return Dashboard.sanctions_by_role_and_type()


def usage_vs_cancelled():
    return Dashboard.usage_vs_cancelled()


def participants_with_multiple_sanctions():
    return Dashboard.participants_with_multiple_sanctions()


def users_most_no_show_or_cancel():
    return Dashboard.users_most_no_show_or_cancel()


def least_used_rooms():
    return Dashboard.least_used_rooms()
