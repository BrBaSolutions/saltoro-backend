from typing import Union

from sqlalchemy.orm import Session
from starlette import status

from src.commons.client.aws.s3_client import S3Client
from src.commons.enum.file_type import FileType
from src.commons.factory.client_factory import ClientFactory
from src.commons.utils.helpers import get_file_key
from src.testimonials.constants.error_codes import ErrorCodes
from src.testimonials.constants.error_messages import ErrorMessages
from src.testimonials.dao.testimonial_dao import TestimonialDao
from src.testimonials.dto.request.testimonial import TestimonialCreate, TestimonialDetails, TestimonialUpdate
from src.testimonials.entities.testimonials import Testimonial
from src.testimonials.exceptions.testimonial_exception import TestimonialException
from src.testimonials.mapper.testimonial_mapper import TestimonialMapper


class TestimonialService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(TestimonialService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Session):
        self.db = db
        self.testimonial_dao = TestimonialDao(db=db)
        self.testimonial_mapper = TestimonialMapper()
        self.s3_client = ClientFactory.get_s3_client()

    def _convert_testimonial_entity_to_dto(
            self,
            testimonial: Testimonial
    ) -> TestimonialDetails:
        logo_url: str = self.s3_client.get_download_pre_signed_url(
            file_key=testimonial.logo_key
        )

        return self.testimonial_mapper.testimonial_entity_to_dto(
            testimonial=testimonial,
            logo_url=logo_url
        )

    def _create_testimonial(
            self,
            user_id: str,
            testimonial_create: TestimonialCreate
    ) -> Testimonial:
        testimonial: Testimonial = self.testimonial_mapper.testimonial_dto_to_entity(
            testimonial_create=testimonial_create
        )

        testimonial.logo_key = get_file_key(
            file_type=FileType.TESTIMONIAL,
            entity_id=testimonial.id,
            file_name=testimonial_create.file_name
        )

        testimonial: Testimonial = self.testimonial_dao.add_testimonial(
            testimonial=testimonial,
            user_id=user_id
        )

        return testimonial

    def add_testimonial(
            self,
            user_id: str,
            testimonial_create: TestimonialCreate
    ) -> str:
        testimonial: Testimonial = self._create_testimonial(
            testimonial_create=testimonial_create,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=testimonial.logo_key
        )

    def _get_testimonial_by_id(
            self,
            testimonial_id: str
    ) -> Testimonial:
        testimonial: Testimonial = self.testimonial_dao.get_testimonial_by_id(
            testimonial_id=testimonial_id
        )

        if testimonial is None:
            raise TestimonialException(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.TESTIMONIAL_NOT_FOUND,
                error_message=ErrorMessages.TESTIMONIAL_NOT_FOUND
            )

        return testimonial

    def get_testimonials(
            self
    ) -> list[TestimonialDetails]:
        testimonials: list[Testimonial] = self.testimonial_dao.get_testimonials()

        return [
            self._convert_testimonial_entity_to_dto(testimonial=testimonial)
            for testimonial in testimonials
        ]

    def _update_testimonial(
            self,
            user_id: str,
            testimonial: Testimonial
    ) -> Testimonial:
        testimonial: Testimonial = self.testimonial_dao.update_testimonial(
            testimonial=testimonial,
            user_id=user_id
        )

        return testimonial

    def update_testimonial(
            self,
            user_id: str,
            testimonial_id: str,
            testimonial_update: TestimonialUpdate
    ) -> Union[str, None]:
        file_updated: bool = False

        existing_testimonial: Testimonial = self._get_testimonial_by_id(
            testimonial_id=testimonial_id
        )

        for field, value in testimonial_update.model_dump().items():
            if value is not None:
                if field == "file_name":
                    file_updated = True
                    existing_testimonial.logo_key = get_file_key(
                        file_type=FileType.TESTIMONIAL,
                        entity_id=existing_testimonial.id,
                        file_name=testimonial_update.file_name
                    )
                else:
                    setattr(existing_testimonial, field, value)

        existing_testimonial: Testimonial = self._update_testimonial(
            testimonial=existing_testimonial,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=existing_testimonial.logo_key
        ) if file_updated else None

    def delete_testimonial(
            self,
            user_id: str,
            testimonial_id: str
    ) -> str:
        existing_testimonial: Testimonial = self._get_testimonial_by_id(
            testimonial_id=testimonial_id
        )

        existing_testimonial.is_active = False

        existing_testimonial: Testimonial = self._update_testimonial(
            user_id=user_id,
            testimonial=existing_testimonial
        )

        return existing_testimonial.id
