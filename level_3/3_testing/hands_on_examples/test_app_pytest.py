import pytest
from app import divide, UserManager

# 1. Basic Test & Assertion
def test_divide_success():
    assert divide(10, 2) == 5

# 2. Testing Exceptions
def test_divide_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# 3. Parametrization (Data Driven Tests)
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (9, 3, 3),
    (100, 10, 10),
])
def test_divide_parametrized(a, b, expected):
    assert divide(a, b) == expected

# 4. Using Fixtures (mock_db, user_manager come from conftest.py)
def test_get_user_names(user_manager, mock_db):
    # Arrange: Setup mock behavior
    mock_db.get_users.return_value = [
        {"name": "alice", "id": 1},
        {"name": "bob", "id": 2}
    ]
    
    # Act
    names = user_manager.get_user_names()
    
    # Assert
    assert names == ["ALICE", "BOB"]
    mock_db.get_users.assert_called_once()

def test_add_user_success(user_manager, mock_db):
    user = user_manager.add_user("charlie")
    
    assert user["name"] == "charlie"
    # Verify DB was called with correct data
    mock_db.save_user.assert_called_with({"name": "charlie", "active": True})

def test_add_user_empty_fails(user_manager):
    with pytest.raises(ValueError, match="Name cannot be empty"):
        user_manager.add_user("")

# 5. Using Markers
@pytest.mark.skip(reason="Work in progress")
def test_wip():
    assert False
