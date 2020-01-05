from pymongo.collection import Collection
from bson import ObjectId

from src.domain.user.user_entity import UserEntity, UserCollection


class UserRepository:

    def __init__(self, mongodb_user_collection: Collection):
        self.mongodb_user_collection = mongodb_user_collection

    def create(self, user_entity: UserEntity) -> UserEntity:
        insert_one_result = self.mongodb_user_collection.insert_one(user_entity.to_dict())
        return self.fetch(insert_one_result.inserted_id)

    def fetch_all(self) -> UserCollection:
        cursor = self.mongodb_user_collection.find(limit=10)
        return UserCollection.from_mongodb_cursor(cursor)

    def fetch(self, user_id) -> UserEntity:
        document = self.mongodb_user_collection.find_one({'_id': ObjectId(user_id)})
        if document is None:
            raise UserNotFoundException('user %s not found' % user_id)
        return UserEntity.from_mongodb_document(document)


class UserNotFoundException(Exception):
    def __init__(self, message):
        super(UserNotFoundException, self).__init__(message)
