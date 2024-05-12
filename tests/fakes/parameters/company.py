from contextlib import nullcontext as does_not_raise
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
    UpdatePositionRequestSchema,
    UpdatePositionResponseSchema,
    DeletePositionResponseSchema,
    
    AddStructRequestSchema,
    UpdateStructRequestSchema,
    UpdateStructResponseSchema,
    DeleteStructResponseSchema,

    AddStructPositionRequestSchema,
    AddStructPositionResponseSchema,
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
from tests.fakes.database.fake_company import (
    FAKE_MEMBERS,
    FAKE_POSITIONS,
    FAKE_COMPANYS,
    FAKE_STRUCT,
)


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
    
    # Повторное удаление удаленной категории
    (
        {'position_id': FAKE_POSITIONS[3].id},
        DeletePositionResponseSchema(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message=f'Неверный параметр: position_id.'
        ).model_dump_json(),

        status.HTTP_400_BAD_REQUEST,
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

TEST_ENDPOINT_ADD_STRUCT: list[tuple[any]] = [
    # Добавление новой структуры с родителем
    (
        AddStructRequestSchema(
            name='added struct 1',
            parent_id=FAKE_STRUCT[3].id
        ).model_dump_json(),
        {
            'company_id': str(FAKE_COMPANYS[1].id),
            'name': 'added struct 1',
            'parent_id': str(FAKE_STRUCT[3].id)
        },
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Добавление новой структуры без родителя
    (
        AddStructRequestSchema(
            name='added struct 2',
        ).model_dump_json(),
        {
            'company_id': str(FAKE_COMPANYS[1].id),
            'name': 'added struct 2',
            'parent_id': None
        },
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Добавление структуры с parent_id позиции другой компании
    (
        AddStructRequestSchema(
            name='error struct',
            parent_id=str(FAKE_STRUCT[0].id)
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_UPDATE_STRUCT: list[tuple[any]] = [
    # Изменение своей структуры
    (
        UpdateStructRequestSchema(
            struct_id=FAKE_STRUCT[2].id,
            name='new name'
        ).model_dump_json(),
        UpdateStructResponseSchema(
            payload=StructSchema(
                id=FAKE_STRUCT[2].id,
                company_id=FAKE_STRUCT[2].company_id,
                name='new name',
                path=FAKE_STRUCT[2].path
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Изменения структуры с parent_id позиции другой компании
    (
        UpdateStructRequestSchema(
            struct_id=FAKE_STRUCT[0].id,
            name='error test'
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
] 

TEST_ENDPOINT_DELETE_STRUCT: list[tuple[any]] = [
    # Удаление своей структуры
    (
        {'struct_id': FAKE_STRUCT[3].id},
        DeleteStructResponseSchema(
            payload=StructSchema(
                id=FAKE_STRUCT[3].id,
                company_id=FAKE_STRUCT[3].company_id,
                name=FAKE_STRUCT[3].name,
                path=FAKE_STRUCT[3].path
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Повторное удаление своей структуры
    (
        {'struct_id': FAKE_STRUCT[3].id},
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),

    # Удаление чужой структуры
    (
        {'struct_id': FAKE_STRUCT[0].id},
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_ADD_STRUCT_POSITION: list[tuple[any]] = [
    # Создание позиции в своей структуре
    (
        AddStructPositionRequestSchema(
            struct_id=FAKE_STRUCT[1].id,
            position_id=FAKE_POSITIONS[1].id,
            member_id=FAKE_MEMBERS[2].id,
            is_director=True
        ).model_dump_json(),
        {'is_director': True},
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Создание позиции в чужой структуре
    (
        AddStructPositionRequestSchema(
            struct_id=FAKE_STRUCT[0].id,
            position_id=FAKE_POSITIONS[1].id,
            member_id=FAKE_MEMBERS[2].id,
            is_director=True
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
    
    # Создание позиции c чужой позицией
    (
        AddStructPositionRequestSchema(
            struct_id=FAKE_STRUCT[1].id,
            position_id=FAKE_POSITIONS[0].id,
            member_id=FAKE_MEMBERS[2].id,
            is_director=True
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: position_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
    
    # Создание позиции c чужим коллегой
    (
        AddStructPositionRequestSchema(
            struct_id=FAKE_STRUCT[1].id,
            position_id=FAKE_POSITIONS[1].id,
            member_id=FAKE_MEMBERS[0].id,
            is_director=True
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: member_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_UPDATE_STRUCT_POSITION: list[tuple[any]] = [
    
]
