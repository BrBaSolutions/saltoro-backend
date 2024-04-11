from src.commons.dto.request.link import LinkDetails, LinkCreate
from src.commons.entities.link import Link


class LinkMapper:
    @staticmethod
    def link_entity_to_dto(
            link: Link,
            logo_url: str
    ) -> LinkDetails:
        return LinkDetails(
            logo_url=logo_url,
            **link.__dict__
        )

    @staticmethod
    def link_dto_to_entity(
            link_create: LinkCreate
    ) -> Link:
        return Link(
            **link_create.model_dump(exclude=["file_name"])
        )
