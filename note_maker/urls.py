from . import app, api
from .services.UserServices import UserService
from .services.NoteServices import NoteService
from .services.TagServices import TagService, TagListService

api.add_resource(UserService, '/api/user/create/',
                 '/api/user/<int:user_id>')

api.add_resource(NoteService, '/api/note/',
                 '/api/note/<int:note_id>/')

api.add_resource(TagService, '/api/tag/',
                 '/api/tag/<int:tag_id>/')

api.add_resource(TagListService, '/api/tag/all/')
