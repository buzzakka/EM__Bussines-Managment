from uuid import uuid4

from tests.fakes.schemas import (
    CompanySchema,
    MemberSchema,
    PositionSchema,
    StructSchema,
    StructPositionSchema,
)
from tests.fakes.database.fake_auth import FAKE_ACCOUNTS


FAKE_COMPANYS = [
    CompanySchema(
        id=uuid4(),
        name='user_1@example.com company'
    ),
    CompanySchema(
        id=uuid4(),
        name='user_2@example.com company'
    )
]


FAKE_MEMBERS = [
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[0].id,
        company_id=FAKE_COMPANYS[0].id,
        is_admin=True
    ),
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[2].id,
        company_id=FAKE_COMPANYS[0].id,
        is_admin=False
    ),
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[1].id,
        company_id=FAKE_COMPANYS[1].id,
        is_admin=True
    ),
    MemberSchema(
        id=uuid4(),
        account_id=FAKE_ACCOUNTS[3].id,
        company_id=FAKE_COMPANYS[1].id,
        is_admin=False
    ),
]


FAKE_POSITIONS = [
    PositionSchema(
        id=uuid4(),
        title='company_1 position',
        company_id=FAKE_COMPANYS[0].id
    ),
    PositionSchema(
        id=uuid4(),
        title='company_2 position',
        company_id=FAKE_COMPANYS[1].id
    ),
    PositionSchema(
        id=uuid4(),
        title='position for update',
        company_id=FAKE_COMPANYS[1].id
    ),
    PositionSchema(
        id=uuid4(),
        title='position for delete',
        company_id=FAKE_COMPANYS[1].id
    ),
]

FAKE_STRUCT = [
    StructSchema(
        id=uuid4(),
        company_id=FAKE_COMPANYS[0].id,
        name='user_1@example.com struct'
    ),
    StructSchema(
        id=uuid4(),
        company_id=FAKE_COMPANYS[1].id,
        name='user_2@example.com struct'
    ),
    StructSchema(
        id='7db26b2a-11cb-4330-94c2-ae7759611906',
        company_id=FAKE_COMPANYS[1].id,
        name='struct for update',
        path='7db26b2a_11cb_4330_94c2_ae7759611906'
    ),
    StructSchema(
        id='7db26b2a-11cb-4330-94c2-ae7759611901',
        company_id=FAKE_COMPANYS[1].id,
        name='struct for delete',
        path='7db26b2a_11cb_4330_94c2_ae7759611901'
    ),
]

FAKE_STRUCT_POSITION = [
    # Позиция в структуре пользователя user_2@example.com
    StructPositionSchema(
        id=uuid4(),
        struct_id=FAKE_STRUCT[2].id,
        position_id=FAKE_POSITIONS[1].id,
        member_id=FAKE_MEMBERS[2].id,
        is_director=True
    ),

    # Позиция в структуре пользователя user_1@example.com
    StructPositionSchema(
        id=uuid4(),
        struct_id=FAKE_STRUCT[0].id,
        position_id=FAKE_POSITIONS[0].id,
        member_id=FAKE_MEMBERS[0].id,
        is_director=True
    ),

    # Позиция в структуре для изменения и удаления
    StructPositionSchema(
        id=uuid4(),
        struct_id=FAKE_STRUCT[1].id,
        position_id=FAKE_POSITIONS[1].id,
        member_id=FAKE_MEMBERS[3].id,
        is_director=False
    ),
]
