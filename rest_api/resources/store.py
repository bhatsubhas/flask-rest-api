from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from rest_api.models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {
                'message': f"A store with name '{name}' already exists"
            }, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {
                'message': 'An error occurred while creating the store.'
            }, 500

        return {
            'message': f"Store '{name}' created successfully."
        }, 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {
                    'message': 'An error occurred while deleting the store.'
                }, 500

        return {'message': f"Store '{name}' is deleted!"}, 200


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {
            'stores': [store.json() for store in StoreModel.find_all()]
        }, 200
