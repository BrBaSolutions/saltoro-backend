from typing import Type, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.commons.utils.helpers import handle_db_error
from src.testimonials.entities.testimonials import Testimonial

from src.commons.constants.error_codes import ErrorCodes as CommonErrorCodes
from src.commons.constants.error_messages import ErrorMessages as CommonErrorMessages


class TestimonialDao:
    def __init__(self, db: Session):
        self.db = db

    def add_testimonial(
            self,
            testimonial: Testimonial,
            user_id: str
    ) -> Testimonial:
        try:
            testimonial.save(self.db, user_id)
            return testimonial
        except Exception as e:
            handle_db_error(
                "testimonial -> testimonial_dao -> add_testimonial",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_testimonials(
            self
    ) -> list[Type[Testimonial]]:
        try:
            return (
                self.db.query(Testimonial)
                .order_by(Testimonial.name)
                .filter(
                    Testimonial.is_active.__eq__(True),
                )
                .all()
            )
        except Exception as e:
            handle_db_error(
                "testimonial -> testimonial_dao -> get_testimonials",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def get_testimonial_by_id(
            self,
            testimonial_id: str
    ) -> Union[Testimonial, None]:
        try:
            return (
                self.db.query(Testimonial)
                .filter(
                    and_(
                        Testimonial.id.__eq__(testimonial_id),
                        Testimonial.is_active.__eq__(True),
                    )
                )
                .first()
            )
        except Exception as e:
            handle_db_error(
                "testimonial -> testimonial_dao -> get_testimonial_by_id",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )

    def update_testimonial(
            self,
            testimonial: Testimonial,
            user_id: str
    ) -> Testimonial:
        try:
            testimonial.save(self.db, user_id)
            return testimonial
        except Exception as e:
            handle_db_error(
                "testimonial -> testimonial_dao -> update_testimonial",
                CommonErrorCodes.DB_EXECUTION_ERROR,
                CommonErrorMessages.DB_EXECUTION_ERROR, e
            )
