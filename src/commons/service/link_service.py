from typing import Union

from sqlalchemy.orm import Session
from starlette import status

from src.commons.constants.error_codes import ErrorCodes
from src.commons.constants.error_messages import ErrorMessages
from src.commons.dao.link_dao import LinkDao
from src.commons.dto.request.link import LinkDetails, LinkCreate, LinkUpdate
from src.commons.entities.link import Link
from src.commons.enum.file_type import FileType
from src.commons.exceptions.link_exception import LinkException
from src.commons.factory.client_factory import ClientFactory
from src.commons.mapper.link_mapper import LinkMapper
from src.commons.utils.helpers import get_file_key


class LinkService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(LinkService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Session):
        self.db = db
        self.link_dao = LinkDao(db=db)
        self.link_mapper = LinkMapper()
        self.s3_client = ClientFactory.get_s3_client()

    def _convert_link_entity_to_dto(
            self,
            link: Link
    ) -> LinkDetails:
        logo_url: str = self.s3_client.get_download_pre_signed_url(
            file_key=link.logo_key
        )

        return self.link_mapper.link_entity_to_dto(
            link=link,
            logo_url=logo_url
        )

    def _create_link(
            self,
            user_id: str,
            link_create: LinkCreate
    ) -> Link:
        link: Link = self.link_mapper.link_dto_to_entity(
            link_create=link_create
        )

        link.logo_key = get_file_key(
            file_type=FileType.LINK,
            entity_id=link.id,
            file_name=link_create.file_name
        )

        link: Link = self.link_dao.add_link(
            link=link,
            user_id=user_id
        )

        return link

    def add_link(
            self,
            user_id: str,
            link_create: LinkCreate
    ) -> str:
        link: Link = self._create_link(
            link_create=link_create,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=link.logo_key
        )

    def _get_link_by_id(
            self,
            link_id: str
    ) -> Link:
        link: Link = self.link_dao.get_link_by_id(
            link_id=link_id
        )

        if link is None:
            raise LinkException(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=ErrorCodes.LINK_NOT_FOUND,
                error_message=ErrorMessages.LINK_NOT_FOUND
            )

        return link

    def get_links(
            self
    ) -> list[LinkDetails]:
        links: list[Link] = self.link_dao.get_links()

        return [
            self._convert_link_entity_to_dto(link=link)
            for link in links
        ]

    def _update_link(
            self,
            user_id: str,
            link: Link
    ) -> Link:
        link: Link = self.link_dao.update_link(
            link=link,
            user_id=user_id
        )

        return link

    def update_link(
            self,
            user_id: str,
            link_id: str,
            link_update: LinkUpdate
    ) -> Union[str, None]:
        file_updated: bool = False

        existing_link: Link = self._get_link_by_id(
            link_id=link_id
        )

        for field, value in link_update.model_dump().items():
            if value is not None:
                if field == "file_name":
                    file_updated = True
                    existing_link.logo_key = get_file_key(
                        file_type=FileType.LINK,
                        entity_id=existing_link.id,
                        file_name=link_update.file_name
                    )
                else:
                    setattr(existing_link, field, value)

        existing_link: Link = self._update_link(
            link=existing_link,
            user_id=user_id
        )

        return self.s3_client.get_upload_pre_signed_url(
            file_key=existing_link.logo_key
        ) if file_updated else None

    def delete_link(
            self,
            user_id: str,
            link_id: str
    ) -> str:
        existing_link: Link = self._get_link_by_id(
            link_id=link_id
        )

        existing_link.is_active = False

        existing_link: Link = self._update_link(
            user_id=user_id,
            link=existing_link
        )

        return existing_link.id
