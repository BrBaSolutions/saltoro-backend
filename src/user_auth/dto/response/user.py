from pydantic import Field

from src.commons.utils.api_response import Response
from src.user_auth.dto.request.user import UserDetails


class UserResponse(Response):
    data: UserDetails = Field(
        ...,
        description="User's Details"
    )
