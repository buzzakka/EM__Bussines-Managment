from fastapi import HTTPException, status


def bad_param(param_name: str):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Неверный параметр: {param_name}.'
    )
