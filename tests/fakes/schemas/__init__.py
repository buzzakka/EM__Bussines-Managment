__all__ = [
    'InviteTestSchema',
    'AccountTestSchema',
    'UserTestSchema',
    'SecretTestSchema',
    'CompanySchema',

    'MemberTestSchema',
    'CompanyTestSchema',
]


from tests.fakes.schemas.auth import (
    InviteTestSchema,
    AccountTestSchema,
    UserTestSchema,
    SecretTestSchema,
)

from tests.fakes.schemas.company import (
    MemberTestSchema,
    CompanyTestSchema
)
