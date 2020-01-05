from .user_entity import UserEntity, UserCollection
from .user_repository import UserRepository, UserNotFoundException as UserNotFoundRepositoryException


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def fetch(self, user_id):

        try:
            user_entity = self.user_repository.fetch(user_id)
            return FetchResponse(user_entity)
        except UserNotFoundRepositoryException as e:
            raise UserNotFoundException(e.__str__())

    def fetch_all(self):
        user_collection = self.user_repository.fetch_all()
        return FetchAllResponse(user_collection)

    def create(self, user_entity: UserEntity):
        user_entity = self.user_repository.create(user_entity)
        return CreateUserResponse(user_entity)

    def update(self, user_id, data):
        pass


class CreateUserResponse:

    def __init__(self, user_entity: UserEntity):
        self.user_entity = user_entity

    def to_dict(self):
        return self.user_entity.to_dict()


class FetchAllResponse:

    def __init__(self, user_collection: UserCollection):
        self.user_collection = user_collection

    def to_dict(self):
        return self.user_collection.to_dict()


class FetchResponse:

    def __init__(self, user_entity: UserEntity):
        self.user_entity = user_entity

    def to_dict(self):
        return self.user_entity.to_dict()


class UserNotFoundException(Exception):
    def __init__(self, message):
        super(UserNotFoundException, self).__init__(message)
