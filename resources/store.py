from flask_restful import Resource
from models.store import StoreModel

from config import get_logger

_logger = get_logger(logger_name=__name__)


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            _logger.warning(f'A store with name \'{name}\' already exists')
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception as e:
            _logger.critical(e, exc_info=True)
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        _logger.info('Storelist accessed')
        return {'stores': [store.json() for store in StoreModel.query.all()]}
