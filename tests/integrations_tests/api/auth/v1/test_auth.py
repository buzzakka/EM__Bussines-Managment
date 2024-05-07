from fastapi.testclient import TestClient
from fastapi import Response, status
import pytest

from tests.fakes.parameters.auth import (
    TEST_ENDPOINT_CHECK_ACCOUNT,
    TEST_ENDPOINT_SIGN_UP_COMPANY,
)


class TestAuthRouterV1:
    
    @pytest.mark.parametrize(
        "email, expected_result, expected_status, expectation",
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
        "data, expected_result, expected_status, expectation",
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
