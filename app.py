from flask_jsonschema_validator import JSONSchemaValidator
from flask import Flask, jsonify, request, Response, redirect
import swagger
import jsonschema

from src.domain.user.user_entity import UserEntity
from src.domain.user.user_repository import UserRepository
from src.domain.user.user_service import UserService, UserNotFoundException
from src.infrastructure.storage.database.mongo_db.mongo_client import MongodbClient

app = Flask(__name__, static_url_path='/static')
JSONSchemaValidator(app=app, root="schemas")

app.register_blueprint(swagger.swagger_ui_blueprint, url_prefix=swagger.SWAGGER_URL)

mongodb_client = MongodbClient()
mongodb_user_collection = mongodb_client.users
user_repository = UserRepository(mongodb_user_collection)
user_service = UserService(user_repository)


@app.route('/')
def root_url():
    return redirect('/static/docs/redoc.html')


@app.route('/v1/users', methods=['POST'])
@app.validate('user', 'user_schema')
def create():
    user_entity = UserEntity.from_json_request(json_request=request.get_json())
    create_user_response = user_service.create(user_entity)
    return jsonify(create_user_response.to_dict())


@app.route('/v1/users', methods=['GET'])
def fetch_all():
    fetch_all_response = user_service.fetch_all()
    return jsonify(fetch_all_response.to_dict())


@app.route('/v1/users/<string:user_id>', methods=['GET'])
def fetch(user_id: str):
    try:
        fetch_response = user_service.fetch(user_id)
        return jsonify(fetch_response.to_dict())
    except UserNotFoundException:
        return jsonify(
            {"status": "fail", "statusCode": "4020", "statusDescription": "wallet account user not found"}), 404


@app.errorhandler(jsonschema.ValidationError)
def onValidationError(e):
    return Response("There was a validation error: " + str(e), 400)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8088)
    # app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
