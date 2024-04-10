from enum import Enum


class Endpoints(str, Enum):
    BASE = "/api/v1"
    SERVICE = '/service'
    SERVICES = '/services'
