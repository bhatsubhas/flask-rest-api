from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from rest_api.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id"
                        )
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('store_id',
                            type=int,
                            required=True,
                            help="store_id is mandatory"
                            )

    @jwt_required()
    def get(self, name):
        data = Item.get_parser.parse_args()
        store_id = data.get('store_id',None)
        item = ItemModel.find_by_name(name, store_id)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name, data['store_id']):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            # Internal Server Error
            return {'message': 'An error occurred inserting the item'}, 500
        return item.json(), 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name, data['store_id'])
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred updating/inserting the item.'}, 500
        return item.json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}, 200
        return {'message': "Item with name '{}' does not exist".format(name)}, 400


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
