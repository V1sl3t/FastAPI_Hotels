from httpx import AsyncClient


async def test_get_hotels(ac: AsyncClient):
    response = await ac.get("/comforts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_hotels(ac: AsyncClient):
    comfort_title = "TV"
    response = await ac.post("/comforts", json={"title": comfort_title})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res
    assert res["data"]["title"] == comfort_title
