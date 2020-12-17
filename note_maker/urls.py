from . import app, api
from .services.UserServices import UserService, UserListService, UserNotesService
from .services.NoteServices import NoteService, NoteListService
from .services.TagServices import TagService, TagListService
from .services.NoteLogic import NoteTagService, NoteUserService

api.add_resource(UserService, '/api/user/create/',
                 '/api/user/<int:user_id>/')

api.add_resource(NoteService, '/api/note/',
                 '/api/note/<int:note_id>/')

api.add_resource(TagService, '/api/tag/',
                 '/api/tag/<int:tag_id>/')

api.add_resource(TagListService, '/api/tag/all/')

api.add_resource(NoteListService, '/api/note/all/')

api.add_resource(UserListService, '/api/user/all/')

api.add_resource(NoteTagService, '/api/add/note/<int:note_id>/tag/<int:tag_id>/')

api.add_resource(NoteUserService, '/api/add/note/<int:note_id>/user/<int:user_id>/')

api.add_resource(UserNotesService, '/api/user/<int:user_id>/notes/')
