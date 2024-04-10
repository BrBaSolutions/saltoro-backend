from pydantic import Field

from src.commons.utils.api_response import Response
from src.services.dto.request.services import ServicesDetails


class ServiceResponse(Response):
    data: ServicesDetails = Field(
        ...,
        description="services details response"
    )


class ServicesResponse(Response):
    data: list[ServicesDetails] = Field(
        ...,
        description="list of services details as response"
    )
