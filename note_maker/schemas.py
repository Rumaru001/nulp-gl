from marshmallow.decorators import validates
from marshmallow.utils import RAISE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import Schema, fields, validate
from .models import (
    User, Note, Tag
)
from . import session


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ['id', 'name']


class NoteSchema(SQLAlchemyAutoSchema):
    name = fields.Str(validate=validate.Length(max=50))
    text = fields.Str(validate=validate.Length(max=404))
    owner_id = fields.Int()

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
