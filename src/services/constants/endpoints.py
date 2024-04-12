from enum import Enum


class Endpoints(str, Enum):
    BASE = "/api/v1"
    SERVICE = BASE + '/service'
    SERVICES = BASE + '/services'
