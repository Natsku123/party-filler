import pytest
import schemathesis
from contextlib import contextmanager
from fastapi import Depends, HTTPException
from fastapi.testclient import TestClient
from sqlmodel import Session

from core.deps import get_db, get_current_user
from core.database import models, crud

from main import app

from test.endpoints.test_creations import (
    test_create_server_1,
    test_create_server_2,
    test_create_game_1,
    test_create_game_2,
    test_create_role_1,
    test_create_role_2,
    test_create_role_3,
    test_create_party_1,
    test_create_party_2,
    test_create_channel_1,
    test_create_channel_2,
    test_create_member_1,
    test_create_member_2,
    test_create_member_3,
)

schemathesis.fixups.install()
schema = schemathesis.from_asgi("/openapi.json", app)


@pytest.fixture(name="client")
def client_default(session: Session):
    with client_fixture(session) as result:
        yield result


@pytest.fixture(name="client_s", scope="session")
def client_session(session_s: Session):
    with client_fixture(session_s) as result:
        yield result


@pytest.fixture(name="schemathesis_setup", scope="session")
def schemathesis_setup(client_s: TestClient):
    """
    Setup data into database before testing with schemathesis
    """
    test_create_server_1(client_s)
    test_create_server_2(client_s)
    test_create_channel_1(client_s, False)
    test_create_channel_2(client_s, False)
    test_create_game_1(client_s)
    test_create_game_2(client_s)
    test_create_party_1(client_s, False)
    test_create_party_2(client_s, False)
    test_create_role_1(client_s, False)
    test_create_role_2(client_s, False)
    test_create_role_3(client_s, False)
    test_create_member_1(client_s, False)
    test_create_member_2(client_s, False)
    test_create_member_3(client_s, False)


@contextmanager
def client_fixture(session: Session):
    def get_testing_get_db():
        return session

    def get_testing_current_user(
        db: Session = Depends(get_testing_get_db),
    ) -> models.Player:
        users = crud.player.get_multi(db)
        if not users:
            raise HTTPException(status_code=404, detail="Player not found")

        return users[0]

    app.dependency_overrides[get_db] = get_testing_get_db
    app.dependency_overrides[get_current_user] = get_testing_current_user

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200, response.text


@schema.parametrize()
def test_api(case, schemathesis_setup):
    response = case.call_asgi()
    case.validate_response(response)
