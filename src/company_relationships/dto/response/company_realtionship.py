from pydantic import Field

from src.commons.utils.api_response import Response
from src.company_relationships.dto.request.company_relationship import CompanyRelationshipDetails


class CompanyRelationshipResponse(Response):
    data: CompanyRelationshipDetails = Field(
        ...,
        description="The company-relationships details response"
    )


class CompanyRelationshipsResponse(Response):
    data: list[CompanyRelationshipDetails] = Field(
        ...,
        description="list of company-relationships details as response"
    )
