from pydantic import UUID4
from sqlalchemy import Result
from src.core.utils import UnitOfWork, BaseService
from src.api.auth.utils import exceptions

from src.api.company.schemas import (
    UpdatePositionResponseSchema,
    UpdateStructRequestSchema,
    UpdateStructResponseSchema,
)
from src.api.company.v1.schemas import (
    AddPositionPayloadSchema,
    AddPositionRequestSchema,
    AddPositionResponseSchema,
    
    UpdatePositionRequestSchema,
    UpdatePositionResponseSchema,

    DeletePositionPayloadSchema,
    DeletePositionResponseSchema,

    AddStructRequestSchema,
    AddStructResponseSchema,
    AddStructPayloadSchema,
)
from src.api.company.models import PositionModel, StructAdmModel
from src.api.company.utils import bad_responses


class PositionService(BaseService):
    repository = 'position'

    @classmethod
    async def add_new_position(
        cls,
        uow: UnitOfWork,
        title: str, company_id: str, description: str = None
    ) -> AddPositionResponseSchema:
        async with uow:
            position_obj: PositionModel = await uow.position.add_one_and_get_obj(
                title=title,
                description=description,
                company_id=company_id,
            )
            return AddPositionResponseSchema(
                payload=AddPositionPayloadSchema(
                    title=title, description=description, position_id=position_obj.id
                )
            )

    @classmethod
    async def update_position(
        cls,
        uow: UnitOfWork,
        position_id: str, company_id: str, new_title: str, new_description: str = None
    ) -> UpdatePositionResponseSchema:
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
                return bad_responses.invalid_position_id(position_id=position_id)

            new_pos: UpdatePositionResponseSchema = UpdatePositionResponseSchema(
                payload=UpdatePositionRequestSchema(
                    position_id=position_id,
                    new_position=AddPositionRequestSchema(
                        title=new_title,
                        description=new_description
                    )
                )
            )
            return new_pos
    
    @classmethod
    async def delete_position(
        cls,
        uow: UnitOfWork,
        company_id: str,
        position_id: UUID4
    ) -> DeletePositionResponseSchema:
        async with uow:
            position_obj: PositionModel = await uow.position.get_by_query_one_or_none(
                company_id=company_id,
                id=position_id
            )
            
            if position_obj is None:
                return bad_responses.invalid_position_id(position_id=position_id)

            await uow.position.delete_by_query(company_id=company_id, id=position_id)
        
        return DeletePositionResponseSchema(
            payload=DeletePositionPayloadSchema(
                position_id=position_id,
                title=position_obj.title
            )
        )

    @classmethod
    async def add_struct(
        cls,
        uow: UnitOfWork,
        data: AddStructRequestSchema, company_id: UUID4
    ) -> AddStructResponseSchema:
        async with uow:
            if data.parent_id is not None:
                parent_obj: StructAdmModel = await uow.struct_adm.get_by_query_one_or_none(
                    company_id=company_id, id=data.parent_id
                )
                if parent_obj is None:
                    return bad_responses.invalid_struct_id(data.parrent_id)
            else:
                parent_obj = None

            struct_obj: StructAdmModel = await uow.struct_adm.add_new_struct(
                company_id=company_id,
                name=data.name,
                parent_obj=parent_obj
            )

        return AddStructResponseSchema(
            payload=AddStructPayloadSchema(
                struct_id=struct_obj.id,
                name=struct_obj.name
            )
        )

    @classmethod
    async def delete_struct(
        cls,
        uow: UnitOfWork,
        struct_id: str, company_id: str
    ):
        async with uow:
            struct_obj: StructAdmModel = await uow.struct_adm.get_by_query_one_or_none(
                id=struct_id, company_id=company_id
            )
            if struct_obj is None:
                raise exceptions.incorrect_param('struct_id')

            await uow.struct_adm.delete_struct_and_descendants(struct_obj)

    @classmethod
    async def update_struct(
        cls,
        uow: UnitOfWork,
        id: str, company_id: str, new_name: str
    ):
        async with uow:
            struct_obj: StructAdmModel = await uow.struct_adm.update_one_by_filters(
                filters={'id': id, 'company_id': company_id},
                values={'name': new_name}
            )
            
            if struct_obj is None:
                raise exceptions.incorrect_param('struct_id')
            
            return UpdateStructResponseSchema(
                new_item=UpdateStructRequestSchema(struct_id=id, new_name=new_name),
            )
