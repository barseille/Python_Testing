def test_index(client):
  
    # Act 
    response = client.get('/')

    # Assert : titre h1 est présent dans la requête
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

