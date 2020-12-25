from flask import request
from flask_restful import Resource

from note_maker import session, auth
from note_maker.models import Tag
from note_maker.schemas import tag_schema, tag_list_schema
from note_maker.services.Exceptions import Message


class TagService(Resource):
    @auth.login_required
    def post(self):
        request_data = request.get_json()
        try:
            name = request_data['name']
        except KeyError:
            return Message.value_error()

        tag = Tag(name=name)

        if tag is None:
            return Message.creation_error()

        session.add(tag)
        session.commit()

        return Message.successful('created', 201)

    @auth.login_required
    def put(self, tag_id):
        request_data = request.get_json()
        tag = session.query(Tag).get(tag_id)

        if tag is None:
            return Message.instance_not_exist()

        if 'name' in request_data:
            tag.name = request_data['name']

        session.commit()
        return Message.successful('updated')

    def get(self, tag_id):
        print('here')
        tag = session.query(Tag).get(tag_id)
        print('here2')
        if tag is None:
            print('here3')
            return Message.instance_not_exist()
        print('here4')
        return tag_schema.dump(tag), 200

    @auth.login_required
    def delete(self, tag_id):
        tag = session.query(Tag).get(tag_id)
        if tag is None:
            return Message.instance_not_exist()
        session.delete(tag)
        session.commit()
        return Message.successful('deleted')


class TagListService(Resource):
    def get(self):
        tag_list = session.query(Tag).all()

        if not tag_list:
            return Message.instance_not_exist()

        return tag_list_schema.dump(tag_list), 200
