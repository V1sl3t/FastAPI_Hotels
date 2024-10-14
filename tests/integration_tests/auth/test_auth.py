import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [("ggdd@qwe.com", "1234", 200), ("ggdd@qwe.com", "1235", 409), ("gg2@qwe.com", "1234", 200)],
)
async def test_auth(email: str, password: str, status_code: int, ac):
    # /register
    resp_register = await ac.post("/auth/register", json={"email": email, "password": password})
    assert resp_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    resp_login = await ac.post("/auth/login", json={"email": email, "password": password})
    assert resp_login.status_code == 200
    assert ac.cookies["access_token"]
    assert "access_token" in resp_login.json()

    # /me
    resp_me = await ac.get("/auth/me")
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user
    await ac.post("/auth/logout")

    # /logout
    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == 200
    assert "access_token" not in ac.cookies
    resp_me_after_logout = await ac.get("/auth/me")
    assert resp_me_after_logout.status_code != 200
