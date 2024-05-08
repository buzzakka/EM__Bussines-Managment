import pytest
from fastapi.testclient import TestClient
from fastapi import Response


@pytest.fixture(scope='session')
async def get_account_jwt(setup_db, client: TestClient) -> str:
    response: Response = client.post(
        url='/api/v1/auth/login/',
        json={'email': 'user_2@example.com', 'password': 'password'}
    )
    payload: dict = response.json()['payload']
    token_type: str = payload['token_type']
    access_token: str = payload['access_token']
    token: str = f'{token_type} {access_token}'
    
    return token