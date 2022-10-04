from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userparams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"User: {self.name}"


class UserParams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    value = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Name: {self.name}"

    def get_attributes_for_publication(self):
        return {"Name": self.name, "Type": self.type, "Value": self.value}


def create_list_of_publicated_class_attributes(user_params):
    """Take all required for publication atributes and returns json-response"""
    pubclication_list = [item.get_attributes_for_publication() for item in user_params if item]

    return json.dumps(pubclication_list)


def get_operation_fields(operation):
    """Parce operation represented as dict and returns name, type and value fields"""
    return operation.get("Name", None), operation.get("Type", None), operation.get("Value", None)


def validate_data(param_name, param_type, value):
    """Check data accuracy"""
    if param_type not in ["int", "str"]:
        return False

    if not param_name or not str(param_name).strip():
        return False

    if not value or not str(value).strip():
        return False

    return True


def add_to_database(username, param_name, param_type, value):
    """Add obtained data into database if data is correct, else returns response with ERROR status"""

    result_of_adding = {
        "Operation": "SetParam",
        "Name": param_name,
        "Type": param_type,
    }

    if not validate_data(param_name, param_type, value):
        result_of_adding["Status"] = "ERROR"
        return result_of_adding

    user_from_db = User.query.filter_by(name=username).first_or_404()

    saved_param = UserParams.query.filter_by(name=param_name, type=param_type, user_id=user_from_db.id).first()

    try:

        if not saved_param:
            param = UserParams(name=param_name, type=param_type, value=value, user_id=user_from_db.id)
            db.session.add(param)
        else:
            saved_param.value = value
            db.session.add(saved_param)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        result_of_adding["Status"] = "ERROR"
        return result_of_adding

    result_of_adding["Status"] = "OK"
    return result_of_adding


@app.route("/api/parameters/<username>/<param_name>/<param_type>/", methods=("POST", ))
def set_param(username, param_name, param_type):

    value = json.loads(request.data).get("Value")

    adding_status = add_to_database(username, param_name, param_type, value)

    return json.dumps({"Result": adding_status})


@app.route("/api/<username>/", methods=("POST", ))
def set_several_params(username):
    result_of_adding = {"Result": []}
    query = json.loads(request.data).get("Query", None)
    if not query:
        result_of_adding["Result"].append("Incorrect data format")
        return json.dumps(result_of_adding)
    for operation in query:
        if operation.get("Operation", None) != "SetParam":
            result_of_adding["Result"].append("Wrong operation type")
        param_name, param_type, value = get_operation_fields(operation)
        adding_status = add_to_database(username=username, param_name=param_name, param_type=param_type, value=value)
        result_of_adding["Result"].append(adding_status)
    return json.dumps(result_of_adding)


@app.route("/api/parameters/<username>/<param_name>/", methods=("GET", ))
@app.route("/api/parameters/<username>/<param_name>/<param_type>/", methods=("GET", ))
def get_param(username, param_name, param_type=None):
    user_from_db = User.query.filter_by(name=username).first_or_404()
    if param_type:
        user_params_from_db = [UserParams.query.filter_by(name=param_name, type=param_type,
                                                          user_id=user_from_db.id).first()]
    else:
        user_params_from_db = UserParams.query.filter_by(name=param_name, user_id=user_from_db.id).all()

    return create_list_of_publicated_class_attributes(user_params_from_db)


@app.route("/api/parameters/<user>/", methods=("GET", ))
def get_all_user_params(user):
    user_from_db = User.query.filter_by(name=user).first_or_404()
    return create_list_of_publicated_class_attributes(UserParams.query.filter_by(user_id=user_from_db.id).all())


@app.route("/add_user/", methods=("POST", "GET"))
def add_user():
    try:
        user = User(name=request.form['name'])
        db.session.add(user)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()

    return render_template("user_add.html", title="Registration")


@app.route("/")
def main_page():
    return "Welcome to the site, buddy!"


if __name__ == "__main__":
    app.run(debug=True)
