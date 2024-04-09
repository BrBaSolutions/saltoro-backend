from typing import Optional

from pydantic import BaseModel, Field


class Strategy(BaseModel):
    heading: str = Field(
        ...,
        description="Title of the strategy"
    )
    sub_heading: Optional[str] = Field(
        None,
        description="Sub-Heading for the strategy"
    )
    description: str = Field(
        ...,
        description="Strategy description"
    )


class StrategyCreate(Strategy):
    file_name: str = Field(
        ...,
        description="Asset-File Name"
    )


class StrategyDetails(Strategy):
    id: str = Field(
        ...,
        description="Primary-Key Id of the testimonial"
    )
    asset_url: str = Field(
        ...,
        description="S3 url to access logo"
    )
    is_active: bool = Field(
        ...,
        description="Is-Strategy still active?"
    )
