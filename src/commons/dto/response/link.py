from pydantic import Field

from src.commons.dto.request.link import LinkDetails
from src.commons.utils.api_response import Response


class LinkResponse(Response):
    data: LinkDetails = Field(
        ...,
        description="link details response"
    )


class LinksResponse(Response):
    data: list[LinkDetails] = Field(
        ...,
        description="list of links details as response"
    )
