from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel

from database import engine
from main import app


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db() -> AsyncGenerator[None, None]:
    """
    Resets the test database schema before running each test function.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


@pytest.mark.asyncio
async def test_create_and_read_item() -> None:
    """
    Tests creating an item via POST /items/ and retrieving it via GET /items/{id}.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        data = {"title": "Test Item", "price": 10.5, "owner_id": 1}
        resp = await client.post("/items/", json=data)
        assert resp.status_code == 201
        created = resp.json()
        assert created["title"] == "Test Item"
        assert created["owner_id"] == 1

        get_resp = await client.get(f"/items/{created['id']}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == created["id"]


@pytest.mark.asyncio
async def test_filter_by_owner_and_search() -> None:
    """
    Tests filtering items by owner_id and searching items by title substring.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/items/", json={"title": "Laptop", "price": 1000.0, "owner_id": 10})
        await client.post("/items/", json={"title": "Phone", "price": 500.0, "owner_id": 20})

        resp = await client.get("/items/?owner_id=10")
        assert resp.status_code == 200
        items = resp.json()
        assert len(items) == 1
        assert items[0]["owner_id"] == 10

        search_resp = await client.get("/items/?title=Lap")
        assert search_resp.status_code == 200
        search_items = search_resp.json()
        assert len(search_items) == 1
        assert search_items[0]["title"] == "Laptop"


@pytest.mark.asyncio
async def test_pagination_and_sorting() -> None:
    """
    Tests sorting items by field (sort_by) and applying pagination (skip, limit).
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/items/", json={"title": "Banana", "price": 30.0, "owner_id": 1})
        await client.post("/items/", json={"title": "Apple", "price": 10.0, "owner_id": 1})
        await client.post("/items/", json={"title": "Cherry", "price": 20.0, "owner_id": 1})

        sort_resp = await client.get("/items/?sort_by=price")
        assert sort_resp.status_code == 200
        sorted_items = sort_resp.json()
        assert len(sorted_items) == 3
        assert sorted_items[0]["title"] == "Apple"
        assert sorted_items[1]["title"] == "Cherry"
        assert sorted_items[2]["title"] == "Banana"

        page_resp = await client.get("/items/?skip=1&limit=1")
        assert page_resp.status_code == 200
        paged_items = page_resp.json()
        assert len(paged_items) == 1


@pytest.mark.asyncio
async def test_owner_update_permissions() -> None:
    """
    Tests that item update (PUT) is allowed for owner and forbidden (403) for non-owner.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/items/", json={"title": "Bike", "price": 200.0, "owner_id": 5})
        item_id = create_resp.json()["id"]

        forbidden_resp = await client.put(f"/items/{item_id}?owner_id=99", json={"title": "Hacked Bike"})
        assert forbidden_resp.status_code == 403

        ok_resp = await client.put(f"/items/{item_id}?owner_id=5", json={"title": "New Bike"})
        assert ok_resp.status_code == 200
        assert ok_resp.json()["title"] == "New Bike"


@pytest.mark.asyncio
async def test_owner_delete_permissions() -> None:
    """
    Tests that item deletion (DELETE) is allowed for owner and forbidden (403) for non-owner.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/items/", json={"title": "Car", "price": 5000.0, "owner_id": 7})
        item_id = create_resp.json()["id"]

        forbidden_resp = await client.delete(f"/items/{item_id}?owner_id=99")
        assert forbidden_resp.status_code == 403

        ok_resp = await client.delete(f"/items/{item_id}?owner_id=7")
        assert ok_resp.status_code == 204
