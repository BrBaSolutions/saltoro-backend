from sqlalchemy import Enum


class CompanyRelationshipTypes(str, Enum):
    CLIENT = 'Client'
    PARTNER = 'Partner'
