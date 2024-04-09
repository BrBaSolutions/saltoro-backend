from pydantic import Field

from src.commons.utils.api_response import Response
from src.testimonials.dto.request.testimonial import TestimonialDetails


class TestimonialResponse(Response):
    data: TestimonialDetails = Field(
        ...,
        description="The testimonial details response"
    )


class TestimonialsResponse(Response):
    data: list[TestimonialDetails] = Field(
        ...,
        description="list of testimonial details as response"
    )
