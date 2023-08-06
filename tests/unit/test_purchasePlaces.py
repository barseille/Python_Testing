import pytest
from server import app, BOOKING_LIMIT

# # Clubs fictifs
# mock_clubs = [
#     {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
#     {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
#     {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
# ]

# # Compétitions fictives
# mock_competitions = [
#     {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
#     {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
# ]

# Clubs fictifs
mock_clubs = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "15"}, # Augmentez les points à 15
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
]

# Compétitions fictives
mock_competitions = [
    {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
    {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"}, # 13 places disponibles
]




# Création de client de test avec des données fictives
@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr('server.clubs', mock_clubs)
    monkeypatch.setattr('server.competitions', mock_competitions)
    with app.test_client() as client:
        yield client


def test_purchasePlaces_valid_request(client):
    """
    Teste l'achat de places avec une requête valide.
    La fonction doit retourner un code de statut 200 et un message de réussite.
    """
    
    data = {
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 200
    assert 'Super ! Réservation réussie!' in response.data.decode()


def test_purchasePlaces_not_enough_points(client):
    """
    Teste l'achat de places avec un club n'ayant pas assez de points.
    La fonction doit retourner un code de statut 400 et un message d'erreur.
    """
    
    data = {
        'club': 'Iron Temple',
        'competition': 'Spring Festival',
        'places': '6'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert "Pas assez de points pour réserver ce nombre de places." in response.data.decode()

def test_purchasePlaces_not_enough_places(client):
    """
    Teste l'achat de places avec une compétition n'ayant pas assez de places disponibles.
    La fonction doit retourner un code de statut 400 et un message d'erreur.
    """
    
    data = {
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': '15'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert "Pas assez de places disponibles dans la compétition." in response.data.decode()

def test_purchasePlaces_invalid_club(client):
    """
    Teste l'achat de places avec un club inexistant.
    La fonction doit retourner un code de statut 404 et un message d'erreur.
    """
    
    data = {
        'club': 'Nonexistent Club',
        'competition': 'Spring Festival',
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 404
    assert 'Club ou compétition non trouvé.' in response.data.decode()

def test_purchasePlaces_invalid_competition(client):
    """
    Teste l'achat de places avec une compétition inexistante.
    La fonction doit retourner un code de statut 404 et un message d'erreur.
    """
    
    data = {
        'club': 'Simply Lift',
        'competition': 'Nonexistent Competition',
        'places': '1'
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 404
    assert 'Club ou compétition non trouvé.' in response.data.decode()

def test_purchasePlaces_exceeding_booking_limit(client):
    """
    Teste l'achat de places avec un nombre de places supérieur à la limite de réservation.
    La fonction doit retourner un code de statut 400 et un message d'erreur.
    """
    
    data = {
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '13' # Un nombre supérieur à la limite de réservation
    }
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert f"Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places." in response.data.decode()
