import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from app.enums import EndpointPath
from app.models.v1.user import UserModel
from app.tests.assertions import Assertions
from app.tests.data_test_generator import AuthDataGen

pytestmark = pytest.mark.asyncio

def get_user_model():
    return UserModel

@pytest.mark.anyio
class TestUserCheck:
    BASE_AUTH_ENDPOINT = "/v1/auth"
    BASE_USERS_ENDPOINT = "/v1/user"
    USER_ID = 1

    async def create_user_and_auth(self, async_client: AsyncClient, test_data: AuthDataGen):
        await async_client.post(f"{self.BASE_AUTH_ENDPOINT}{EndpointPath.REGISTER.value}", json=test_data)
        response = await async_client.post(f"{self.BASE_AUTH_ENDPOINT}{EndpointPath.LOGIN.value}", json=test_data)
        return response

    @pytest.mark.parametrize(
        "endpoint",
        [
            f"{BASE_USERS_ENDPOINT}{EndpointPath.GET_ALL_USERS.value}",
            f"{BASE_USERS_ENDPOINT}{EndpointPath.GET_USER.value.format(user_id=1)}",
            f"{BASE_USERS_ENDPOINT}{EndpointPath.GET_ACTIVE_USERS.value.format(user_id=1)}",
        ]
    )
    async def test_get_all_users(self, async_client: AsyncClient, endpoint) -> None:
        test_data = AuthDataGen()
        response = await self.create_user_and_auth(async_client=async_client, test_data=test_data.get_data())
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = await async_client.get(url=endpoint, headers=headers)
        Assertions.assert_are_equal(expected_result=status.HTTP_200_OK, actual_result=response.status_code)
        data = response.json()
        if not isinstance(data, dict):
            data = response.json()[0]

        Assertions.assert_is_not_none(data=data)
        Assertions.assert_are_equal(expected_result=test_data.email, actual_result=data.get("email"))

    async def test_deactivate_user(self, async_client: AsyncClient, async_db_connection: AsyncConnection) -> None:
        test_data = AuthDataGen()
        expected_is_active_after_deactivate = 0
        expected_is_active_before_deactivate = 1
        login_response = await self.create_user_and_auth(async_client=async_client, test_data=test_data.get_data())
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        user_before_deactivate = await async_client.get(
            url=f"{self.BASE_USERS_ENDPOINT}{EndpointPath.GET_USER.value.format(user_id=self.USER_ID)}", headers=headers)
        Assertions.assert_are_equal(expected_result=user_before_deactivate.json()["is_active"],
                                    actual_result=expected_is_active_before_deactivate)
        user_after_deactivate = await async_client.put(
            url=f"{self.BASE_USERS_ENDPOINT}{EndpointPath.DEACTIVATE_USER.value.format(user_id=self.USER_ID)}", headers=headers)
        Assertions.assert_are_equal(expected_result=user_after_deactivate.json()["is_active"],
                                    actual_result=expected_is_active_after_deactivate)
        query = select(get_user_model()).filter_by(email=test_data.email)
        coroutine_result = await async_db_connection.execute(query)
        result = coroutine_result.first()
        Assertions.assert_are_equal(expected_result=result.is_active, actual_result=expected_is_active_after_deactivate)

    async def test_change_person_type(self, async_client: AsyncClient, async_db_connection: AsyncConnection) -> None:
        test_data = AuthDataGen()
        expected_person_type = "admin"
        login_response = await self.create_user_and_auth(async_client=async_client, test_data=test_data.get_data())
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        user_before_deactivate = await async_client.get(
            url=f"{self.BASE_USERS_ENDPOINT}{EndpointPath.GET_USER.value.format(user_id=self.USER_ID)}", headers=headers)
        Assertions.assert_are_equal(expected_result=user_before_deactivate.json()["is_active"], actual_result=1)
        user_after_deactivate = await async_client.post(
            url=f"{self.BASE_USERS_ENDPOINT}{EndpointPath.CHANGE_PERSON_TYPE.value}",
            headers=headers,
            json={"id": self.USER_ID, "person_type": expected_person_type})
        Assertions.assert_are_equal(expected_result=user_after_deactivate.json()["person_type"],
                                    actual_result=expected_person_type)
        query = select(get_user_model()).filter_by(email=test_data.email)
        coroutine_result = await async_db_connection.execute(query)
        result = coroutine_result.first()
        Assertions.assert_are_equal(expected_result=result.person_type, actual_result=expected_person_type)
