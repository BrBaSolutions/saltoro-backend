from pydantic import Field

from src.commons.dto.request.saltoro import SaltoroDetails
from src.commons.utils.api_response import Response


class SaltoroResponse(Response):
    data: SaltoroDetails = Field(
        ...,
        description="company details response"
    )
