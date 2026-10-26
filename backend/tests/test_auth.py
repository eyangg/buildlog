def signup(client, email="user@example.com", nickname="닉네임", password="password1"):
    return client.post(
        "/api/auth/signup",
        json={"email": email, "password": password, "nickname": nickname},
    )


def login(client, email="user@example.com", password="password1"):
    return client.post("/api/auth/login", json={"email": email, "password": password})


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_signup_creates_user_without_returning_password(client):
    response = signup(client)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "user@example.com"
    assert body["nickname"] == "닉네임"
    assert "password" not in body and "password_hash" not in body


def test_signup_trims_email_and_nickname(client):
    response = client.post(
        "/api/auth/signup",
        json={"email": "  Mixed@Example.com ", "password": "password1", "nickname": "  nick_1  "},
    )

    assert response.status_code == 201
    assert response.json()["email"] == "mixed@example.com"
    assert response.json()["nickname"] == "nick_1"


def test_signup_rejects_duplicate_email_and_nickname(client):
    signup(client)

    dup_email = signup(client, nickname="다른닉")
    assert dup_email.status_code == 409
    assert dup_email.json()["detail"] == "이미 사용 중인 이메일입니다."

    dup_nick = signup(client, email="other@example.com")
    assert dup_nick.status_code == 409
    assert dup_nick.json()["detail"] == "이미 사용 중인 닉네임입니다."


def test_signup_rejects_invalid_email(client):
    response = signup(client, email="not-an-email")
    assert response.status_code == 422


def test_password_length_boundaries(client):
    assert signup(client, email="a1@example.com", nickname="aa", password="1234567").status_code == 422
    assert signup(client, email="a2@example.com", nickname="bb", password="1" * 65).status_code == 422
    assert signup(client, email="a3@example.com", nickname="cc", password="1" * 8).status_code == 201
    assert signup(client, email="a4@example.com", nickname="dd", password="1" * 64).status_code == 201


def test_nickname_length_and_characters(client):
    assert signup(client, email="n1@example.com", nickname="a").status_code == 422
    assert signup(client, email="n2@example.com", nickname="a" * 21).status_code == 422
    assert signup(client, email="n3@example.com", nickname="a-b").status_code == 422
    assert signup(client, email="n4@example.com", nickname="aa").status_code == 201
    assert signup(client, email="n5@example.com", nickname="a" * 20).status_code == 201


def test_login_returns_token_and_rejects_wrong_credentials(client):
    signup(client)

    ok = login(client)
    assert ok.status_code == 200
    assert ok.json()["token_type"] == "bearer"
    assert ok.json()["access_token"]

    wrong = login(client, password="wrong-password")
    assert wrong.status_code == 401
    assert wrong.json()["detail"] == "이메일 또는 비밀번호가 맞지 않습니다."

    unknown = login(client, email="nobody@example.com")
    assert unknown.status_code == 401


def test_account_info_requires_valid_token(client):
    signup(client)
    token = login(client).json()["access_token"]

    no_token = client.get("/api/account/info")
    assert no_token.status_code == 401

    bad_token = client.get("/api/account/info", headers=auth_header("broken.token.value"))
    assert bad_token.status_code == 401

    ok = client.get("/api/account/info", headers=auth_header(token))
    assert ok.status_code == 200
    assert ok.json()["email"] == "user@example.com"


def test_logout_requires_token(client):
    signup(client)
    token = login(client).json()["access_token"]

    assert client.post("/api/auth/logout").status_code == 401
    response = client.post("/api/auth/logout", headers=auth_header(token))
    assert response.status_code == 200


def test_nickname_change_issues_new_token_and_updates_nickname(client):
    signup(client)
    token = login(client).json()["access_token"]

    response = client.put(
        "/api/account/nickname",
        json={"nickname": "  새닉네임  "},
        headers=auth_header(token),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["nickname"] == "새닉네임"
    assert body["access_token"]
    info = client.get("/api/account/info", headers=auth_header(body["access_token"]))
    assert info.json()["nickname"] == "새닉네임"


def test_nickname_change_rejects_taken_nickname_and_keeps_old_one(client):
    signup(client, email="first@example.com", nickname="첫번째")
    signup(client, email="second@example.com", nickname="두번째")
    token = login(client, email="second@example.com").json()["access_token"]

    response = client.put("/api/account/nickname", json={"nickname": "첫번째"}, headers=auth_header(token))

    assert response.status_code == 409
    info = client.get("/api/account/info", headers=auth_header(token))
    assert info.json()["nickname"] == "두번째"


def test_nickname_change_validates_rules(client):
    signup(client)
    token = login(client).json()["access_token"]

    response = client.put("/api/account/nickname", json={"nickname": "x"}, headers=auth_header(token))
    assert response.status_code == 422

    blank = client.put("/api/account/nickname", json={"nickname": "   "}, headers=auth_header(token))
    assert blank.status_code == 422
