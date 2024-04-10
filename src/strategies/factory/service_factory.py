from sqlalchemy.orm import Session

from src.strategies.service.strategies_service import StrategiesService


class ServiceFactory:
    @staticmethod
    def get_strategies_service(db: Session) -> StrategiesService:
        return StrategiesService(db=db)
