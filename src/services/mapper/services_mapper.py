from src.services.dto.request.services import ServicesDetails, ServicesCreate
from src.services.entities.services import Services


class ServicesMapper:
    @staticmethod
    def service_entity_to_dto(
            service: Services,
            asset_url: str
    ) -> ServicesDetails:
        return ServicesDetails(
            asset_url=asset_url,
            **service.__dict__
        )

    @staticmethod
    def service_dto_to_entity(
            service: ServicesCreate
    ) -> Services:
        return Services(
            **service.model_dump(exclude=["file_name"])
        )
