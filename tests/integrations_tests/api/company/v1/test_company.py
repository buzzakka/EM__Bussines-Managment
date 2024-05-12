from fastapi.testclient import TestClient
from fastapi import Response, status

from uuid import UUID
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


def is_valid_uuid(uuid_to_test: str):
    try:
        uuid_obj = UUID(uuid_to_test, version=4)
        return str(uuid_obj) == str(uuid_to_test)
    except ValueError:
        return False


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
            response_data: dict = response.json()

            if response.status_code == status.HTTP_200_OK:
                payload: dict = response_data['payload']
                for elem in ['id', 'account_id', 'company_id']:
                    assert elem in payload
                    assert is_valid_uuid(payload[elem])
            else:
                assert response_data == json.loads(expected_result)

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

            response_data: dict = response.json()

            payload: dict = response_data['payload']

            assert 'id' in payload
            assert is_valid_uuid(payload['id'])
            assert payload['title'] == expected_result['title']
            assert payload['description'] == expected_result['description']


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
