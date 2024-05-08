from contextlib import nullcontext as does_not_raise
from uuid import uuid4
from fastapi import status

from src.api.company.v1.schemas import (
    AddMemberRequestSchema,
    AddMemberResponseSchema,

    UpdateUsersEmailByAdminRequestSchema,
    UpdateUsersEmailByAdminResponseSchema,

    UpdateUsersNameByAdminRequestSchema,
    UpdateUsersNameByAdminResponseSchema,
    
    AddPositionPayloadSchema,
    AddPositionRequestSchema,
    AddPositionResponseSchema,
)
from tests.fakes.database.fake_auth import FAKE_ACCOUNTS


TEST_ENDPOINT_ADD_NEW_MEMBER: list[tuple[any]] = [
    (
        AddMemberRequestSchema(
            email='new_employee_1@gmail.com', first_name='New', last_name='One'
        ).model_dump(),
        AddMemberResponseSchema(
            payload=AddMemberRequestSchema(
                email='new_employee_1@gmail.com', first_name='New', last_name='One'
            ),
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        AddMemberRequestSchema(
            email='new_employee_1@gmail.com', first_name='New', last_name='One'
        ).model_dump(),
        AddMemberResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Пользователь new_employee_1@gmail.com уже зарегистрирован.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_UPDATE_USERS_EMAIL: list[tuple[any]] = [
    (
        UpdateUsersEmailByAdminRequestSchema(
            account_id=FAKE_ACCOUNTS[1].id,
            new_email='new_email@mail.com'
        ).model_dump_json(),
        UpdateUsersEmailByAdminResponseSchema(
            payload=UpdateUsersEmailByAdminRequestSchema(
                account_id=FAKE_ACCOUNTS[1].id,
                new_email='new_email@mail.com'
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    # (
    #     UpdateUsersEmailByAdminRequestSchema(
    #         account_id=FAKE_ACCOUNTS[0].id,
    #         new_email='new1_email@mail.com'
    #     ).model_dump_json(),
    #     UpdateUsersEmailByAdminResponseSchema(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         error=True,
    #         message=f'Неверный account_id {FAKE_ACCOUNTS[0].id}'
    #     ).model_dump_json(),
    #     status.HTTP_200_OK,
    #     does_not_raise(),
    # ),
]

TEST_ENDPOINT_UPDATE_USERS_NAME: list[tuple[any]] = [
    (
        UpdateUsersNameByAdminRequestSchema(
            account_id=str(FAKE_ACCOUNTS[0].id),
            first_name='New',
            last_name='Name',
        ).model_dump_json(),
        UpdateUsersNameByAdminResponseSchema(
            payload=UpdateUsersNameByAdminRequestSchema(
                account_id=FAKE_ACCOUNTS[0].id,
                first_name='New',
                last_name='Name',
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        UpdateUsersNameByAdminRequestSchema(
            account_id='d5ce10c2-2979-489c-b701-f1aacf0b49c3',
            first_name='New',
            last_name='Name',
        ).model_dump(),
        UpdateUsersNameByAdminResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный account_id d5ce10c2-2979-489c-b701-f1aacf0b49c3.'
        ).model_dump(),
        status.HTTP_200_OK,
        does_not_raise(),
    )
]

TEST_ENDPOINT_ADD_POSITION: list[tuple[any]] = [
    (
        AddPositionRequestSchema(title='Position', description='Test'),
        AddPositionResponseSchema(
            payload=AddPositionPayloadSchema(
                title='Position',
                description='Test',
                position_id='d5ce10c2-2979-489c-b701-f1aacf0b49c3'
            )
        ),
        status.HTTP_200_OK,
        does_not_raise(),
    )
]
