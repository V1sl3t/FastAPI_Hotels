async def test_get_hotels(ac):
    response = await ac.get("/comforts")
    print(f"{response.json()=}")
    assert response.status_code == 200