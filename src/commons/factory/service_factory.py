from sqlalchemy.orm import Session

from src.commons.service.common_service import CommonService
from src.commons.service.link_service import LinkService
from src.commons.service.saltoro_service import SaltoroService


class ServiceFactory:

    @staticmethod
    def get_common_service(db: Session):
        return CommonService(db=db)

    @staticmethod
    def get_saltoro_service(db: Session):
        return SaltoroService(db=db)

    @staticmethod
    def get_link_service(db: Session):
        return LinkService(db=db)
