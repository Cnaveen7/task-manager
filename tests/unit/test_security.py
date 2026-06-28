from app.core.security import hash_password, verify_password

def test_hash_password_generates_different_string():
    password = "mysecurepassword"
    hashed = hash_password(password)
    assert hashed != password
    assert len(hashed) > 0

def test_verify_password_correct():
    password = "mysecurepassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    password = "mysecurepassword"
    hashed = hash_password(password)
    assert verify_password("wrongpassword", hashed) is False
