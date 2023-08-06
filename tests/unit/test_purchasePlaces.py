import pytest
from server import app, BOOKING_LIMIT

def test_purchasePlaces_valid_request(client):
    # Arrange
    data = {
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '1'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 200
    assert 'Super ! Réservation réussie!' in response.data.decode()

def test_purchasePlaces_not_enough_points(client):
    # Arrange
    data = {
        'club': 'Iron Temple',
        'competition': 'Spring Festival',
        'places': '6'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 400
    assert "Pas assez de points pour réserver ce nombre de places." in response.data.decode()

def test_purchasePlaces_not_enough_places(client):
    # Arrange
    data = {
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': '15'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 400
    assert "Pas assez de places disponibles dans la compétition." in response.data.decode()

def test_purchasePlaces_invalid_club(client):
    # Arrange
    data = {
        'club': 'Nonexistent Club',
        'competition': 'Spring Festival',
        'places': '1'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 404
    assert 'Club ou compétition non trouvé.' in response.data.decode()

def test_purchasePlaces_invalid_competition(client):
    # Arrange
    data = {
        'club': 'Simply Lift',
        'competition': 'Nonexistent Competition',
        'places': '1'
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 404
    assert 'Club ou compétition non trouvé.' in response.data.decode()

def test_purchasePlaces_exceeding_booking_limit(client):
    # Arrange
    data = {
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '13' # Un nombre supérieur à la limite de réservation
    }

    # Act
    response = client.post('/purchasePlaces', data=data)

    # Assert
    assert response.status_code == 400
    assert f"Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places." in response.data.decode()