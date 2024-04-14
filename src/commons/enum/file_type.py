from enum import Enum


class FileType(str, Enum):
    TESTIMONIAL = 'testimonial'
    LINK = 'link'
    COMPANY_RELATIONSHIP = 'company_relationship'
    SERVICES = 'services'
    STRATEGIES = 'strategies'
    SALTORO = 'saltoro'
