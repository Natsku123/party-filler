from fastapi.testclient import TestClient

from .database import testing_get_db, init_test_db, testing_current_user

from core.deps import get_db, get_current_user

from main import app


client = TestClient(app)

app.dependency_overrides[get_db] = testing_get_db
app.dependency_overrides[get_current_user] = testing_current_user

test_player = init_test_db()


def test_root():
    response = client.get("/")
    assert response.status_code == 200, response.text


