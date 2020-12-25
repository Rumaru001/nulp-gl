from flask import request
from flask_restful import Resource

from note_maker import session, auth
from note_maker.models import Note, Tag, User, note_to_user
from note_maker.schemas import (
    user_schema, note_schema, tag_schema,
    note_list_schema, tag_list_schema)
from note_maker.services.Exceptions import Message


class NoteTagService(Resource):
    @auth.login_required
    def put(self, note_id, tag_id):
        note = session.query(Note).get(note_id)

        if note is None:
            return Message.instance_not_exist()

        if note.owner_id != auth.current_user().id:
            return Message.auth_failed()

        tag = session.query(Tag).get(tag_id)
        if tag is None:
            return Message.instance_not_exist()

        note.tags.append(tag)

        session.commit()

        return Message.successful('add tag to note')


class NoteUserService(Resource):
    @auth.login_required
    def put(self, note_id, user_id):
        note = session.query(Note).get(note_id)

        if note is None:
            return Message.instance_not_exist()

        user = session.query(User).get(user_id)
        if user is None:
            return Message.instance_not_exist()

        is_moderator = False
        for moderator in note.users:
            if moderator.id == auth.current_user().id:
                is_moderator = True
        if note.owner_id != auth.current_user().id and not is_moderator:
            return Message.auth_failed()

        max_moderators = 5
        if note.number_of_moderators >= max_moderators:
            return Message.message('Can not add a moderator', 400)

        note.number_of_moderators += 1
        note.users.append(user)
        session.commit()
        return Message.successful('add moderator to note')
