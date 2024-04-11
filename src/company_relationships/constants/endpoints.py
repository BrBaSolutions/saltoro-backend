from enum import Enum


class Endpoints(str, Enum):
    BASE = "/api/v1"
    COMPANY_RELATIONSHIP = '/company-relationship'
    COMPANY_RELATIONSHIPS = '/company-relationships'
