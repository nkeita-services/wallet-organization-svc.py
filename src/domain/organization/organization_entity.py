from pymongo.cursor import Cursor

from src.domain.organization.organization_address import OrganizationAddress


class OrganizationEntity:

    def __init__(self, organization_id: str = None, name: str = None,
                 address: OrganizationAddress = None, email: str = None, phone_number: str = None,
                 mobile_number: str = None):
        if organization_id is not None:
            self.organization_id = organization_id

        self.name = name
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.mobile_number = mobile_number

    @classmethod
    def from_json_request(cls, json_request: dict):
        return cls(name=json_request['name'] if 'name' in json_request else None,
                   address=OrganizationAddress.from_json_request(
                       json_request['address']) if 'address' in json_request else None,
                   email=json_request['email'] if 'email' in json_request else None,
                   phone_number=json_request['phoneNumber'] if 'phoneNumber' in json_request else None,
                   mobile_number=json_request['mobileNumber'] if 'mobileNumber' in json_request else None)

    @classmethod
    def from_mongodb_document(cls, document: dict):
        return cls(organization_id=str(document['_id']), name=document['name'],
                   address=OrganizationAddress.from_mongodb_document(document['address']), email=document['email'],
                   phone_number=document['phone_number'], mobile_number=document['mobile_number'])

    def to_dict(self):
        organization_dict = self.__dict__
        organization_dict['address'] = organization_dict['address'].to_dict()
        return organization_dict


class OrganizationCollection:

    def __init__(self, organizations):
        self.organizations = organizations

    @classmethod
    def from_mongodb_cursor(cls, cursor: Cursor):
        organizations = []
        for organization in cursor:
            organizations.append(OrganizationEntity.from_mongodb_document(organization))
        return cls(organizations)

    def to_dict(self):
        organizations = []
        for organization in self.organizations:
            organizations.append(organization.to_dict())
        return organizations
