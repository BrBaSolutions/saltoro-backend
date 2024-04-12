from enum import Enum


class Endpoints(str, Enum):
    BASE = '/api/v1'
    STRATEGY = BASE + '/strategy'
    STRATEGIES = BASE + '/strategies'
