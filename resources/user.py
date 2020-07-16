from flask_restful import Resource, reqparse

from models.user import UserModel

from config import get_logger

_logger = get_logger(logger_name=__name__)


class UserRegister(Resource):
    """
    This resource allows users to register by sending
    a POST request with their username and password.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be blank'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be blank'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            _logger.warning(f'A user with name \'{data["username"]}\' already exists')
            return {'message': 'A user with such name already exists'}, 400  # Bad request

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User create successfully'}, 201  # Created
