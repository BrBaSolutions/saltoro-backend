from typing import Type, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.commons.utils.helpers import handle_db_error

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages
from src.contact_us.entities.contact_us import ContactUs


class ContactUsDao:
    def __init__(self, db: Session):
        self.db = db

    def add_contact_us(
            self,
            contact_us: ContactUs,
            user_id: str
    ) -> ContactUs:
        try:
            contact_us.save(self.db, user_id)
            return contact_us
        except Exception as e:
            handle_db_error(
                "contact_us -> contact_us_dao -> add_contact_us",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_contact_uss(
            self
    ) -> list[Type[ContactUs]]:
        try:
            return (
                self.db.query(ContactUs)
                .order_by(ContactUs.name)
                .filter(
                    ContactUs.is_active.__eq__(True),
                )
                .all()
            )
        except Exception as e:
            handle_db_error(
                "contact_us -> contact_us_dao -> get_contact_uss",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_contact_us_by_id(
            self,
            contact_us_id: str
    ) -> Union[ContactUs, None]:
        try:
            return (
                self.db.query(ContactUs)
                .filter(
                    and_(
                        ContactUs.id.__eq__(contact_us_id),
                        ContactUs.is_active.__eq__(True),
                    )
                )
                .first()
            )
        except Exception as e:
            handle_db_error(
                "contact_us -> contact_us_dao -> get_contact_us_by_id",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_contact_us(
            self,
            contact_us: ContactUs,
            user_id: str
    ) -> ContactUs:
        try:
            contact_us.save(self.db, user_id)
            return contact_us
        except Exception as e:
            handle_db_error(
                "contact_us -> contact_us_dao -> update_contact_us",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
