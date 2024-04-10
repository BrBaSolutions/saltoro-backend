from pydantic import Field

from src.commons.utils.api_response import Response
from src.strategies.dto.request.strategy import StrategyDetails


class StrategyResponse(Response):
    data: StrategyDetails = Field(
        ...,
        description="strategies details response"
    )


class StrategiesResponse(Response):
    data: list[StrategyDetails] = Field(
        ...,
        description="list of strategies details as response"
    )
