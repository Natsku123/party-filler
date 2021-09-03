import pytest
from fastapi import Depends, HTTPException
from fastapi.testclient import TestClient
from sqlmodel import Session

from core.deps import get_db, get_current_user
from core.database import models, crud

from main import app


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_testing_get_db():
        return session

    def get_testing_current_user(
        db: Session = Depends(get_testing_get_db),
    ) -> models.Player:
        user = crud.player.get(db, id=1)
        if not user:
            raise HTTPException(status_code=404, detail="Player not found")

        return user

    app.dependency_overrides[get_db] = get_testing_get_db
    app.dependency_overrides[get_current_user] = get_testing_current_user

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200, response.text
