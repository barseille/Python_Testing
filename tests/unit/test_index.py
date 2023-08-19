def test_index(client):
    """ 
    Objectif :
    - On attend un status 200
    - Le titre "Welcome to the GUDLFT Registration Portal!" doit être prsésent dans la réponse
    """
  
    # Act 
    response = client.get('/')

    # Assert : 
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

