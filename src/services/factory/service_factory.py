from sqlalchemy.orm import Session

from src.services.service.services_service import ServicesService


class ServiceFactory:
    @staticmethod
    def get_services_service(db: Session) -> ServicesService:
        return ServicesService(db=db)
