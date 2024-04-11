from src.company_relationships.dto.request.company_relationship import CompanyRelationshipDetails, \
    CompanyRelationshipCreate
from src.company_relationships.entities.company_relationship import CompanyRelationship


class CompanyRelationshipMapper:
    @staticmethod
    def company_relationship_entity_to_dto(
            company_relationship: CompanyRelationship,
            logo_url: str
    ) -> CompanyRelationshipDetails:
        return CompanyRelationshipDetails(
            logo_url=logo_url,
            **company_relationship.__dict__
        )

    @staticmethod
    def company_relationship_dto_to_entity(
            company_relationship_create: CompanyRelationshipCreate
    ) -> CompanyRelationship:
        return CompanyRelationship(
            **company_relationship_create.model_dump(exclude=["file_name"])
        )
