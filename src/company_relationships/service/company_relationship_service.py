from typing import Union

from sqlalchemy.orm import Session
from starlette import status

from src.commons.enum.file_type import FileType
from src.commons.factory.client_factory import ClientFactory
from src.commons.utils.helpers import get_file_key
from src.company_relationships.constants.error_codes import ErrorCodes
from src.company_relationships.constants.error_messages import ErrorMessages
from src.company_relationships.dao.company_relationship_dao import CompanyRelationshipDao
from src.company_relationships.dto.request.company_relationship import CompanyRelationshipDetails, \
    CompanyRelationshipCreate, CompanyRelationshipUpdate
from src.company_relationships.entities.company_relationship import CompanyRelationship
from src.company_relationships.exceptions.company_relationship_exception import CompanyRelationshipException
from src.company_relationships.mapper.company_relationship_mapper import CompanyRelationshipMapper


class CompanyRelationshipService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(CompanyRelationshipService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Session):
        self.db = db
        self.company_relationship_dao = CompanyRelationshipDao(db=db)
        self.company_relationship_mapper = CompanyRelationshipMapper()
        self.s3_client = ClientFactory.get_s3_client()

    def _convert_company_relationship_entity_to_dto(
            self,
            company_relationship: CompanyRelationship
    ) -> CompanyRelationshipDetails:
        logo_url: str = self.s3_client.get_download_pre_signed_url(
            file_key=company_relationship.logo_key
        )

        return self.company_relationship_mapper.company_relationship_entity_to_dto(
            company_relationship=company_relationship,
            logo_url=logo_url
        )

    def _create_company_relationship(
            self,
            user_id: str,
            company_relationship_create: CompanyRelationshipCreate
    ) -> CompanyRelationship:
        company_relationship: CompanyRelationship = self.company_relationship_mapper.company_relationship_dto_to_entity(
            company_relationship_create=company_relationship_create
        )

        company_relationship.logo_key = get_file_key(
            file_type=FileType.COMPANY_RELATIONSHIP,
            entity_id=company_relationship.id,
            file_name=company_relationship_create.file_name
        )

        company_relationship: CompanyRelationship = self.company_relationship_dao.add_company_relationship(
            company_relationship=company_relationship,
            user_id=user_id
        )

        return company_relationship

    def add_company_relationship(
            self,
            user_id: str,
            company_relationship_create: CompanyRelationshipCreate
    ) -> str:
        company_relationship: CompanyRelationship = self._create_company_relationship(
            company_relationship_create=company_relationship_create,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=company_relationship.logo_key
        )

    def _get_company_relationship_by_id(
            self,
            company_relationship_id: str
    ) -> CompanyRelationship:
        company_relationship: CompanyRelationship = self.company_relationship_dao.get_company_relationship_by_id(
            company_relationship_id=company_relationship_id
        )

        if company_relationship is None:
            raise CompanyRelationshipException(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.COMPANY_RELATIONSHIP_NOT_FOUND,
                error_message=ErrorMessages.COMPANY_RELATIONSHIP_NOT_FOUND
            )

        return company_relationship

    def get_company_relationships(
            self
    ) -> list[CompanyRelationshipDetails]:
        company_relationships: list[CompanyRelationship] = self.company_relationship_dao.get_company_relationships()

        return [
            self._convert_company_relationship_entity_to_dto(company_relationship=company_relationship)
            for company_relationship in company_relationships
        ]

    def _update_company_relationship(
            self,
            user_id: str,
            company_relationship: CompanyRelationship
    ) -> CompanyRelationship:
        company_relationship: CompanyRelationship = self.company_relationship_dao.update_company_relationship(
            company_relationship=company_relationship,
            user_id=user_id
        )

        return company_relationship

    def update_company_relationship(
            self,
            user_id: str,
            company_relationship_id: str,
            company_relationship_update: CompanyRelationshipUpdate
    ) -> Union[str, None]:
        file_updated: bool = False

        existing_company_relationship: CompanyRelationship = self._get_company_relationship_by_id(
            company_relationship_id=company_relationship_id
        )

        for field, value in company_relationship_update.model_dump().items():
            if value is not None:
                if field == "file_name":
                    file_updated = True
                    existing_company_relationship.logo_key = get_file_key(
                        file_type=FileType.COMPANY_RELATIONSHIP,
                        entity_id=existing_company_relationship.id,
                        file_name=company_relationship_update.file_name
                    )
                else:
                    setattr(existing_company_relationship, field, value)

        existing_company_relationship: CompanyRelationship = self._update_company_relationship(
            company_relationship=existing_company_relationship,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=existing_company_relationship.logo_key
        ) if file_updated else None

    def delete_company_relationship(
            self,
            user_id: str,
            company_relationship_id: str
    ) -> str:
        existing_company_relationship: CompanyRelationship = self._get_company_relationship_by_id(
            company_relationship_id=company_relationship_id
        )

        existing_company_relationship.is_active = False

        existing_company_relationship: CompanyRelationship = self._update_company_relationship(
            user_id=user_id,
            company_relationship=existing_company_relationship
        )

        return existing_company_relationship.id
