__all__ = [
    'CompanyRepository',
    'MemberRepository',
    'PositionRepository',
    'StructAdmRepository',
    'TaskRepository',
    'StructAdmPositionRepository',
]

from src.api.company.v1.repositories.company import CompanyRepository
from src.api.company.v1.repositories.member import MemberRepository
from src.api.company.v1.repositories.position import PositionRepository
from src.api.company.v1.repositories.struct_adm import StructAdmRepository
from src.api.company.v1.repositories.task import TaskRepository
from src.api.company.v1.repositories.struct_adm_position import StructAdmPositionRepository
