from typing import Union

from sqlalchemy.orm import Session
from starlette import status

from src.commons.client.aws.s3_client import S3Client
from src.commons.enum.file_type import FileType
from src.commons.utils.helpers import get_file_key
from src.services.constants.error_codes import ErrorCodes
from src.services.constants.error_messages import ErrorMessages
from src.services.dao.services_dao import ServicesDao
from src.services.dto.request.services import ServicesDetails, ServicesCreate, ServicesUpdate
from src.services.entities.services import Services
from src.services.exceptions.services_exception import ServicesException
from src.services.mapper.services_mapper import ServicesMapper


class ServicesService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(ServicesService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Session):
        self.db = db
        self.services_dao = ServicesDao(db=db)
        self.service_mapper = ServicesMapper()
        self.s3_client = S3Client()

    def _convert_service_entity_to_dto(
            self,
            service: Services
    ) -> ServicesDetails:
        asset_url: str = self.s3_client.get_download_pre_signed_url(
            file_key=service.asset_key
        )

        return self.service_mapper.service_entity_to_dto(
            service=service,
            asset_url=asset_url
        )

    def _create_service(
            self,
            user_id: str,
            service_create: ServicesCreate
    ) -> Services:
        service: Services = self.service_mapper.service_dto_to_entity(
            service=service_create
        )

        service.asset_key = get_file_key(
            file_type=FileType.TESTIMONIAL,
            entity_id=service.id,
            file_name=service_create.file_name
        )

        service: Services = self.services_dao.add_service(
            services=service,
            user_id=user_id
        )

        return service

    def add_service(
            self,
            user_id: str,
            service_create: ServicesCreate
    ) -> str:
        service: Services = self._create_service(
            service_create=service_create,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=service.asset_key
        )

    def _get_service_by_id(
            self,
            service_id: str
    ) -> Services:
        service: Services = self.services_dao.get_service_by_id(
            services_id=service_id
        )

        if service_id is None:
            raise ServicesException(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.SERVICES_NOT_FOUND,
                error_message=ErrorMessages.SERVICES_NOT_FOUND
            )

        return service

    def get_services_details_by_id(
            self,
            service_id: str
    ) -> ServicesDetails:
        service: Services = self._get_service_by_id(
            service_id=service_id
        )

        return self._convert_service_entity_to_dto(
            service=service
        )

    def get_services(
            self
    ) -> list[ServicesDetails]:
        services: list[Services] = self.services_dao.get_services()

        return [
            self._convert_service_entity_to_dto(service=service)
            for service in services
        ]

    def _update_service(
            self,
            user_id: str,
            service: Services
    ) -> Services:
        service: Services = self.services_dao.update_service(
            services=service,
            user_id=user_id
        )

        return service

    def update_service(
            self,
            user_id: str,
            service_id: str,
            service_update: ServicesUpdate
    ) -> Union[str, None]:
        file_updated: bool = False

        existing_service: Services = self._get_service_by_id(
            service_id=service_id
        )

        for field, value in service_update.model_dump().items():
            if value is not None:
                if field == "file_name":
                    file_updated = True
                    existing_service.asset_key = get_file_key(
                        file_type=FileType.TESTIMONIAL,
                        entity_id=existing_service.id,
                        file_name=service_update.file_name
                    )
                else:
                    setattr(existing_service, field, value)

        existing_service: Services = self._update_service(
            service=existing_service,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=existing_service.asset_key
        ) if file_updated else None

    def delete_service(
            self,
            user_id: str,
            service_id: str
    ) -> str:
        existing_service: Services = self._get_service_by_id(
            service_id=service_id
        )

        existing_service.is_active = False

        existing_service: Services = self._update_service(
            user_id=user_id,
            service=existing_service
        )

        return existing_service.id
