from typing import Type, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.commons.utils.helpers import handle_db_error

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages
from src.services.entities.services import Services


class ServicesDao:
    def __init__(self, db: Session):
        self.db = db

    def add_service(
            self,
            services: Services,
            user_id: str
    ) -> Services:
        try:
            services.save(self.db, user_id)
            return services
        except Exception as e:
            handle_db_error(
                "services -> services_dao -> add_service",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_services(
            self
    ) -> list[Type[Services]]:
        try:
            return (
                self.db.query(Services)
                .order_by(Services.name)
                .filter(
                    Services.is_active.__eq__(True),
                )
                .all()
            )
        except Exception as e:
            handle_db_error(
                "services -> services_dao -> get_services",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_service_by_id(
            self,
            services_id: str
    ) -> Union[Services, None]:
        try:
            return (
                self.db.query(Services)
                .filter(
                    and_(
                        Services.id.__eq__(services_id),
                        Services.is_active.__eq__(True),
                    )
                )
                .first()
            )
        except Exception as e:
            handle_db_error(
                "services -> services_dao -> get_service_by_id",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_service(
            self,
            services: Services,
            user_id: str
    ) -> Services:
        try:
            services.save(self.db, user_id)
            return services
        except Exception as e:
            handle_db_error(
                "services -> services_dao -> update_service",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
