from pydantic import Field

from src.commons.utils.api_response import Response
from src.user_auth.dto.common.token import Token


class TokenResponse(Response):
    data: Token = Field(..., description="Tokens for the requested user")
