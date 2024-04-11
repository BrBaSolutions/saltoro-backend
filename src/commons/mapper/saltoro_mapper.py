from src.commons.dto.request.saltoro import SaltoroDetails, SaltoroCreate
from src.commons.entities.saltoro import Saltoro


class SaltoroMapper:
    @staticmethod
    def saltoro_entity_to_dto(
            saltoro: Saltoro,
            logo_url: str
    ) -> SaltoroDetails:
        return SaltoroDetails(
            logo_url=logo_url,
            **saltoro.__dict__
        )

    @staticmethod
    def saltoro_dto_to_entity(
            saltoro_create: SaltoroCreate
    ) -> Saltoro:
        return Saltoro(
            **saltoro_create.model_dump(exclude=["file_name"])
        )
