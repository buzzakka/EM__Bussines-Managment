from fastapi.testclient import TestClient
from fastapi import Response, status
import pytest

from tests.fakes.parameters.auth import TEST_ENDPOINT_CHECK_ACCOUNT


class TestAuthRouterV1:
    
    @pytest.mark.parametrize(
        "email, expected_result, expected_status, expectation",
        TEST_ENDPOINT_CHECK_ACCOUNT
    )
    def test_check_account(
        self,
        fill_db,
        client: TestClient,
        email, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.get(
                f'/api/v1/auth/check_account/{email}',
            )

            assert response.status_code == expected_status

            assert response.json() == expected_result
