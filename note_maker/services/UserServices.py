from flask import request
from flask_restful import Resource

from note_maker import session, auth, app
from sqlalchemy.exc import IntegrityError
from note_maker.models import User, Note
from note_maker.schemas import (
    user_schema, user_list_schema, note_list_schema)
from note_maker.services.Exceptions import Message
from werkzeug.security import check_password_hash


class UserService(Resource):
    def post(self):
        request_data = request.get_json()
        try:
            username = request_data['username']
            email = request_data['email']
            password = request_data['password']
        except KeyError:
            return Message.value_error()

        user = User(
            username=username,
            email=email,
            password=password
        )

        if user is None:
            return Message.creation_error()

        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return Message.creation_error()

        return Message.successful('created', 201)

    @auth.login_required
    def put(self, user_id):
        request_data = request.get_json()
        user = session.query(User).get(user_id)

        if user.email != auth.current_user().email:
            return Message.auth_failed()

        if user is None:
            return Message.instance_not_exist()

        if 'username' in request_data:
            user.username = request_data['username']
        if 'email' in request_data:
            user.email = request_data['email']
        if 'password' in request_data:
            user.password = request_data["password"]

        session.commit()
        return Message.successful('updated')

    def get(self, user_id):
        user = session.query(User).get(user_id)
        if user is None:
            return Message.instance_not_exist()
        return user_schema.dump(user), 200

    @auth.login_required
    def delete(self, user_id):
        user = session.query(User).get(user_id)

        if user.email != auth.current_user().email:
            return Message.auth_failed()

        if user is None:
            return Message.instance_not_exist()
        session.delete(user)
        session.commit()
        return Message.successful('deleted')


class UserListService(Resource):
    def get(self):
        user_list = session.query(User).all()

        if not user_list:
            return Message.instance_not_exist()

        return user_list_schema.dump(user_list), 200


class UserNotesService(Resource):
    def get(self, user_id):
        user = session.query(User).get(user_id)
        if user is None:
            return Message.instance_not_exist()

        user_note_list = user.notes
        return note_list_schema.dump(user_note_list)


@auth.verify_password
def verify_password(login, password):
    user = session.query(User).filter(User.email == login).first()
    if user and check_password_hash(user.password, password):
        return user


@app.route('/index', methods=['GET'])
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())
