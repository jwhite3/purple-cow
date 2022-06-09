import pytest

from fastapi.testclient import TestClient

from cow.app.main import app, current_items
from cow.app.models import Item


@pytest.fixture(scope='module')
def client() -> TestClient:
    return TestClient(app)


test_items = [Item(id=1, name='bob'), Item(id=2, name='sue'), Item(id=3, name='sally'), ]


@pytest.fixture(autouse=True)
def clear_current_items():
    yield
    current_items.clear()  # Reset current_items to original state after the test


@pytest.fixture
def input_items():  # TODO: This isn't great since it effectively re-implements one of the path operation functions
    current_items.clear()
    current_items.update({item.id: item for item in test_items})


def test_add_item(client):
    response = client.post('/items/', json={'id': 1000, 'name': 'Me'})
    assert response.status_code == 200

    content = response.json()

    assert len(current_items) == 1
    assert content['id'] == 1000
    assert content['name'] == 'Me'


@pytest.mark.parametrize('limit', ((None, 3), (2, 2), (1, 1), ), ids=('No limit', 'Limit of 2', 'Limit of 1'))
def test_get_all_items(client, input_items, limit):
    """Test the get_all_items endpoint with various limit values."""
    value, expected = limit

    response = client.get('/items/', params={'limit': value})

    assert response.status_code == 200

    content = response.json()
    assert len(content) == expected


# TODO: It would also be good to add a test/tests to ensure that this is actually idempotent
def test_put_items(client):
    items = [{'id': 100, 'name': 'MyName'}, {'id': 101, 'name': 'MyOtherName'}]

    response = client.put('/items/', json=items)
    assert response.status_code == 201

    assert len(current_items) == 2
    assert sorted(item.name for item in current_items.values()) == ['MyName', 'MyOtherName']


def test_delete_items(client, input_items):
    assert len(current_items)

    response = client.delete('/items/')
    assert response.status_code == 200
    assert not len(current_items)


def test_get_item(client, input_items):
    response = client.get('/items/1')
    assert response.status_code == 200

    content = response.json()
    assert content['id'] == 1
    assert content['name'] == 'bob'


def test_missing_item_reponds_with_404(client, input_items):
    response = client.get('/items/500')
    assert response.status_code == 404


def test_update_item(client, input_items):
    assert current_items[1].name == 'bob'

    response = client.post('/items/1', json={'name': 'NewName'})
    assert response.status_code == 200

    content = response.json()
    assert content['id'] == 1
    assert content['name'] == 'NewName'


def test_update_on_missing_item_responds_with_404(client, input_items):
    response = client.post('/items/25', json={'name': 'NewName'})
    assert response.status_code == 404


def test_delete_item(client, input_items):
    assert len(current_items) == 3

    response = client.delete('/items/3')
    assert response.status_code == 200
    assert len(current_items) == 2
    assert 'sally' not in [item.name for item in current_items.values()]
