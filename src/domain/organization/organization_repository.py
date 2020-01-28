from pymongo.collection import Collection
from bson import ObjectId

from src.domain.organization.organization_entity import OrganizationEntity, OrganizationCollection


class OrganizationRepository:

    def __init__(self, mongodb_organization_collection: Collection):
        self.mongodb_organization_collection = mongodb_organization_collection

    def create(self, organization_entity: OrganizationEntity) -> OrganizationEntity:
        insert_one_result = self.mongodb_organization_collection.insert_one(organization_entity.to_dict())
        return self.fetch(insert_one_result.inserted_id)

    def fetch_all(self) -> OrganizationCollection:
        cursor = self.mongodb_organization_collection.find(limit=10)
        return OrganizationCollection.from_mongodb_cursor(cursor)

    def fetch(self, organization_id) -> OrganizationEntity:
        document = self.mongodb_organization_collection.find_one({'_id': ObjectId(organization_id)})
        if document is None:
            raise OrganizationNotFoundException('organization %s not found' % organization_id)
        return OrganizationEntity.from_mongodb_document(document)


class OrganizationNotFoundException(Exception):
    def __init__(self, message):
        super(OrganizationNotFoundException, self).__init__(message)
