from db import db


class StudentModel(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admission_no = db.Column(db.Integer)
    date_of_birth = db.Column(db.String(20))

    student_class_id = db.Column(db.Integer, db.ForeignKey("class_sec.id"))
    # So store_id is in this table. So `Item` table is the child table,
    # and the store.id, i.e the id column of `Store` table is the parent table
    class_sec = db.relationship("ClassModel")

    def __init__(self, name, admission_no, date_of_birth, student_class_id):
        self.name = name
        self.admission_no = admission_no
        self.date_of_birth = date_of_birth
        self.student_class_id = student_class_id

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "admission_no": self.admission_no,
                "date_of_birth": self.date_of_birth,
                "student_class_id": self.student_class_id
            }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
