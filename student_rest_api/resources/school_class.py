from flask_restful import Resource
from models.school_class import ClassModel


class ClassResource(Resource):
    def get(self, class_sec):
        class_sec_obj = ClassModel.find_by_name(class_sec)
        if class_sec_obj:
            return class_sec_obj.json()
        return {"message": "Given class and section is not found"}, 404

    def post(self, class_sec):
        if ClassModel.find_by_name(class_sec):
            return {"message": f"A class with given section '{class_sec}' already "
                               f"exists"}, 400

        class_sec_obj = ClassModel(class_sec)
        try:
            class_sec_obj.save_to_db()
        except:
            return {"message": "An error occurred while creating the class"
                               "with specific section"}, 500

        return class_sec_obj.json(), 201

    def delete(self, class_sec):
        class_sec_obj = ClassModel.find_by_name(class_sec)
        if class_sec_obj:
           class_sec_obj.delete_from_db()

        return {"message": "The class with the given section is deleted"}


class ClassList(Resource):
    def get(self):
        return {"class_sections": [class_sec.json() for class_sec in ClassModel.find_all()]}
