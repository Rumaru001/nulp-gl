from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import user
from sqlalchemy.types import Integer, String, SmallInteger, DateTime
import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from . import session

# Base class to inherite from to create models
Base = declarative_base()

# many to many table User - Note
# main purpose - store modification access for each note and user (up to 5 users per note)
note_to_user = Table('note_to_user', Base.metadata,
                     Column('note_id', ForeignKey(
                         'note.id'), primary_key=True),
                     Column('user_id', ForeignKey('user.id'), primary_key=True))

# many to many table User - Note
# main purpose - store date&time of note modification and user who did it
modifications = Table('modifications', Base.metadata,
                      Column('note_id', ForeignKey(
                          'note.id'), primary_key=True),
                      Column('user_id', ForeignKey(
                          'user.id'), primary_key=True),
                      Column('date_of_modification', DateTime, default=datetime.datetime.utcnow))


# main user model
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    email = Column(String(80), unique=True)
    password = Column(String(128))

    # own notes of this user
    notes = relationship("Note", back_populates="owner",
                         cascade="all, delete",
                         passive_deletes=True)

    # all notes that is avaliable for modifing by this user
    notes_available_for_editing = relationship("Note",
                                               secondary=note_to_user,
                                               back_populates='users')

    # all notes that was modified by this user
    notes_modifications = relationship("Note",
                                       secondary=modifications,
                                       back_populates='modifications')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


# many to many table Tag - Note
tag_to_note = Table("tag_to_note", Base.metadata,
                    Column('note_id', ForeignKey('note.id'), primary_key=True),
                    Column('tag_id', ForeignKey('tag.id'), primary_key=True))


class Note(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    text = Column(String(404), nullable=False)

    # must be handled during adding permision for user to modify note or removing this permition
    # max value = 5
    number_of_moderators = Column(SmallInteger, default=0)

    # user-owner id
    owner_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))

    # only shown/avaliable in python
    owner = relationship("User", back_populates="notes")

    # moderators (up to 5)
    users = relationship("User",
                         secondary=note_to_user,
                         back_populates='notes_available_for_editing')

    # history of modification of that note
    modifications = relationship("User",
                                 secondary=modifications,
                                 back_populates='notes_modifications')

    # all note's tags
    tags = relationship("Tag",
                        secondary=tag_to_note,
                        back_populates='notes')

    def __init__(self, name, text, owner_id):
        self.name = name
        self.text = text
        self.owner_id = owner_id

    def __repr__(self):
        return f"<Note(name={self.name}, number_of_moderators={self.number_of_moderators})>"


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), unique=True)

    # notes with with tag
    notes = relationship("Note",
                         secondary=tag_to_note,
                         back_populates='tags')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Tag(name={self.name})>"
