from typing import Type, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.commons.utils.helpers import handle_db_error

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages
from src.company_relationships.entities.company_relationship import CompanyRelationships


class CompanyRelationshipsDao:
    def __init__(self, db: Session):
        self.db = db

    def add_company_relationships(
            self,
            company_relationships: CompanyRelationships,
            user_id: str
    ) -> CompanyRelationships:
        try:
            company_relationships.save(self.db, user_id)
            return company_relationships
        except Exception as e:
            handle_db_error(
                "company_relationships -> company_relationships_dao -> add_company_relationships",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_company_relationshipss(
            self
    ) -> list[Type[CompanyRelationships]]:
        try:
            return (
                self.db.query(CompanyRelationships)
                .order_by(CompanyRelationships.name)
                .filter(
                    CompanyRelationships.is_active.__eq__(True),
                )
                .all()
            )
        except Exception as e:
            handle_db_error(
                "company_relationships -> company_relationships_dao -> get_company_relationshipss",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_company_relationships_by_id(
            self,
            company_relationships_id: str
    ) -> Union[CompanyRelationships, None]:
        try:
            return (
                self.db.query(CompanyRelationships)
                .filter(
                    and_(
                        CompanyRelationships.id.__eq__(company_relationships_id),
                        CompanyRelationships.is_active.__eq__(True),
                    )
                )
                .first()
            )
        except Exception as e:
            handle_db_error(
                "company_relationships -> company_relationships_dao -> get_company_relationships_by_id",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_company_relationships(
            self,
            company_relationships: CompanyRelationships,
            user_id: str
    ) -> CompanyRelationships:
        try:
            company_relationships.save(self.db, user_id)
            return company_relationships
        except Exception as e:
            handle_db_error(
                "company_relationships -> company_relationships_dao -> update_company_relationships",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
