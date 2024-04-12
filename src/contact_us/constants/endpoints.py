from enum import Enum


class Endpoints(str, Enum):
    BASE = "/api/v1"
    CONTACT_US = BASE + '/contact-us'
