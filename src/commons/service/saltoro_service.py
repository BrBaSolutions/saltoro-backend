from typing import Union

from sqlalchemy.orm import Session
from starlette import status

from src.commons.client.aws.s3_client import S3Client
from src.commons.dao.saltoro_dao import SaltoroDao
from src.commons.dto.request.saltoro import SaltoroDetails, SaltoroCreate, SaltoroUpdate
from src.commons.entities.saltoro import Saltoro
from src.commons.enum.file_type import FileType
from src.commons.exceptions.saltoro_exception import SaltoroException
from src.commons.mapper.saltoro_mapper import SaltoroMapper
from src.commons.utils.helpers import get_file_key
from src.commons.constants.error_codes import ErrorCodes
from src.commons.constants.error_messages import ErrorMessages


class SaltoroService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(SaltoroService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Session):
        self.db = db
        self.saltoro_dao = SaltoroDao(db=db)
        self.saltoro_mapper = SaltoroMapper()
        self.s3_client = S3Client()

    def _convert_saltoro_entity_to_dto(
            self,
            saltoro: Saltoro
    ) -> SaltoroDetails:
        logo_url: str = self.s3_client.get_download_pre_signed_url(
            file_key=saltoro.logo_key
        )

        return self.saltoro_mapper.saltoro_entity_to_dto(
            saltoro=saltoro,
            logo_url=logo_url
        )

    def _create_saltoro(
            self,
            user_id: str,
            saltoro_create: SaltoroCreate
    ) -> Saltoro:
        saltoro: Saltoro = self.saltoro_mapper.saltoro_dto_to_entity(
            saltoro_create=saltoro_create
        )

        saltoro.logo_key = get_file_key(
            file_type=FileType.TESTIMONIAL,
            entity_id=saltoro.id,
            file_name=saltoro_create.file_name
        )

        saltoro: Saltoro = self.saltoro_dao.add_saltoro(
            saltoro=saltoro,
            user_id=user_id
        )

        return saltoro

    def add_saltoro(
            self,
            user_id: str,
            saltoro_create: SaltoroCreate
    ) -> str:
        if self.saltoro_dao.get_count_of_saltoro() >= 1:
            raise SaltoroException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.ADD_SALTORO_FAILED,
                error_message=ErrorMessages.ADD_SALTORO_FAILED
            )

        saltoro: Saltoro = self._create_saltoro(
            saltoro_create=saltoro_create,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=saltoro.logo_key
        )

    def _get_saltoro(
            self
    ) -> Saltoro:
        saltoro: Saltoro = self.saltoro_dao.get_saltoro()

        if saltoro is None:
            raise SaltoroException(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.SALTORO_DETAILS_NOT_FOUND,
                error_message=ErrorMessages.SALTORO_DETAILS_NOT_FOUND
            )

        return saltoro

    def get_saltoro(
            self
    ) -> SaltoroDetails:
        saltoro: Saltoro = self._get_saltoro()

        return self._convert_saltoro_entity_to_dto(
            saltoro=saltoro
        )

    def _update_saltoro(
            self,
            user_id: str,
            saltoro: Saltoro
    ) -> Saltoro:
        saltoro: Saltoro = self.saltoro_dao.update_saltoro(
            saltoro=saltoro,
            user_id=user_id
        )

        return saltoro

    def update_saltoro(
            self,
            user_id: str,
            saltoro_update: SaltoroUpdate
    ) -> Union[str, None]:
        file_updated: bool = False

        existing_saltoro: Saltoro = self._get_saltoro()

        for field, value in saltoro_update.model_dump().items():
            if value is not None:
                if field == "file_name":
                    file_updated = True
                    existing_saltoro.logo_key = get_file_key(
                        file_type=FileType.TESTIMONIAL,
                        entity_id=existing_saltoro.id,
                        file_name=saltoro_update.file_name
                    )
                else:
                    setattr(existing_saltoro, field, value)

        existing_saltoro: Saltoro = self._update_saltoro(
            saltoro=existing_saltoro,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=existing_saltoro.logo_key
        ) if file_updated else None
