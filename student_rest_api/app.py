from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.staff import StaffRegister, Staff
from resources.student import StudentResource, StudentList
from resources.school_class import ClassResource, ClassList

app = Flask(__name__)

app.secret_key = "aditya"
api = Api(app)

# uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://")
db.init_app(app)

# Run the below code in deployment case or if the `data.db` is not present
@app.before_first_request
def create_tables():
    db.create_all()


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

jwt = JWT(app, authenticate, identity)

api.add_resource(ClassResource, '/class_sec/<string:class_sec>')
api.add_resource(StudentResource, '/student/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(ClassList, '/class_sections')

api.add_resource(StaffRegister, '/register')
api.add_resource(Staff, '/staff/<int:user_id>')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
