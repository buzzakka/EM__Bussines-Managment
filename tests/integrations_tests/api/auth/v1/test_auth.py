from fastapi.testclient import TestClient
from fastapi import Response, status
import pytest

from tests.fakes.parameters.auth import (
    TEST_ENDPOINT_CHECK_ACCOUNT,
    TEST_ENDPOINT_SIGN_UP_COMPANY,
    TEST_ENDPOINT_SIGN_UP_COMPLETE_COMPANY,
    TEST_ENDPOINT_CONFIRM_EMPLOYEE_ACCOUNT,
    TEST_ENDPOINT_SIGN_UP_COMPLETE_EMPLOYEE,
    TEST_ENDPOINT_INVALID_TOKEN,
)


class TestAuthRouterV1:

    @pytest.mark.parametrize(
        'email, expected_result, expected_status, expectation',
        TEST_ENDPOINT_CHECK_ACCOUNT
    )
    def test_check_account(
        self,
        client: TestClient,
        email, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.get(
                f'/api/v1/auth/check_account/{email}',
            )
            assert response.status_code == expected_status
            assert response.json() == expected_result

    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_SIGN_UP_COMPANY
    )
    def test_sign_up_company(
        self,
        client: TestClient,
        data, expected_result, expected_status, expectation
    ):
        with expectation:
            response: Response = client.post(
                '/api/v1/auth/sign-up',
                json=data
            )
            assert response.status_code == expected_status
            assert response.json() == expected_result

    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_SIGN_UP_COMPLETE_COMPANY
    )
    def test_sign_up_complete_account(
        self,
        client: TestClient,
        data, expected_result, expected_status, expectation
    ):
        with expectation:
            response: Response = client.post(
                '/api/v1/auth/sign-up-complete/',
                json=data
            )
            assert response.status_code == expected_status
            assert response.json() == expected_result

    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_SIGN_UP_COMPLETE_EMPLOYEE
    )
    def test_sign_up_complete_employee(
        self,
        client: TestClient,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.post(
                '/api/v1/auth/sign-up-employee/',
                json=data
            )
            assert response.status_code == expected_status
            assert response.json() == expected_result

    @pytest.mark.parametrize(
        'email, token, expected_result, expected_status, expectation',
        TEST_ENDPOINT_CONFIRM_EMPLOYEE_ACCOUNT
    )
    def test_sign_up_employee(
        self,
        client: TestClient,
        email, token, expected_result, expected_status, expectation
    ):
        with expectation:
            response: Response = client.get(
                '/api/v1/auth/sign-up-employee/',
                params={'email': email, 'invite_token': token}
            )
            assert response.status_code == expected_status
            assert response.json() == expected_result

    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_INVALID_TOKEN
    )
    def test_invalid_login(
        self,
        client: TestClient,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.post(
                '/api/v1/auth/login/',
                json=data
            )
            assert response.status_code == expected_status
            assert response.json() == expected_result

    def test_login_and_logout(self, client: TestClient):
        response: Response = client.post(
            '/api/v1/auth/login/',
            json={'email': 'user_2@example.com', 'password': 'password'}
        )
        payload: dict = response.json()['payload']
        access_token: str = payload['access_token']
        token_type: str = payload['token_type']

        response: Response = client.post(
            '/api/v1/auth/logout/'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response: Response = client.post(
            '/api/v1/auth/logout/',
            headers={'Authorization': f'{token_type} {access_token}'}
        )
        assert response.status_code == status.HTTP_200_OK
