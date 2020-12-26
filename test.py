from os import name
from note_maker.schemas import NoteSchema, UserSchema, TagSchema
from note_maker.services.Exceptions import Message
import unittest
from flask.globals import session
from flask_testing import TestCase, LiveServerTestCase
from note_maker import app, api, Session, engine
from note_maker.models import Base
import json
import unittest
import base64
from note_maker.models import *


def create_user(self):
    user = User(username="user1",
                email="user1@test.com",
                password="user1test")

    self.session.add(user)
    self.session.commit()

    return user


def create_note(self):

    user = create_user(self)

    note = Note(name="note1",
                text="note1 blablablablabla",
                owner_id=user.id)

    self.session.add(note)
    self.session.commit()

    return note


def create_tag(self):

    tag = Tag(name="tag1")

    self.session.add(tag)
    self.session.commit()

    return tag


class TestNoteMaker(unittest.TestCase):
    app.testing = True
    client = app.test_client()

    @classmethod
    def setUpClass(cls):
        Base.metadata.drop_all(engine)
        print("Start of testing...")

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(engine)

    def setUp(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_create_user_succesful(self):

        response = self.client.post("/api/user/create/", data=json.dumps(dict(
            username="user1",
            email="user1@test.com",
            password="user1test"
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 201),
                         Message.successful('created', 201))

    def test_create_user_value_error(self):

        response = self.client.post("/api/user/create/", data=json.dumps(dict(
            username="user1",
            password="user1test"
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 400),
                         Message.value_error())

    def test_create_user_creation_error(self):

        user = create_user(self)

        response = self.client.post("/api/user/create/", data=json.dumps(dict(
            username="user1",
            email="user1@test.com",
            password="user1test"
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 400),
                         Message.creation_error())

    def test_get_user(self):

        user = create_user(self)

        # credentials = base64.b64encode(
        #     b"user1@test.com: user1test").decode('utf-8')

        # response = self.client.get(f"/api/user/{user.id}", headers=json.dumps({
        #                            "Authorization": "Basic user1@test.com:user1test"}),
        #                            content_type='application/json')

        response = self.client.get(f"/api/user/{user.id}/")

        self.assertEqual(response.get_json(), UserSchema().dump(user))

    def test_get_user_404(self):

        user = create_user(self)

        response = self.client.get(f"/api/user/{user.id + 2}/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_put_user(self):

        user = create_user(self)

        response = self.client.put(
            f"/api/user/{user.id}/", data=json.dumps(dict(username="user1_edited")),
            content_type='application/json')

        self.assertEqual((response.get_json(), 200),
                         Message.successful('updated'))

    def test_put_user_404(self):

        user = create_user(self)

        response = self.client.put(
            f"/api/user/{user.id + 2}/", data=json.dumps(dict(username="user1_edited")),
            content_type='application/json')

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_delete_user(self):

        user = create_user(self)

        response = self.client.delete(f"/api/user/{user.id}/")

        self.assertEqual((response.get_json(), 200),
                         Message.successful('deleted'))

    def test_delete_user_404(self):

        user = create_user(self)

        response = self.client.delete(f"/api/user/{user.id + 2}/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_userList(self):

        users = []
        for i in range(10):
            users.append(User(username=f"user{i+1}",
                              email=f"user{i+1}@test.com",
                              password=f"user{i+1}test"))
        self.session.add_all(users)
        self.session.commit()

        response = self.client.get(f"/api/user/all/")

        self.assertEqual(response.get_json(),
                         UserSchema(many=True).dump(users))

    def test_userList_404(self):

        response = self.client.get(f"/api/user/all/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_userNotesList(self):

        user = create_user(self)

        notes = []

        for i in range(10):
            notes.append(Note(name=f"name{i+1}",
                              text=f"text{i+1} blablablablablabla",
                              owner_id=user.id))
        self.session.add_all(notes)
        self.session.commit()

        response = self.client.get(f"/api/user/{user.id}/notes/")

        self.assertEqual(response.get_json(),
                         NoteSchema(many=True).dump(notes))

    def test_userNotesList_404(self):

        user = create_user(self)

        response = self.client.get(f"/api/user/{user.id+2}/notes/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    # notes

    def test_create_note_succesful(self):

        user = create_user(self)

        response = self.client.post("/api/note/", data=json.dumps(dict(
            name="note1",
            text="note1 blablablablabla",
            owner_id=user.id
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 201),
                         Message.successful('created', 201))

    def test_create_note_value_error(self):

        response = self.client.post("/api/note/", data=json.dumps(dict(
            name="note1",
            text="note1 blablablablabla",
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 400),
                         Message.value_error())

    def test_create_note_creation_error(self):

        response = self.client.post("/api/note/", data=json.dumps(dict(
            name="note1",
            text="note1 blablablablabla",
            owner_id="str"
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 400),
                         Message.creation_error())

    def test_get_note(self):

        note = create_note(self)

        response = self.client.get(f"/api/note/{note.id}/")

        self.assertEqual(response.get_json(), NoteSchema().dump(note))

    def test_get_note_404(self):

        note = create_note(self)

        response = self.client.get(f"/api/note/{note.id + 2}/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_put_note(self):

        note = create_note(self)

        response = self.client.put(
            f"/api/note/{note.id}/", data=json.dumps(dict(name="note1_edited")),
            content_type='application/json')

        self.assertEqual((response.get_json(), 200),
                         Message.successful('updated'))

    def test_put_note_404(self):

        note = create_note(self)

        response = self.client.put(
            f"/api/note/{note.id + 2}/", data=json.dumps(dict(name="note1_edited")),
            content_type='application/json')

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_delete_note(self):

        note = create_note(self)

        response = self.client.delete(f"/api/note/{note.id}/")

        self.assertEqual((response.get_json(), 200),
                         Message.successful('deleted'))

    def test_delete_note_404(self):

        note = create_note(self)

        response = self.client.delete(f"/api/note/{note.id + 2}/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_noteList(self):

        user = create_user(self)

        self.session.add(user)

        notes = []
        for i in range(10):
            notes.append(Note(name=f"note{i+1}",
                              text=f"note{i+1} blablablabla",
                              owner_id=user.id))
        self.session.add_all(notes)
        self.session.commit()

        response = self.client.get(f"/api/note/all/")

        self.assertEqual(response.get_json(),
                         NoteSchema(many=True).dump(notes))

    def test_noteList_404(self):

        response = self.client.get(f"/api/note/all/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    # tag

    def test_create_tag_succesful(self):

        response = self.client.post("/api/tag/", data=json.dumps(dict(
            name="tag1",
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 201),
                         Message.successful('created', 201))

    def test_create_tag_value_error(self):

        response = self.client.post("/api/tag/", data=json.dumps(dict(
            name=None,
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 400),
                         Message.value_error())

    def test_create_tag_creation_error(self):

        tag = create_tag(self)

        response = self.client.post("/api/tag/", data=json.dumps(dict(
            name="tag1",
        )),
            content_type='application/json')

        self.assertEqual((response.get_json(), 400),
                         Message.creation_error())

    def test_get_tag(self):

        tag = create_tag(self)

        response = self.client.get(f"/api/tag/{tag.id}/")

        self.assertEqual(response.get_json(), TagSchema().dump(tag))

    def test_get_tag_404(self):

        tag = create_tag(self)

        response = self.client.get(f"/api/tag/{tag.id + 2}/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_put_tag(self):

        tag = create_tag(self)

        response = self.client.put(
            f"/api/tag/{tag.id}/", data=json.dumps(dict(name="tag1_edited")),
            content_type='application/json')

        self.assertEqual((response.get_json(), 200),
                         Message.successful('updated'))

    def test_put_tag_404(self):

        tag = create_tag(self)

        response = self.client.put(
            f"/api/tag/{tag.id + 2}/", data=json.dumps(dict(name="tag1_edited")),
            content_type='application/json')

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_delete_tag(self):

        tag = create_tag(self)

        response = self.client.delete(f"/api/tag/{tag.id}/")

        self.assertEqual((response.get_json(), 200),
                         Message.successful('deleted'))

    def test_delete_tag_404(self):

        tag = create_tag(self)

        response = self.client.delete(f"/api/tag/{tag.id + 2}/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_tagList(self):

        tags = []
        for i in range(10):
            tags.append(Tag(name=f"tag{i+1}"))

        self.session.add_all(tags)
        self.session.commit()

        response = self.client.get(f"/api/tag/all/")

        self.assertEqual(response.get_json(),
                         TagSchema(many=True).dump(tags))

    def test_tagList_404(self):

        response = self.client.get(f"/api/tag/all/")

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    # NoteLogic

    def test_note_tag(self):

        tag = create_tag(self)

        note = create_note(self)

        response = self.client.put(
            f"/api/add/note/{note.id}/tag/{tag.id}/",
            content_type='application/json')

        self.assertEqual((response.get_json(), 200),
                         Message.successful('add tag to note'))

    def test_note_tag_404(self):

        tag = create_tag(self)

        note = create_note(self)

        response = self.client.put(
            f"/api/add/note/{note.id}/tag/{tag.id+2}/",
            content_type='application/json')

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_note_404_tag(self):

        tag = create_tag(self)

        note = create_note(self)

        response = self.client.put(
            f"/api/add/note/{note.id+2}/tag/{tag.id}/",
            content_type='application/json')

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_note_user(self):

        user = User(username=f"user{11}",
                    email=f"user{11}@test.com",
                    password=f"user{11}test")

        self.session.add(user)
        self.session.commit()

        note = create_note(self)

        response = self.client.put(
            f"/api/add/note/{note.id}/user/{user.id}/",
            content_type='application/json')

        self.assertEqual((response.get_json(), 200),
                         Message.successful('add moderator to note'))

    def test_note_user_404(self):

        user = User(username=f"user{11}",
                    email=f"user{11}@test.com",
                    password=f"user{11}test")

        self.session.add(user)
        self.session.commit()

        note = create_note(self)

        response = self.client.put(
            f"/api/add/note/{note.id}/user/{user.id+2}/",
            content_type='application/json')

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_note_404_user(self):

        user = User(username=f"user{11}",
                    email=f"user{11}@test.com",
                    password=f"user{11}test")

        self.session.add(user)
        self.session.commit()

        note = create_note(self)

        response = self.client.put(
            f"/api/add/note/{note.id+2}/user/{user.id}/",
            content_type='application/json')

        self.assertEqual((response.get_json(), 404),
                         Message.instance_not_exist())

    def test_note_user_over(self):

        users = []

        for i in range(1, 6):
            users.append(User(username=f"user{i+1}",
                              email=f"user{i+1}@test.com",
                              password=f"user{i+1}test"))

        note = create_note(self)

        note.users = users
        note.number_of_moderators = 5

        user6 = User(username=f"user{10}",
                              email=f"user{10}@test.com",
                              password=f"user{10}test")

        self.session.add(user6)
        self.session.commit()

        response = self.client.put(
            f"/api/add/note/{note.id}/user/{user6.id}/",
            content_type='application/json')

        self.assertEqual((response.get_json(), 400),
                         Message.message('Can not add a moderator', 400))
