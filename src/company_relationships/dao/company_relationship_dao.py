from typing import Type, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.commons.utils.helpers import handle_db_error

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages
from src.company_relationships.entities.company_relationship import CompanyRelationship


class CompanyRelationshipDao:
    def __init__(self, db: Session):
        self.db = db

    def add_company_relationship(
            self,
            company_relationship: CompanyRelationship,
            user_id: str
    ) -> CompanyRelationship:
        try:
            company_relationship.save(self.db, user_id)
            return company_relationship
        except Exception as e:
            handle_db_error(
                "company_relationship -> company_relationship_dao -> add_company_relationship",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_company_relationships(
            self
    ) -> list[Type[CompanyRelationship]]:
        try:
            return (
                self.db.query(CompanyRelationship)
                .order_by(CompanyRelationship.name)
                .filter(
                    CompanyRelationship.is_active.__eq__(True),
                )
                .all()
            )
        except Exception as e:
            handle_db_error(
                "company_relationship -> company_relationship_dao -> get_company_relationships",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_company_relationship_by_id(
            self,
            company_relationship_id: str
    ) -> Union[CompanyRelationship, None]:
        try:
            return (
                self.db.query(CompanyRelationship)
                .filter(
                    and_(
                        CompanyRelationship.id.__eq__(company_relationship_id),
                        CompanyRelationship.is_active.__eq__(True),
                    )
                )
                .first()
            )
        except Exception as e:
            handle_db_error(
                "company_relationship -> company_relationship_dao -> get_company_relationship_by_id",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_company_relationship(
            self,
            company_relationship: CompanyRelationship,
            user_id: str
    ) -> CompanyRelationship:
        try:
            company_relationship.save(self.db, user_id)
            return company_relationship
        except Exception as e:
            handle_db_error(
                "company_relationship -> company_relationship_dao -> update_company_relationship",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
