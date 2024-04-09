from typing import Type, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.commons.entities.address import Address
from src.commons.utils.helpers import handle_db_error

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages


class AddressDao:
    def __init__(self, db: Session):
        self.db = db

    def add_address(
            self,
            address: Address,
            user_id: str
    ) -> Address:
        try:
            address.save(self.db, user_id)
            return address
        except Exception as e:
            handle_db_error(
                "common -> address_dao -> add_address",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_addresss(
            self
    ) -> list[Type[Address]]:
        try:
            return (
                self.db.query(Address)
                .order_by(Address.name)
                .filter(
                    Address.is_active.__eq__(True),
                )
                .all()
            )
        except Exception as e:
            handle_db_error(
                "common -> address_dao -> get_addresss",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_address_by_id(
            self,
            address_id: str
    ) -> Union[Address, None]:
        try:
            return (
                self.db.query(Address)
                .filter(
                    and_(
                        Address.id.__eq__(address_id),
                        Address.is_active.__eq__(True),
                    )
                )
                .first()
            )
        except Exception as e:
            handle_db_error(
                "common -> address_dao -> get_address_by_id",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_address(
            self,
            address: Address,
            user_id: str
    ) -> Address:
        try:
            address.save(self.db, user_id)
            return address
        except Exception as e:
            handle_db_error(
                "common -> address_dao -> update_address",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
