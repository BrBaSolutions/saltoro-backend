from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.commons.dependencies.db_dependency import get_db
from src.commons.utils.api_response import Response
from src.testimonials.constants.endpoints import Endpoints
from src.testimonials.dto.request.testimonial import TestimonialCreate, TestimonialUpdate
from src.testimonials.dto.response.testimonial import TestimonialsResponse
from src.testimonials.factory.service_factory import ServiceFactory
from src.user_auth.dependencies.auth_dependency import get_current_user
from src.user_auth.dto.request.user import UserDetails

router = APIRouter()


@router.post(
    path=Endpoints.TESTIMONIAL,
    summary="Create a new testimonial",
    response_model=Response,
    tags=["TESTIMONIAL"]
)
def create_testimonial(
        testimonial_create: Annotated[TestimonialCreate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_201_CREATED,
        message="TESTIMONIAL SUCCESSFULLY CREATED",
        data=ServiceFactory.get_testimonial_service(db=db).add_testimonial(
            user_id=current_user.id,
            testimonial_create=testimonial_create
        )
    )


@router.get(
    path=Endpoints.TESTIMONIALS,
    summary="Fetch all the testimonials",
    response_model=TestimonialsResponse,
    tags=["TESTIMONIAL"]
)
def get_testimonials(
        db: Session = Depends(get_db)
) -> TestimonialsResponse:
    return TestimonialsResponse(
        status_code=status.HTTP_200_OK,
        message="TESTIMONIAL SUCCESSFULLY FETCHED",
        data=ServiceFactory.get_testimonial_service(db=db).get_testimonials()
    )


@router.put(
    path=Endpoints.TESTIMONIAL,
    summary="Update existing testimonial",
    response_model=Response,
    tags=["TESTIMONIAL"]
)
def update_testimonial(
        testimonial_id: str,
        testimonial_update: Annotated[TestimonialUpdate, Body()],
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="TESTIMONIAL SUCCESSFULLY UPDATED",
        data=ServiceFactory.get_testimonial_service(db=db).update_testimonial(
            user_id=current_user.id,
            testimonial_id=testimonial_id,
            testimonial_update=testimonial_update
        )
    )


@router.delete(
    path=Endpoints.TESTIMONIAL,
    summary="Delete existing testimonial",
    response_model=Response,
    tags=["TESTIMONIAL"]
)
def delete_testimonial(
        testimonial_id: str,
        current_user: Annotated[
            UserDetails,
            Depends(get_current_user)
        ],
        db: Session = Depends(get_db)
):
    return Response(
        status_code=status.HTTP_200_OK,
        message="TESTIMONIAL SUCCESSFULLY DELETED",
        data=ServiceFactory.get_testimonial_service(db=db).delete_testimonial(
            user_id=current_user.id,
            testimonial_id=testimonial_id
        )
    )
