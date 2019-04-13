from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from rest_api.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        username = data['username']
        if UserModel.find_by_username(username):
            return {
                "message": f"A user with name '{username}' already exists"
            }, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": f"User '{username}' created successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': f"User with id '{user_id}' not found"}, 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {
                'message': f"User with id '{user_id}' deleted successfully"
            }, 200

        return {'message': f"User with id '{user_id}' not found"}, 404
