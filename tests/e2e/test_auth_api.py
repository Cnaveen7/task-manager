from fastapi.testclient import TestClient

def test_user_registration_and_login_flow(client: TestClient):
    # 1. Register a user
    register_payload = {
        "username": "e2euser",
        "email": "e2e@example.com",
        "password": "e2epassword"
    }
    register_response = client.post("/users/register", json=register_payload)
    assert register_response.status_code == 200
    data = register_response.json()
    assert data["username"] == "e2euser"
    assert data["email"] == "e2e@example.com"
    assert "id" in data
    
    # 2. Try to register with the same email
    dup_response = client.post("/users/register", json=register_payload)
    assert dup_response.status_code == 400
    assert dup_response.json()["detail"] == "User with this email already exists"
    
    # 3. Login with correct credentials
    login_payload = {
        "username": "e2e@example.com", # OAuth2 Form username maps to email
        "password": "e2epassword"
    }
    login_response = client.post("/auth/login", data=login_payload)
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert token_data["token_type"] == "bearer"
    assert "access_token" in token_data

def test_login_incorrect_credentials(client: TestClient):
    # Try to login with non-existent user
    login_payload = {
        "username": "nonexistent@example.com",
        "password": "somepassword"
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
