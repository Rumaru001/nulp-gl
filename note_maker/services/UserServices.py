from flask import request, jsonify, Response

from flask_restful import Resource
from note_maker.services.Exceptions import Message
from note_maker.models import User
from note_maker.schemas import user_schema
from note_maker import session


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
        session.commit()

        return Message.successful('created', 201)

    def put(self, user_id):
        request_data = request.get_json()
        user = session.query(User).get(user_id)

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

    def delete(self, user_id):
        user = session.query(User).get(user_id)
        if user is None:
            return Message.instance_not_exist()
        session.delete(user)
        session.commit()
        return Message.successful('deleted')
