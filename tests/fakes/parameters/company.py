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
    
    UpdatePositionRequestSchema,
    UpdatePositionResponseSchema,
)
from tests.fakes.database.fake_auth import FAKE_ACCOUNTS
from tests.fakes.database.fake_company import FAKE_POSITIONS


TEST_ENDPOINT_ADD_NEW_MEMBER: list[tuple[any]] = [
    # Регистрация нового работника
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

    # Повторная регистрация нового работника
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
    # Изменение email адреса своего коллеги
    (
        UpdateUsersEmailByAdminRequestSchema(
            account_id=FAKE_ACCOUNTS[3].id,
            new_email='new_email@mail.com'
        ).model_dump_json(),
        UpdateUsersEmailByAdminResponseSchema(
            payload=UpdateUsersEmailByAdminRequestSchema(
                account_id=FAKE_ACCOUNTS[3].id,
                new_email='new_email@mail.com'
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    (
        UpdateUsersEmailByAdminRequestSchema(
            account_id=FAKE_ACCOUNTS[3].id,
            new_email='employee_2@example.com'
        ).model_dump_json(),
        UpdateUsersEmailByAdminResponseSchema(
            payload=UpdateUsersEmailByAdminRequestSchema(
                account_id=FAKE_ACCOUNTS[3].id,
                new_email='employee_2@example.com'
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Изменение email адреса сотрудника другой компании
    (
        UpdateUsersEmailByAdminRequestSchema(
            account_id=FAKE_ACCOUNTS[2].id,
            new_email='new1_email@mail.com'
        ).model_dump_json(),
        UpdateUsersEmailByAdminResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message=f'Неверный account_id {FAKE_ACCOUNTS[2].id}.'
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_UPDATE_USERS_NAME: list[tuple[any]] = [
    (
        UpdateUsersNameByAdminRequestSchema(
            account_id=FAKE_ACCOUNTS[1].id,
            first_name='New',
            last_name='Name',
        ).model_dump_json(),
        UpdateUsersNameByAdminResponseSchema(
            payload=UpdateUsersNameByAdminRequestSchema(
                account_id=FAKE_ACCOUNTS[1].id,
                first_name='New',
                last_name='Name',
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        UpdateUsersNameByAdminRequestSchema(
            account_id=FAKE_ACCOUNTS[0].id,
            first_name='New',
            last_name='Name',
        ).model_dump_json(),
        UpdateUsersNameByAdminResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message=f'Неверный account_id {FAKE_ACCOUNTS[0].id}.'
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    )
]

TEST_ENDPOINT_ADD_POSITION: list[tuple[any]] = [
    (
        AddPositionRequestSchema(title='Position', description='Test').model_dump_json(),
        AddPositionResponseSchema(
            payload=AddPositionPayloadSchema(
                title='Position',
                description='Test',
                position_id='d5ce10c2-2979-489c-b701-f1aacf0b49c3'
            )
        ),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        AddPositionRequestSchema(title='Position', description='Test').model_dump_json(),
        AddPositionResponseSchema(
            payload=AddPositionPayloadSchema(
                title='Position',
                description='Test',
                position_id='d5ce10c2-2979-489c-b701-f1aacf0b49c3'
            )
        ),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_UPDATE_POSITION: list[tuple[any]] = [
    # Изменение позиции своей компании
    (
        UpdatePositionRequestSchema(
            position_id=FAKE_POSITIONS[1].id,
            new_position=AddPositionRequestSchema(
                title='renamed position',
                description='New description'
            )
        ).model_dump_json(),
        UpdatePositionResponseSchema(
            payload=UpdatePositionRequestSchema(
                position_id=FAKE_POSITIONS[1].id,
                new_position=AddPositionRequestSchema(
                    title='renamed position',
                    description='New description'
                )
            ),
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Изменение позиции другой компании
    (
        UpdatePositionRequestSchema(
            position_id=FAKE_POSITIONS[0].id,
            new_position=AddPositionRequestSchema(
                title='renamed position',
                description='New description'
            )
        ).model_dump_json(),
        UpdatePositionResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message=f'Неверный position_id {FAKE_POSITIONS[0].id}.'
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    )
]
