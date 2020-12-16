from ..schemas import ExceptionSchema

es = ExceptionSchema()


class Message:
    @staticmethod
    def message(msg: str, status_code: int):
        return es.dump(dict(msg=msg)), status_code

    @staticmethod
    def successful(msg: str = '', status_code: int = 200):
        msg = ' '.join(['Successful', msg])
        return es.dump(dict(msg=msg)), status_code

    @staticmethod
    def value_error(msg: str = 'Input value error',
                    status_code: int = 400):
        return es.dump(dict(msg=msg)), status_code

    @staticmethod
    def creation_error(msg: str = 'Instance was not created',
                       status_code: int = 400):
        return es.dump(dict(msg=msg)), status_code

    @staticmethod
    def instance_not_exist(msg: str = 'User does not exist'):
        return es.dump(dict(msg=msg)), 404
