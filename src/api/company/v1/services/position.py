from src.core.utils import UnitOfWork, BaseService
from src.core import exceptions

from src.api.company.schemas import (
    AddPositionResponseSchema,
    AddPositionRequestSchema,
    UpdatePositionResponseSchema
)
from src.api.company.models import PositionModel


class PositionService(BaseService):
    repository = 'position'

    @classmethod
    async def add_new_position(
        cls,
        uow: UnitOfWork,
        title: str, company_id: str, description: str = None
    ):
        async with uow:
            await uow.position.add_one_and_get_obj(
                title=title,
                description=description,
                company_id=company_id,
            )
            return AddPositionResponseSchema(
                position=AddPositionRequestSchema(
                    title=title, description=description, company_id=company_id
                )
            )

    @classmethod
    async def update_position(
        cls,
        uow: UnitOfWork,
        position_id: str, company_id: str, new_title: str, new_description: str = None
    ):
        async with uow:
            filters: dict = {
                'id': position_id,
                'company_id': company_id
            }
            values: dict = {
                'title': new_title,
                'description': new_description
            }

            position_obj: PositionModel = await uow.position.update_one_by_filters(
                filters=filters,
                values=values
            )

            if position_obj is None:
                raise exceptions.incorrect_position_id()

            new_pos: UpdatePositionResponseSchema = UpdatePositionResponseSchema(
                position=AddPositionRequestSchema(
                    title=new_title,
                    description=new_description
                )
            )
            return new_pos
