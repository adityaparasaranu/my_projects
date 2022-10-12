from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # The below adds only valid items that as been mentioned in the `add_argument` func
    # like it would add the json only if it as the key `price` and should be in float
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This filed cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": f"A item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred in inserting the item"}, 500

        return item.json(), 200

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.find_all()]}