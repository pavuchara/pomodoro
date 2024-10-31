import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
async def anonymous_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost/"
    ) as ac:
        yield ac
