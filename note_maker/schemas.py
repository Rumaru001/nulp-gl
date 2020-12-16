from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import Schema, fields
from .models import (
    User, Note, Tag
)
from . import session


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        # fields = ['id', 'username', 'email', 'password', 'notes']
        model = User
        # sqla_session = session
        # # include_relationships = True
        # # load_instance = True


class NoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        # model = Note
        fields = ['id', 'name', 'text',
                  'owner_id', 'owner', 'users',
                  'number_of_moderators']

    owner = fields.Nested(UserSchema)
    users = fields.Nested(UserSchema, many=True)


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ['id', 'name', 'notes']

    notes = fields.Nested(NoteSchema, many=True)


class ExceptionSchema(Schema):
    msg = fields.String()


user_schema = UserSchema()
note_schema = NoteSchema()
note_list_schema = NoteSchema(many=True)
tag_schema = TagSchema()
tag_list_schema = TagSchema(many=True)
