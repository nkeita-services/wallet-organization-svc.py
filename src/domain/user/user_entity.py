from pymongo.cursor import Cursor

from src.domain.user.user_address import UserAddress


class UserEntity:

    def __init__(self, user_id: str = None, first_name: str = None, last_name: str = None,
                 address: UserAddress = None, email: str = None, phone_number: str = None,
                 mobile_number: str = None, language: str = None, wallet_organizations=None):

        if user_id is not None:
            self.user_id = user_id

        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.mobile_number = mobile_number
        self.language = language
        self.wallet_organizations = wallet_organizations

    @classmethod
    def from_json_request(cls, json_request: dict):
        return cls(first_name=json_request['firstName'], last_name=json_request['lastName'],
                   address=UserAddress.from_json_request(json_request['address']), email=json_request['email'],
                   phone_number=json_request['phoneNumber'], mobile_number=json_request['mobileNumber'],
                   language=json_request['language'], wallet_organizations=json_request['walletOrganizations'])

    @classmethod
    def from_mongodb_document(cls, document: dict):
        return cls(user_id=str(document['_id']), first_name=document['first_name'], last_name=document['last_name'],
                   address=UserAddress.from_mongodb_document(document['address']), email=document['email'],
                   phone_number=document['phone_number'], mobile_number=document['mobile_number'],
                   language=document['language'], wallet_organizations=document['wallet_organizations'])

    def to_dict(self):
        user_dict = self.__dict__
        user_dict['address'] = user_dict['address'].to_dict()
        return user_dict


class UserCollection:

    def __init__(self, users):
        self.users = users

    @classmethod
    def from_mongodb_cursor(cls, cursor: Cursor):
        users = []
        for user in cursor:
            users.append(UserEntity.from_mongodb_document(user))
        return cls(users)

    def to_dict(self):
        users = []
        for user in self.users:
            users.append(user.to_dict())
        return users
