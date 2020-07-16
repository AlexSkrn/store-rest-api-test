import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from security import authenticate, identity

from config import get_logger

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

from config import DevelopmentConfig

from db import db

_logger = get_logger(logger_name=__name__)

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
# app.config['DEBUG'] = True
#
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY').encode()
# app.secret_key = os.environ.get('SECRET_KEY').encode()

# prepare app to work with db
db.init_app(app)

api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

# This decorator allows customizing authorization error message
# @app.errorhandler(JWTError)
# def auth_error(err):
#     return jsonify(
#         {'message':
#          'Could not authorize. Did you include a valid auth header?'
#          }
#         ), 401  # Unauthorized

_logger.debug('Application created.')

if __name__ == '__main__':
    # This block is for development. For production, use run.py
    # To set up a production database, run setup_db.py first

    # from db import db
    #
    # db.init_app(app)

    # if app.config['DEBUG']:
    @app.before_first_request
    def create_tables():
        db.drop_all()
        db.create_all()

    app.run()  # port=5000
