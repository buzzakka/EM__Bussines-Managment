from fastapi import status

from src.core.schemas import BaseResponseModel


def invalid_account_id(account_id: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Неверный account_id {account_id}.'
    )


def invalid_position_id(position_id: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Неверный position_id {position_id}.'
    )


def invalid_struct_id(struct_id: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Неверный id структуры: {struct_id}'
    )


def invalid_member_id(member_id: str):
    return BaseResponseModel(
        status_code=status.HTTP_400_BAD_REQUEST,
        error=True,
        message=f'Неверный member_id: {member_id}'
    )
