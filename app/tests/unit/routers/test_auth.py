import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from enums import EndpointPath
from models.v1.user import UserModel
from tests.assertions import Assertions
from tests.data_test_generator import AuthDataGen

pytestmark = pytest.mark.asyncio

def get_user_model():
    return UserModel

@pytest.mark.anyio
class TestAuth:
    BASE_ENDPOINT = "/v1/auth"

    async def create_user(self, async_client: AsyncClient, test_data: AuthDataGen):
        response = await async_client.post(f"{self.BASE_ENDPOINT}{EndpointPath.REGISTER.value}", json=test_data)
        return response

    async def test_register(self, async_db_connection: AsyncConnection, async_client: AsyncClient) -> None:
        test_data = AuthDataGen()
        response = await self.create_user(async_client=async_client, test_data=test_data.get_data())
        Assertions.assert_are_equal(status.HTTP_201_CREATED, response.status_code)
        query = select(get_user_model()).filter_by(email=test_data.email)
        coroutine_result = await async_db_connection.execute(query)
        result = coroutine_result.first()
        Assertions.assert_are_equal(test_data.email, result.email)

    async def test_login(self, async_client: AsyncClient) -> None:
        test_data = AuthDataGen()
        await self.create_user(test_data=test_data.get_data(), async_client=async_client)
        response = await async_client.post(f"{self.BASE_ENDPOINT}{EndpointPath.LOGIN.value}", json=test_data.get_data())
        Assertions.assert_are_equal(response.status_code, status.HTTP_200_OK)
        Assertions.assert_is_not_none(response.json())
