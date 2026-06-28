from fastapi.testclient import TestClient

def test_todo_crud_and_isolation_flow(client: TestClient):
    # 1. Register User 1 and User 2
    client.post("/users/register", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123"
    })
    client.post("/users/register", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "password456"
    })
    
    # 2. Login as User 1 and User 2 to get tokens
    login1 = client.post("/auth/login", data={"username": "user1@example.com", "password": "password123"})
    token1 = login1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    
    login2 = client.post("/auth/login", data={"username": "user2@example.com", "password": "password456"})
    token2 = login2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    # 3. Create a Todo for User 1
    create_payload = {
        "title": "E2E Todo Item",
        "completed": False
    }
    create_resp = client.post("/todos", json=create_payload, headers=headers1)
    assert create_resp.status_code == 201
    todo = create_resp.json()
    assert todo["title"] == "E2E Todo Item"
    assert todo["completed"] is False
    assert "id" in todo
    todo_id = todo["id"]
    
    # 4. List Todos for User 1
    list1_resp = client.get("/todos", headers=headers1)
    assert list1_resp.status_code == 200
    todos1 = list1_resp.json()
    assert len(todos1) == 1
    assert todos1[0]["id"] == todo_id
    
    # 5. List Todos for User 2 (should be empty, verifying isolation)
    list2_resp = client.get("/todos", headers=headers2)
    assert list2_resp.status_code == 200
    todos2 = list2_resp.json()
    assert len(todos2) == 0
    
    # 6. Try to read User 1's Todo using User 2's token (should return 403 Forbidden)
    get_unauth_resp = client.get(f"/todos/{todo_id}", headers=headers2)
    assert get_unauth_resp.status_code == 403
    
    # 7. Try to update User 1's Todo using User 2's token (should return 403 Forbidden)
    update_payload = {"completed": True}
    update_unauth_resp = client.put(f"/todos/{todo_id}", json=update_payload, headers=headers2)
    assert update_unauth_resp.status_code == 403
    
    # 8. Update User 1's Todo using User 1's token (should succeed)
    update_auth_resp = client.put(f"/todos/{todo_id}", json=update_payload, headers=headers1)
    assert update_auth_resp.status_code == 200
    updated_todo = update_auth_resp.json()
    assert updated_todo["completed"] is True
    
    # 9. Delete User 1's Todo using User 2's token (should return 403 Forbidden)
    delete_unauth_resp = client.delete(f"/todos/{todo_id}", headers=headers2)
    assert delete_unauth_resp.status_code == 403
    
    # 10. Delete User 1's Todo using User 1's token (should succeed)
    delete_auth_resp = client.delete(f"/todos/{todo_id}", headers=headers1)
    assert delete_auth_resp.status_code == 204
    
    # 11. Verify Todo is deleted for User 1
    list1_after_resp = client.get("/todos", headers=headers1)
    assert len(list1_after_resp.json()) == 0

def test_unauthorized_access(client: TestClient):
    # Try accessing endpoints without credentials (should return 401 Unauthorized)
    assert client.get("/todos").status_code == 401
    assert client.post("/todos", json={"title": "Unauthorized", "completed": False}).status_code == 401
    assert client.get("/todos/1").status_code == 401
    assert client.put("/todos/1", json={"completed": True}).status_code == 401
    assert client.delete("/todos/1").status_code == 401
