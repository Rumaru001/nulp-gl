from flask import request
from flask_restful import Resource

from note_maker import session, auth
from note_maker.models import Note, Tag
from note_maker.schemas import user_schema, note_schema, note_list_schema
from note_maker.services.Exceptions import Message


class NoteService(Resource):
    @auth.login_required
    def post(self):
        request_data = request.get_json()
        try:
            name = request_data['name']
            text = request_data['text']
            owner_id = auth.current_user().id
        except KeyError:
            return Message.value_error()

        note = Note(
            name=name,
            text=text,
            owner_id=owner_id)

        if note is None:
            return Message.creation_error()

        session.add(note)
        session.commit()

        return Message.successful('created', 201)

    @auth.login_required
    def put(self, note_id):
        request_data = request.get_json()
        note = session.query(Note).get(note_id)

        is_moderator = False
        for moderator in note.users:
            if moderator.id == auth.current_user().id:
                is_moderator = True
        if note.owner_id != auth.current_user().id and not is_moderator:
            return Message.auth_failed()

        if note is None:
            return Message.instance_not_exist()

        if 'name' in request_data:
            note.name = request_data['name']
        if 'text' in request_data:
            note.text = request_data['text']
        if 'tag_id' in request_data:
            tag_id = request_data['tag_id']
            tag = session.query(Tag).get(tag_id)
            note.tags.append(tag)

        session.commit()
        return Message.successful('updated')

    def get(self, note_id):
        note = session.query(Note).get(note_id)
        if note is None:
            return Message.instance_not_exist()
        return note_schema.dump(note), 200

    @auth.login_required
    def delete(self, note_id):
        note = session.query(Note).get(note_id)

        if note.owner_id != auth.current_user().id:
            return Message.auth_failed()

        if note is None:
            return Message.instance_not_exist()
        session.delete(note)
        session.commit()
        return Message.successful('deleted')


class NoteListService(Resource):
    def get(self):
        note_list = session.query(Note).all()

        if not note_list:
            return Message.instance_not_exist()

        return note_list_schema.dump(note_list), 200
