from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import Schema, fields
from .models import (
    User, Note, Tag
)
from . import session


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # sqla_session = session
        # # include_relationships = True
        # # load_instance = True


class ExceptionSchema(Schema):
    msg = fields.String()


user_schema = UserSchema()
