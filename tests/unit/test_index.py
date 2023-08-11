def test_index(client):
  
    # Act 
    response = client.get('/')

    # Assert 
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

