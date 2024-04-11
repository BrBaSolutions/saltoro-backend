from enum import Enum


class Endpoints(str, Enum):
    BASE = "/api/v1"

    # SALTORO
    SALTORO = BASE + "/saltoro"

    # LINKS
    LINK = BASE + "/link"
    LINKS = BASE + "/links"
