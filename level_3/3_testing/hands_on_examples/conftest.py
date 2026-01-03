import pytest
from unittest.mock import MagicMock
from app import Database, UserManager

@pytest.fixture
def mock_db():
    return MagicMock(spec=Database)

@pytest.fixture
def user_manager(mock_db):
    return UserManager(mock_db)
