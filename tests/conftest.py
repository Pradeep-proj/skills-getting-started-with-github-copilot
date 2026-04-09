import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(scope="session")
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.reset_activities()
    yield
