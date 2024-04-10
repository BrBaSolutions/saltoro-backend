from enum import Enum


class Endpoints(str, Enum):
    BASE = '/api/v1'
    STRATEGY = '/strategy'
    STRATEGIES = '/strategies'
