from uuid import uuid4


@pytest.mark.asyncio
async def test_get(app, client, mongo_db):
    collection_name = 'test'
    film_id = uuid4()
    await mongo_db[collection_name].insert_one({'film_id': film_id})
    r = await client.get(f'/api/v1/history/get/{collection_name}')
    assert r.status_code == 200
