from sqlalchemy.orm import Session

from src.company_relationships.service.company_relationship_service import CompanyRelationshipService


class ServiceFactory:
    @staticmethod
    def get_company_relationship_service(db: Session) -> CompanyRelationshipService:
        return CompanyRelationshipService(db=db)
