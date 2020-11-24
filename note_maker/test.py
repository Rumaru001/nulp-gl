from note_maker import session, engine
from .models import *

def test():

    user_status = UserStatus(name='user')

    session.add(user_status)
    session.commit()

    status = session.query(UserStatus).filter_by(name='user').first()

    user1 = User(username="tester1",email="tester1@gmail.com",password="pass1", status=status)
    user2 = User(username="tester2",email="tester2@gmail.com",password="pass2", status=status)


    note1 = Note(name="Fisrt note",text="This is a very first note", owner=user1)
    note2 = Note(name="Second note",text="This is only a second note", owner=user2)

    user1.notes_avaliable_for_editing.append(note2)

    tag = Tag(name='tag1')

    note2.tags.append(tag)
    note2.number_of_moderators = 1

    session.add_all([tag, user1, user2, note1, note2])
    session.commit()


