from sqlalchemy.orm import Session

from src.contact_us.service.contact_us_service import ContactUsService


class ServiceFactory:
    @staticmethod
    def get_contact_us_service(db: Session) -> ContactUsService:
        return ContactUsService(db=db)
