from typing import Union

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages
from src.commons.entities.saltoro import Saltoro
from src.commons.utils.helpers import handle_db_error


class SaltoroDao:
    def __init__(self, db: Session):
        self.db = db

    def add_saltoro(
            self,
            saltoro: Saltoro,
            user_id: str
    ) -> Saltoro:
        try:
            saltoro.save(self.db, user_id)
            return saltoro
        except Exception as e:
            handle_db_error(
                "common -> saltoro_dao -> add_saltoro",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_saltoro(
            self
    ) -> Union[Saltoro, None]:
        try:
            return (
                self.db.query(Saltoro)
                .first()
            )
        except Exception as e:
            handle_db_error(
                "common -> saltoro_dao -> get_saltoro",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_count_of_saltoro(
            self
    ) -> int:
        try:
            return (
                self.db.query(func.count(Saltoro.id))
                .scalar()
            )
        except Exception as e:
            handle_db_error(
                "common -> saltoro_dao -> get_count_of_saltoro",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_saltoro(
            self,
            saltoro: Saltoro,
            user_id: str
    ) -> Saltoro:
        try:
            saltoro.save(self.db, user_id)
            return saltoro
        except Exception as e:
            handle_db_error(
                "common -> saltoro_dao -> update_saltoro",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
