from contextlib import nullcontext as does_not_raise
from uuid import uuid4
from fastapi import status

from src.core.schemas import BaseResponseModel
from src.api.company.v1.schemas import (
    AddMemberRequestSchema,
    AddMemberResponseSchema,

    UpdateUsersEmailByAdminRequestSchema,
    UpdateUsersEmailByAdminResponseSchema,

    UpdateUsersNameByAdminRequestSchema,
    UpdateUsersNameByAdminResponseSchema,

    AddPositionRequestSchema,
    AddPositionResponseSchema,

    UpdatePositionRequestSchema,
    UpdatePositionResponseSchema,

    DeletePositionResponseSchema,
)
from src.api.company.schemas import (
    CompanySchema,
    MemberSchema,
    PositionSchema,
    StructSchema,
    StructPositionSchema,
    TaskSchema
)
from tests.fakes.database.fake_auth import FAKE_ACCOUNTS
from tests.fakes.database.fake_company import FAKE_POSITIONS


TEST_ENDPOINT_ADD_NEW_MEMBER: list[tuple[any]] = [
    # Регистрация нового работника
    (
        AddMemberRequestSchema(
            email='new_employee_1@gmail.com', first_name='New', last_name='One'
        ).model_dump(),
        ...,
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
            message='Пользователь с таким адресом электронной почты уже зарегестрирован.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
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
            message=f'Неверный параметр: account_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_UPDATE_USERS_NAME: list[tuple[any]] = [
    # Изменение имени своего коллеги
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

    # Изменение имени чужого пользователя
    (
        UpdateUsersNameByAdminRequestSchema(
            account_id=FAKE_ACCOUNTS[0].id,
            first_name='New',
            last_name='Name',
        ).model_dump_json(),
        UpdateUsersNameByAdminResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message=f'Неверный параметр: account_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    )
]

TEST_ENDPOINT_ADD_POSITION: list[tuple[any]] = [
    # Добавление новой позиции
    (
        AddPositionRequestSchema(
            title='Position', description='Test'
        ).model_dump_json(),
        {'title': 'Position', 'description': 'Test'},
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Повторное добавление позиции с теми же данными
    (
        AddPositionRequestSchema(
            title='Position', description='Test').model_dump_json(),
        {'title': 'Position', 'description': 'Test'},
        status.HTTP_200_OK,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_UPDATE_POSITION: list[tuple[any]] = [
    # Изменение позиции своей компании
    (
        UpdatePositionRequestSchema(
            position_id=FAKE_POSITIONS[2].id,
            new_position=AddPositionRequestSchema(
                title='renamed position',
                description='New description'
            )
        ).model_dump_json(),
        UpdatePositionResponseSchema(
            payload=PositionSchema(
                id=FAKE_POSITIONS[2].id,
                title='renamed position',
                description='New description'
            )
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
            message=f'Неверный параметр: position_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    )
]

TEST_ENDPOINT_DELETE_POSITION: list[tuple[any]] = [
    # Удаление своей категории
    (
        {'position_id': FAKE_POSITIONS[3].id},
        DeletePositionResponseSchema(
            payload=PositionSchema(
                id=FAKE_POSITIONS[3].id,
                title=FAKE_POSITIONS[3].title,
                description=FAKE_POSITIONS[3].description
            )
        ).model_dump_json(),

        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Удаление чужой категории
    (
        {'position_id': FAKE_POSITIONS[0].id},
        DeletePositionResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message=f'Неверный параметр: position_id.'
        ).model_dump_json(),

        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

# TEST_ENDPOINT_ADD_STRUCT: list[tuple[any]] = [

# ]
