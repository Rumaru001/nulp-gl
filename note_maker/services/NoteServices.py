from flask import request
from flask_restful import Resource

from note_maker import session
from note_maker.models import Note
from note_maker.schemas import user_schema, note_schema
from note_maker.services.Exceptions import Message


class NoteService(Resource):
    def post(self):
        request_data = request.get_json()
        try:
            name = request_data['name']
            text = request_data['text']
            owner_id = request_data['owner_id']
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

    def put(self, note_id):
        request_data = request.get_json()
        note = session.query(Note).get(note_id)

        if note is None:
            return Message.instance_not_exist()

        if 'name' in request_data:
            note.name = request_data['name']
        if 'text' in request_data:
            note.text = request_data['text']
        if 'owner_id' in request_data:
            note.owner_id = request_data["owner_id"]

        session.commit()
        return Message.successful('updated')

    def get(self, note_id):
        note = session.query(Note).get(note_id)
        if note is None:
            return Message.instance_not_exist()
        return note_schema.dump(note), 200

    def delete(self, note_id):
        note = session.query(Note).get(note_id)
        if note is None:
            return Message.instance_not_exist()
        session.delete(note)
        session.commit()
        return Message.successful('deleted')
