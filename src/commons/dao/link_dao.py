from typing import Type, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.commons.entities.link import Link
from src.commons.utils.helpers import handle_db_error

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages


class LinkDao:
    def __init__(self, db: Session):
        self.db = db

    def add_link(
            self,
            link: Link,
            user_id: str
    ) -> Link:
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
    ) -> list[Type[Link]]:
        try:
            return (
                self.db.query(Link)
                .order_by(Link.name)
                .filter(
                    Link.is_active.__eq__(True),
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
    ) -> Union[Link, None]:
        try:
            return (
                self.db.query(Link)
                .filter(
                    and_(
                        Link.id.__eq__(link_id),
                        Link.is_active.__eq__(True),
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
            link: Link,
            user_id: str
    ) -> Link:
        try:
            link.save(self.db, user_id)
            return link
        except Exception as e:
            handle_db_error(
                "common -> link_dao -> update_link",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
