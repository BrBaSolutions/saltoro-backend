from src.contact_us.dto.request.contact_us import ContactUsDetails, ContactUsCreate
from src.contact_us.entities.contact_us import ContactUs
from src.services.dto.request.services import ServicesDetails


class ContactUsMapper:
    @staticmethod
    def contact_us_entity_to_dto(
            contact_us: ContactUs,
            service_details: ServicesDetails
    ) -> ContactUsDetails:
        return ContactUsDetails(
            service_details=service_details,
            **contact_us.__dict__
        )

    @staticmethod
    def contact_us_dto_to_entity(
            contact_us_create: ContactUsCreate
    ) -> ContactUs:
        return ContactUs(
            **contact_us_create.model_dump()
        )
