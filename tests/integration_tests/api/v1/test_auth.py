from fastapi import Response, status
from fastapi.testclient import TestClient
import pytest

from tests.fakes.parameters.auth import (
    TEST_ENDPOINT_CHECK_ACCOUNT,
    TEST_ENDPOINT_SIGN_UP,
    TEST_ENDPOINT_SIGN_UP_COMPLETE,
)


class TestAuthRouterV1:
    
    @pytest.mark.parametrize(
        "email, expected_result, expected_status, expectation",
        TEST_ENDPOINT_CHECK_ACCOUNT
    )
    def test_check_account(
        self,
        client: TestClient,
        email, expected_result, expected_status, expectation
    ):
        with expectation:
            response: Response = client.get(
                f'/api/v1/auth/check_account/{email}',
            )
            
            assert response.status_code == expected_status
            
            assert response.json() == expected_result

    @pytest.mark.parametrize(
        "data, expected_result, expected_status, expectation",
        TEST_ENDPOINT_SIGN_UP
    )
    def test_sign_up(
        self,
        client: TestClient,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.post(
                '/api/v1/auth/sign-up/',
                data=data
            )
            
            assert response.status_code == expected_status
            
            assert response.json() == expected_result
    
    @pytest.mark.parametrize(
        "data, expected_result, expected_status, expectation",
        TEST_ENDPOINT_SIGN_UP_COMPLETE
    )
    def test_sign_up_complete(
        self,
        client: TestClient,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.post(
                '/api/v1/auth/sign-up-complete/',
                data=data
            )
            
            assert response.status_code == expected_status
            
            assert response.json() == expected_result
