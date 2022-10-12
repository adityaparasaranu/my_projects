from flask_restful import Resource, reqparse
from models.staff import StaffModel


class StaffRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Any username must be given in string format!")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Password must be given for a username registration!")

    def post(self):
        data = StaffRegister.parser.parse_args()

        if StaffModel.find_by_username(data['username']):
            return {"message": "A username with provided details already exists"}, 400

        staff = StaffModel(**data)
        staff.save_to_db()

        return {"message": "Staff created successfully"}, 201


class Staff(Resource):
    @classmethod
    def get(cls, staff_id):
        staff = StaffModel.find_by_id(staff_id)
        if not staff:
            return {"message": "Staff not found"}, 404
        return staff.json()

    @classmethod
    def delete(cls, staff_id):
        staff = StaffModel.find_by_id(staff_id)
        if not staff:
            return {"message": "Staff not found"}, 404
        staff.delete_from_db()
        return {"message": "Staff deleted"}, 200
