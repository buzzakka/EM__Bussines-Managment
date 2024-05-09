from fastapi.testclient import TestClient
from fastapi import Response, status
import pytest

from tests.fakes.parameters.company import (
    TEST_ENDPOINT_ADD_NEW_MEMBER,
    TEST_ENDPOINT_UPDATE_USERS_EMAIL,
    TEST_ENDPOINT_UPDATE_USERS_NAME,
    TEST_ENDPOINT_ADD_POSITION,
    TEST_ENDPOINT_UPDATE_POSITION,
    TEST_ENDPOINT_DELETE_POSITION,
)
import json

class TestCompanyRouterV1:
    
    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_ADD_NEW_MEMBER
    )
    def test_add_new_member(
        self,
        client: TestClient,
        get_account_jwt,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.post(
                '/api/v1/company/member/',
                json=data,
                headers={'Authorization': get_account_jwt}
            )
            assert response.status_code == expected_status
            assert response.json() == expected_result

    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_UPDATE_USERS_EMAIL
    )
    def test_update_users_email(
        self,
        client: TestClient,
        get_account_jwt,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.patch(
                '/api/v1/company/member/email/',
                data=data,
                headers={'Authorization': get_account_jwt}
            )
            assert response.status_code == expected_status
            assert response.json() == json.loads(expected_result)


    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_UPDATE_USERS_NAME
    )
    def test_update_users_name(
        self,
        client: TestClient,
        get_account_jwt,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.patch(
                '/api/v1/company/member/name',
                data=data,
                headers={'Authorization': get_account_jwt}
            )
            assert response.status_code == expected_status
            assert response.json() == json.loads(expected_result)

    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_ADD_POSITION
    )
    def test_add_position(
        self,
        client: TestClient,
        get_account_jwt,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.post(
                '/api/v1/company/position/',
                data=data,
                headers={'Authorization': get_account_jwt}
            )
            assert response.status_code == expected_status

            payload: dict = response.json()['payload']
            assert payload['title'] == expected_result.payload.title
            assert payload['description'] == expected_result.payload.description


    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_UPDATE_POSITION
    )
    def test_update_position(
        self,
        client: TestClient,
        get_account_jwt,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.patch(
                '/api/v1/company/position/',
                data=data,
                headers={'Authorization': get_account_jwt}
            )
            assert response.status_code == expected_status
            assert response.json() == json.loads(expected_result)


    @pytest.mark.parametrize(
        'data, expected_result, expected_status, expectation',
        TEST_ENDPOINT_DELETE_POSITION
    )
    def test_delete_position(
        self,
        client: TestClient,
        get_account_jwt,
        data, expected_result, expected_status, expectation,
    ):
        with expectation:
            response: Response = client.delete(
                '/api/v1/company/position/',
                params=data,
                headers={'Authorization': get_account_jwt}
            )
            assert response.status_code == expected_status
            assert response.json() == json.loads(expected_result)
