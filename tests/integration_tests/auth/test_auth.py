import pytest


@pytest.mark.parametrize("email, password", [
    ("ggdd@qwe.com", "1234"),
    ("gg1@qwe.com", "1235"),
    ("gg2@qwe.com", "1234")
])
async def test_auth(
        email, password,
        ac
):
    await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    response = await ac.get("/auth/me")
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["email"] == email
    await ac.post("/auth/logout")
    response_after_logout = await ac.get("/auth/me")
    assert response_after_logout.status_code != 200



