from typing import Type, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.commons.entities.links import Links
from src.commons.utils.helpers import handle_db_error

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages


class LinksDao:
    def __init__(self, db: Session):
        self.db = db

    def add_link(
            self,
            link: Links,
            user_id: str
    ) -> Links:
        try:
            link.save(self.db, user_id)
            return link
        except Exception as e:
            handle_db_error(
                "common -> link_dao -> add_link",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_links(
            self
    ) -> list[Type[Links]]:
        try:
            return (
                self.db.query(Links)
                .order_by(Links.name)
                .filter(
                    Links.is_active.__eq__(True),
                )
                .all()
            )
        except Exception as e:
            handle_db_error(
                "common -> link_dao -> get_links",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_link_by_id(
            self,
            link_id: str
    ) -> Union[Links, None]:
        try:
            return (
                self.db.query(Links)
                .filter(
                    and_(
                        Links.id.__eq__(link_id),
                        Links.is_active.__eq__(True),
                    )
                )
                .first()
            )
        except Exception as e:
            handle_db_error(
                "common -> link_dao -> get_link_by_id",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_link(
            self,
            link: Links,
            user_id: str
    ) -> Links:
        try:
            link.save(self.db, user_id)
            return link
        except Exception as e:
            handle_db_error(
                "common -> link_dao -> update_link",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
