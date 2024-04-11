from typing import Type

from sqlalchemy.orm import Session

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages
from src.commons.utils.helpers import handle_db_error
from src.contact_us.entities.contact_us import ContactUs


class ContactUsDao:
    def __init__(self, db: Session):
        self.db = db

    def add_contact_us(
            self,
            contact_us: ContactUs
    ) -> ContactUs:
        try:
            contact_us.save(self.db)
            return contact_us
        except Exception as e:
            handle_db_error(
                "contact_us -> contact_us_dao -> add_contact_us",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_all_contact_us(
            self
    ) -> list[Type[ContactUs]]:
        try:
            return (
                self.db.query(ContactUs)
                .order_by(ContactUs.name)
                .all()
            )
        except Exception as e:
            handle_db_error(
                "contact_us -> contact_us_dao -> get_all_contact_us",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
