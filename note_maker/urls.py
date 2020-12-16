from . import app, api
from .services.UserServices import UserService

api.add_resource(UserService, '/api/user/create/',
                 '/api/user/<int:user_id>')
