from sqlalchemy.orm import Session

from src.contact_us.dao.contact_us_dao import ContactUsDao
from src.contact_us.dto.request.contact_us import ContactUsDetails, ContactUsCreate
from src.contact_us.entities.contact_us import ContactUs
from src.contact_us.mapper.contact_us_mapper import ContactUsMapper
from src.services.service.services_service import ServicesService


class ContactUsService:
    _instance = None

    def __new__(cls, db: Session):
        if cls._instance is None:
            cls._instance = super(ContactUsService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Session):
        self.db = db
        self.contact_us_dao = ContactUsDao(db=db)
        self.services_service = ServicesService(db=db)
        self.contact_us_mapper = ContactUsMapper()

    def _convert_contact_us_entity_to_dto(
            self,
            contact_us: ContactUs
    ) -> ContactUsDetails:
        return self.contact_us_mapper.contact_us_entity_to_dto(
            contact_us=contact_us,
            service_details=self.services_service.get_services_details_by_id(
                service_id=contact_us.service_id
            )
        )

    def _create_contact_us(
            self,
            contact_us_create: ContactUsCreate
    ) -> ContactUs:
        contact_us: ContactUs = self.contact_us_mapper.contact_us_dto_to_entity(
            contact_us_create=contact_us_create
        )

        contact_us: ContactUs = self.contact_us_dao.add_contact_us(
            contact_us=contact_us
        )

        return contact_us

    def add_contact_us(
            self,
            contact_us_create: ContactUsCreate
    ) -> ContactUsDetails:
        contact_us: ContactUs = self._create_contact_us(
            contact_us_create=contact_us_create,
        )

        # TODO: call email service to send email to the admin

        return self._convert_contact_us_entity_to_dto(
            contact_us=contact_us
        )

    def get_all_contact_us(
            self
    ) -> list[ContactUsDetails]:
        contact_uss: list[ContactUs] = self.contact_us_dao.get_all_contact_us()

        return [
            self._convert_contact_us_entity_to_dto(contact_us=contact_us)
            for contact_us in contact_uss
        ]

