from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.student import StudentModel


class StudentResource(Resource):
    # The below adds only valid items that as been mentioned in the `add_argument` func
    # like it would add the json only if it as the key `price` and should be in float
    parser = reqparse.RequestParser()
    parser.add_argument('admission_no', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('date_of_birth', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('student_class_id', type=int, required=True, help="This field cannot be left blank!")

    # @jwt_required()
    def get(self, name):
        data = request.get_json()
        student = StudentModel.find_by_name(name)
        if data["admission_no"] == student.admission_no:
            return student.json()
        return {"message": "Student not found"}, 404

    def post(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            return {"message": f"A student with name '{name}' already exists"}, 400

        data = StudentResource.parser.parse_args()

        student = StudentModel(name, **data)

        try:
            student.save_to_db()
        except:
            return {"message": "An error occurred in inserting the student"}, 500

        return student.json(), 200

    def put(self, name):
        data = StudentResource.parser.parse_args()

        student = StudentModel.find_by_name(name)

        if student is None:
            student = StudentModel(name, **data)
        else:
            student.admission_no = data["admission_no"]
            student.date_of_birth = data['date_of_birth']
            student.student_class_id = data['student_class_id']

        student.save_to_db()
        return student.json()

    def delete(self, name):
        data = request.get_json()
        student = StudentModel.find_by_name(name)
        try:
            if data["admission_no"] == student.admission_no:
                student.delete_from_db()
                return {"message": "Student deleted"}
        except:
            return {"message": "Student not found"}


class StudentList(Resource):
    def get(self):
        return {"students": [student.json() for student in StudentModel.find_all()]}