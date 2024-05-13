from contextlib import nullcontext as does_not_raise
from datetime import datetime
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
    UpdateStructPositionRequestSchema,
    UpdateStructPositionResponseSchema,
    DeleteStructPositionResponseSchema,

    TaskPayloadSchema,
    AddTaskRequestSchema,
    AddTaskResponseSchema,
    UpdateTaskRequestSchema,
    UpdateTaskResponseSchema,
    DeleteTaskResponseSchema

)
from src.api.company.schemas import (
    CompanySchema,
    MemberSchema,
    PositionSchema,
    StructSchema,
    StructPositionSchema,
    TaskSchema,
)
from tests.fakes.database.fake_auth import FAKE_ACCOUNTS
from tests.fakes.database.fake_company import (
    FAKE_MEMBERS,
    FAKE_POSITIONS,
    FAKE_COMPANYS,
    FAKE_STRUCT,
    FAKE_STRUCT_POSITION,
    FAKE_TASKS
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
    # Изменение корректной позиции структуры
    (
        UpdateStructPositionRequestSchema(
            struct_position_id=FAKE_STRUCT_POSITION[2].id,
            struct_id=FAKE_STRUCT[2].id,
            position_id=FAKE_POSITIONS[2].id,
            member_id=FAKE_MEMBERS[3].id,
            is_director=False
        ).model_dump_json(),
        UpdateStructPositionResponseSchema(
            payload=StructPositionSchema(
                id=FAKE_STRUCT_POSITION[2].id,
                struct_id=FAKE_STRUCT[2].id,
                position_id=FAKE_POSITIONS[2].id,
                member_id=FAKE_MEMBERS[3].id,
                is_director=False
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Неверный struct_position_id
    (
        UpdateStructPositionRequestSchema(
            struct_position_id=FAKE_STRUCT_POSITION[1].id,
            struct_id=FAKE_STRUCT[2].id,
            position_id=FAKE_POSITIONS[2].id,
            member_id=FAKE_MEMBERS[3].id,
            is_director=False
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_position_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),

    # Неверный struct_id
    (
        UpdateStructPositionRequestSchema(
            struct_position_id=FAKE_STRUCT_POSITION[2].id,
            struct_id=FAKE_STRUCT[0].id,
            position_id=FAKE_POSITIONS[2].id,
            member_id=FAKE_MEMBERS[3].id,
            is_director=False
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),

    # Неверный position_id
    (
        UpdateStructPositionRequestSchema(
            struct_position_id=FAKE_STRUCT_POSITION[2].id,
            struct_id=FAKE_STRUCT[1].id,
            position_id=FAKE_POSITIONS[0].id,
            member_id=FAKE_MEMBERS[3].id,
            is_director=False
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: position_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),

    # Неверный member_id
    (
        UpdateStructPositionRequestSchema(
            struct_position_id=FAKE_STRUCT_POSITION[2].id,
            struct_id=FAKE_STRUCT[1].id,
            position_id=FAKE_POSITIONS[2].id,
            member_id=FAKE_MEMBERS[1].id,
            is_director=False
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

TEST_ENDPOINT_DELETE_STRUCT_POSITION: list[tuple[any]] = [
    # Удаление корректной позиции структуры
    (
        {'struct_position_id': FAKE_STRUCT_POSITION[2].id},
        DeleteStructPositionResponseSchema(
            payload=StructPositionSchema(
                id=FAKE_STRUCT_POSITION[2].id,
                struct_id=FAKE_STRUCT[2].id,
                position_id=FAKE_POSITIONS[2].id,
                member_id=FAKE_MEMBERS[3].id,
                is_director=False
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Повторная попытка удаления
    (
        {'struct_position_id': FAKE_STRUCT_POSITION[2].id},
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_position_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),

    # Удаление чужой позиции структуры
    (
        {'struct_position_id': FAKE_STRUCT_POSITION[1].id},
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: struct_position_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_ADD_TASK: list[tuple[any]] = [
    # Добавление новой задачи
    (
        AddTaskRequestSchema(
            title='new added task 1',
            description='descr',
            responsible_id=FAKE_ACCOUNTS[3].id,
            deadline=datetime(2030, 1, 1),
            observers=[FAKE_ACCOUNTS[1].id, FAKE_ACCOUNTS[3].id],
            performers=[FAKE_ACCOUNTS[1].id, FAKE_ACCOUNTS[3].id],
        ).model_dump_json(),
        {
            'title': 'new added task 1',
            'description': 'descr',
            'responsible_id': str(FAKE_ACCOUNTS[3].id),
            'deadline': '2030-01-01T00:00:00',
            'author_id': str(FAKE_ACCOUNTS[1].id),
            'observers': [str(FAKE_ACCOUNTS[1].id), str(FAKE_ACCOUNTS[3].id)],
            'performers': [str(FAKE_ACCOUNTS[1].id), str(FAKE_ACCOUNTS[3].id)],
        },
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    (
        AddTaskRequestSchema(
            title='new added task 2',
            deadline=datetime(2030, 1, 1),
        ).model_dump_json(),
        {
            'title': 'new added task 2',
            'description': None,
            'responsible_id': None,
            'deadline': '2030-01-01T00:00:00',
            'author_id': str(FAKE_ACCOUNTS[1].id),
            'observers': [],
            'performers': [],
        },
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Добавление задачи с неправильным responsible_id
    (
        AddTaskRequestSchema(
            title='error task 3',
            responsible_id=FAKE_ACCOUNTS[0].id,
            deadline=datetime(2030, 1, 1),
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Один из введенных id аккаунта некорректен.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),

    # Добавление задачи с неправильным observer_id
    (
        AddTaskRequestSchema(
            title='error task 2',
            deadline=datetime(2030, 1, 1),
            observers=[FAKE_ACCOUNTS[0].id]
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Один из введенных id аккаунта некорректен.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),

    # Добавление задачи с неправильным performer_id
    (
        AddTaskRequestSchema(
            title='error task 2',
            deadline=datetime(2030, 1, 1),
            performers=[FAKE_ACCOUNTS[0].id]
        ).model_dump_json(),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Один из введенных id аккаунта некорректен.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_UPDATE_TASK: list[tuple[any]] = [
    # Изменение задачи
    (
        UpdateTaskRequestSchema(
            task_id=FAKE_TASKS[2].id,
            title='new title',
            description='new descr',
            responsible_id=FAKE_ACCOUNTS[3].id,
            deadline=datetime(2040, 2, 2),
            observers=[FAKE_ACCOUNTS[1].id, FAKE_ACCOUNTS[3].id],
            performers=[FAKE_ACCOUNTS[1].id, FAKE_ACCOUNTS[3].id],
            status='IN_PROGRESS'
        ).model_dump_json(),
        UpdateTaskResponseSchema(
            payload=TaskPayloadSchema(
                id=str(FAKE_TASKS[2].id),
                title='new title',
                description='new descr',
                author_id=str(FAKE_ACCOUNTS[1].id),
                responsible_id=str(FAKE_ACCOUNTS[3].id),
                deadline='2040-02-02T00:00:00',
                status='IN_PROGRESS',
                observers=[str(FAKE_ACCOUNTS[1].id), str(FAKE_ACCOUNTS[3].id)],
                performers=[str(FAKE_ACCOUNTS[1].id),
                            str(FAKE_ACCOUNTS[3].id)],
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),

    # Изменение задачи пустыми значениями, задача не меняется
    (
        UpdateTaskRequestSchema(
            task_id=FAKE_TASKS[2].id
        ).model_dump_json(exclude_unset=True),
        UpdateTaskResponseSchema(
            payload=TaskPayloadSchema(
                id=str(FAKE_TASKS[2].id),
                title='new title',
                description='new descr',
                author_id=str(FAKE_ACCOUNTS[1].id),
                responsible_id=str(FAKE_ACCOUNTS[3].id),
                deadline='2040-02-02T00:00:00',
                status='IN_PROGRESS',
                observers=[str(FAKE_ACCOUNTS[1].id), str(FAKE_ACCOUNTS[3].id)],
                performers=[str(FAKE_ACCOUNTS[1].id),
                            str(FAKE_ACCOUNTS[3].id)],
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Изменение задачи с неправильным task_id
    (
        UpdateTaskRequestSchema(
            task_id=FAKE_TASKS[0].id
        ).model_dump_json(exclude_unset=True),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: task_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
    
    # Изменение задачи с неправильным responsible_id
    (
        UpdateTaskRequestSchema(
            task_id=FAKE_TASKS[2].id,
            responsible_id=FAKE_TASKS[0].id,
        ).model_dump_json(exclude_unset=True),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Один из введенных id аккаунта некорректен.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
    
    # Изменение задачи с неправильным observers
    (
        UpdateTaskRequestSchema(
            task_id=FAKE_TASKS[2].id,
            observers=[FAKE_TASKS[0].id]
        ).model_dump_json(exclude_unset=True),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Один из введенных id аккаунта некорректен.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
    
    # Изменение задачи с неправильным performers
    (
        UpdateTaskRequestSchema(
            task_id=FAKE_TASKS[2].id,
            performers=[FAKE_TASKS[0].id]
        ).model_dump_json(exclude_unset=True),
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Один из введенных id аккаунта некорректен.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]

TEST_ENDPOINT_DELETE_TASK: list[tuple[any]] = [
    # Удаление задачи
    (
        {'task_id': str(FAKE_TASKS[3].id)},
        DeleteTaskResponseSchema(
            payload=TaskPayloadSchema(
                id=str(FAKE_TASKS[3].id),
                title=FAKE_TASKS[3].title,
                description=None,
                author_id=str(FAKE_ACCOUNTS[1].id),
                responsible_id=None,
                deadline='2030-01-01T00:00:00',
                status='OPEN',
                observers=[],
                performers=[],
            )
        ).model_dump_json(),
        status.HTTP_200_OK,
        does_not_raise(),
    ),
    
    # Удаление задачи повторно
    (
        {'task_id': str(FAKE_TASKS[3].id)},
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: task_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
    
    # Удаление чужой задачи
    (
        {'task_id': str(FAKE_TASKS[0].id)},
        BaseResponseModel(
            status_code=status.HTTP_400_BAD_REQUEST,
            error=True,
            message='Неверный параметр: task_id.'
        ).model_dump_json(),
        status.HTTP_400_BAD_REQUEST,
        does_not_raise(),
    ),
]
