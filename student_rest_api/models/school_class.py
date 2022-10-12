from db import db


class ClassModel(db.Model):
    __tablename__ = "class_sec"

    id = db.Column(db.Integer, primary_key=True)
    class_sec = db.Column(db.String(80))

    students = db.relationship("StudentModel", lazy="dynamic")
    # This is the parent table. So this table's `Id` column should
    # always have  unique values, but the store_id column of `Item`
    # table need not have to be to having unique values, but it should
    # have only the values that is present in this table's `Id` column
    # and no other values other than this. For example if this Id column
    # has 1, 2 and 3 values in it, then the store_id should only have these
    # 1, 2 or 3 or all of them. It can't have 4 in it as the parent
    # doesn't have it.

    def __init__(self, class_sec):
        self.class_sec = class_sec

    def json(self):
        return {"id": self.id,
                "class_sec": self.class_sec,
                "students": [student.json() for student in self.students]
                }

    @classmethod
    def find_by_name(cls, class_sec):
        return cls.query.filter_by(name=class_sec).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()






