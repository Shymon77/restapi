from app import create_app

app = create_app()
client = app.test_client()


def test_get_contacts_unauthorized():
    response = client.get("/contacts/")
    assert response.status_code == 401


import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
