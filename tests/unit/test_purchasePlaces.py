from server import BOOKING_LIMIT



def test_purchasePlaces_valid_request(client, mock_clubs, mock_competitions):
    """Teste une demande de réservation valide."""
    
    # Arrange
    data = {
        'club': mock_clubs[0]['name'],  
        'competition': mock_competitions[0]['name'],  
        'places': '1'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 200
    assert 'Super ! Réservation réussie!' in response.data.decode()


def test_purchasePlaces_not_enough_points(client, mock_clubs, mock_competitions):
    """Teste une réservation avec un nombre de points insuffisant."""
    
    # Arrange
    data = {
        'club': mock_clubs[1]['name'],  
        'competition': mock_competitions[0]['name'],  
        'places': '6'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 400
    assert "Pas assez de points pour réserver ce nombre de places." in response.data.decode()


def test_purchasePlaces_not_enough_places(client, mock_clubs, mock_competitions):
    """Teste une réservation avec un nombre de places insuffisant dans la compétition."""
    
    # Arrange
    data = {
        'club': mock_clubs[0]['name'],  
        'competition': mock_competitions[1]['name'],  
        'places': '15'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 400
    assert "Pas assez de places disponibles dans la compétition." in response.data.decode()


def test_purchasePlaces_invalid_club(client, mock_clubs, mock_competitions):
    """Teste une réservation avec un club non existant."""
    
    # Arrange
    data = {
        'club': 'Nonexistent Club',
        'competition': mock_competitions[0]['name'],  
        'places': '1'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 404
    assert 'Club ou compétition non trouvé.' in response.data.decode()


def test_purchasePlaces_invalid_competition(client, mock_clubs, mock_competitions):
    """Teste une réservation avec une compétition non existante."""
    
    # Arrange
    data = {
        'club': mock_clubs[0]['name'],  
        'competition': 'Nonexistent Competition',
        'places': '1'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 404
    assert 'Club ou compétition non trouvé.' in response.data.decode()


def test_purchasePlaces_exceeding_booking_limit(client, mock_clubs, mock_competitions):
    """Teste une réservation dépassant la limite de réservation."""
    
    # Arrange
    data = {
        'club': mock_clubs[0]['name'],  
        'competition': mock_competitions[0]['name'],  
        'places': '13' 
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 400
    assert f"Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places." in response.data.decode()
    
    
def test_purchasePlaces_negative_or_zero_places(client, mock_clubs, mock_competitions):
    """Teste une réservation avec un nombre de places négatif ou nul."""
    
    # Arrange
    data = {
        'club': mock_clubs[0]['name'],  
        'competition': mock_competitions[0]['name'],  
        'places': '0' 
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 400
    assert "Le nombre de places demandées doit être un nombre positif." in response.data.decode()
