from uuid import uuid4


@pytest.mark.asyncio
def test_get(app, client):
    r = client.get(f'/api/v1/history/get/{collection_name}')
    assert r.status_code == 200