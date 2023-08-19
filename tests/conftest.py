import pytest
from server import app
from datetime import datetime

# Clubs fictifs
clubs = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
]


# Compétitions fictives
competitions = [
    {"name": "Spring Festival", "date": datetime.strptime("2027-03-27 10:00:00", '%Y-%m-%d %H:%M:%S'), "numberOfPlaces": "25"},
    {"name": "Fall Classic", "date": datetime.strptime("2020-10-22 13:30:00", '%Y-%m-%d %H:%M:%S'), "numberOfPlaces": "13"},
]

# Fixture pour fournir la liste des clubs fictifs aux tests
@pytest.fixture
def mock_clubs():
    return clubs

# Fixture pour fournir la liste des compétitions fictives aux tests
@pytest.fixture
def mock_competitions():
    return competitions

# Création de client de test avec des données fictives
@pytest.fixture
def client(monkeypatch):

    """
    Remplace les fonctions de sauvegarde par des fonctions vides, 
    ce qui empêche les modifications d'être écrites dans les fichiers JSON réels 
    pendant l'exécution des tests
    """

    # Remplace les données réelles par les données fictives
    monkeypatch.setattr('server.clubs', clubs)
    monkeypatch.setattr('server.competitions', competitions)
    
    # Crée un client de test pour simuler les requêtes HTTP
    with app.test_client() as client:
        yield client