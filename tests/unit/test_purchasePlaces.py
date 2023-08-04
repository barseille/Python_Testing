import pytest
from server import app
from unittest.mock import patch

mock_clubs = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
]

mock_competitions = [
    {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
    {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
]

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@patch('server.clubs', mock_clubs)
@patch('server.competitions', mock_competitions)
def test_purchasePlaces_valid_request(client):
    data = {
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 200
    assert 'Super ! Réservation réussie!' in response.data.decode()

@patch('server.clubs', mock_clubs)
@patch('server.competitions', mock_competitions)
def test_purchasePlaces_not_enough_points(client):
    data = {
        'club': 'Iron Temple',
        'competition': 'Spring Festival',
        'places': '6'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert "Pas assez de points pour réserver ce nombre de places." in response.data.decode()

@patch('server.clubs', mock_clubs)
@patch('server.competitions', mock_competitions)
def test_purchasePlaces_not_enough_places(client):
    data = {
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': '15'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert "Pas assez de places disponibles dans la compétition." in response.data.decode()

@patch('server.clubs', mock_clubs)
@patch('server.competitions', mock_competitions)
def test_purchasePlaces_invalid_club(client):
    data = {
        'club': 'Nonexistent Club',
        'competition': 'Spring Festival',
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 404
    assert 'Club ou compétition non trouvé.' in response.data.decode()

@patch('server.clubs', mock_clubs)
@patch('server.competitions', mock_competitions)
def test_purchasePlaces_invalid_competition(client):
    data = {
        'club': 'Simply Lift',
        'competition': 'Nonexistent Competition',
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 404
    assert 'Club ou compétition non trouvé.' in response.data.decode()
