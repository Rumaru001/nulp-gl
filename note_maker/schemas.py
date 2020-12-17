from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import Schema, fields
from .models import (
    User, Note, Tag
)
from . import session


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ['id', 'name']


class NoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ['id', 'name', 'text',
                  'owner_id', 'owner', 'users',
                  'number_of_moderators', 'tags']

    owner = fields.Nested(UserSchema)
    users = fields.Nested(UserSchema, many=True)
    tags = fields.Nested(TagSchema, many=True)


class ExceptionSchema(Schema):
    msg = fields.String()


user_schema = UserSchema()
user_list_schema = UserSchema(many=True)
note_schema = NoteSchema()
note_list_schema = NoteSchema(many=True)
tag_schema = TagSchema()
tag_list_schema = TagSchema(many=True)
