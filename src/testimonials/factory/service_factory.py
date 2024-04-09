from sqlalchemy.orm import Session

from src.testimonials.service.testimonial_service import TestimonialService


class ServiceFactory:
    @staticmethod
    def get_testimonial_service(db: Session) -> TestimonialService:
        return TestimonialService(db=db)
