from enum import Enum


class Endpoints(str, Enum):
    BASE = "/api/v1"
    COMPANY_RELATIONSHIP = BASE + '/company-relationship'
    COMPANY_RELATIONSHIPS = BASE + '/company-relationships'
