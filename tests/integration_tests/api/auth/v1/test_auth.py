from fastapi import Response, status
from fastapi.testclient import TestClient
import pytest

from src.api.auth.schemas import UserLoginSchema

from tests.fakes.parameters.auth import (
    TEST_ENDPOINT_CHECK_ACCOUNT,
    # TEST_ENDPOINT_SIGN_UP,
    # TEST_ENDPOINT_SIGN_UP_COMPLETE,
)


class TestAuthRouterV1:
    
    def test_main(self):
        assert 1 == 1

    # @pytest.mark.parametrize(
    #     "email, expected_result, expected_status, expectation",
    #     TEST_ENDPOINT_CHECK_ACCOUNT
    # )
    # def test_check_account(
    #     self,
    #     client: TestClient,
    #     email, expected_result, expected_status, expectation
    # ):
    #     with expectation:
    #         response: Response = client.get(
    #             f'/api/v1/auth/check_account/{email}',
    #         )

    #         assert response.status_code == expected_status

    #         assert response.json() == expected_result

    # @pytest.mark.parametrize(
    #     "data, expected_result, expected_status, expectation",
    #     TEST_ENDPOINT_SIGN_UP
    # )
    # def test_sign_up(
    #     self,
    #     client: TestClient,
    #     data, expected_result, expected_status, expectation,
    # ):
    #     with expectation:
    #         response: Response = client.post(
    #             '/api/v1/auth/sign-up/',
    #             data=data
    #         )

    #         assert response.status_code == expected_status

    #         assert response.json() == expected_result

    # @pytest.mark.parametrize(
    #     "data, expected_result, expected_status, expectation",
    #     TEST_ENDPOINT_SIGN_UP_COMPLETE
    # )
    # def test_sign_up_complete(
    #     self,
    #     client: TestClient,
    #     data, expected_result, expected_status, expectation,
    # ):
    #     with expectation:
    #         response: Response = client.post(
    #             '/api/v1/auth/sign-up-complete/',
    #             data=data
    #         )

    #         assert response.status_code == expected_status

    #         assert response.json() == expected_result

    # def test_login_and_logout(
    #     self,
    #     client: TestClient,
    # ):
    #     # Попытка получить доступ к странице, к которой могут получить доступ
    #     # только авторизованные пользователи без jwt токена
    #     response: Response = client.post(url='/api/v1/auth/logout/')

    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    #     # Аутентификация пользователя
    #     response: Response = client.post(
    #         url='/api/v1/auth/login/',
    #         data=UserLoginSchema(email='user_2@example.com',
    #                              password='string').model_dump_json()
    #     )

    #     token_type: str = response.json()['token_type']
    #     access_token: str = response.json()['access_token']
    #     token: str = f'{token_type} {access_token}'

    #     # Попытка разлогиниться с jwt токеном
    #     response: Response = client.post(
    #         url='/api/v1/auth/logout/',
    #         headers={'Authorization': token}
    #     )

    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.json() == None

    #     # Попытка разлогиниться с удаленным jwt токеном
    #     response: Response = client.post(
    #         url='/api/v1/auth/logout/',
    #         headers={'Authorization': token}
    #     )

    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED
