from pydantic import Field

from src.commons.utils.api_response import Response
from src.contact_us.dto.request.contact_us import ContactUsDetails


class ContactUsResponse(Response):
    data: ContactUsDetails = Field(
        ...,
        description="The contact-us details response"
    )


class ContactUsListResponse(Response):
    data: list[ContactUsDetails] = Field(
        ...,
        description="list of contact-us details as response"
    )
