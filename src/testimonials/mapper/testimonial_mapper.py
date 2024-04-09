from src.testimonials.dto.request.testimonial import TestimonialDetails, TestimonialCreate
from src.testimonials.entities.testimonials import Testimonial


class TestimonialMapper:
    @staticmethod
    def testimonial_entity_to_dto(
            testimonial: Testimonial,
            logo_url: str
    ) -> TestimonialDetails:
        return TestimonialDetails(
            logo_url=logo_url,
            **testimonial.__dict__
        )

    @staticmethod
    def testimonial_dto_to_entity(
            testimonial_create: TestimonialCreate
    ) -> Testimonial:
        return Testimonial(
            **testimonial_create.model_dump(exclude=["file_name"])
        )
