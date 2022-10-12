from models.staff import StaffModel


def authenticate(username, password):
    staff = StaffModel.find_by_username(username)
    if staff and staff.password == password:
        return staff


def identity(payload):
    staff_id = payload['identity']
    return StaffModel.find_by_id(staff_id)

# { "identity": 1,
#   }
