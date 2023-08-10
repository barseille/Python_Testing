# import pytest
# from server import app

# # Clubs fictifs
# mock_clubs = [
#     {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
#     {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
#     {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
# ]

# # Compétitions fictives
# mock_competitions = [
#     {"name": "Spring Festival", "date": "2027-03-27 10:00:00", "numberOfPlaces": "25"},
#     {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
# ]


# # Création de client de test avec des données fictives
# @pytest.fixture
# def client(monkeypatch):

#     """
#     Remplace les fonctions de sauvegarde par des fonctions vides, 
#     ce qui empêche les modifications d'être écrites dans les fichiers JSON réels 
#     pendant l'exécution des tests
#     """

#     monkeypatch.setattr('server.clubs', mock_clubs)
#     monkeypatch.setattr('server.competitions', mock_competitions)
#     with app.test_client() as client:
#         yield client


import pytest
from server import app

# Clubs fictifs
clubs = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
]


from datetime import datetime

# Compétitions fictives
competitions = [
    {"name": "Spring Festival", "date": datetime.strptime("2027-03-27 10:00:00", '%Y-%m-%d %H:%M:%S'), "numberOfPlaces": "25"},
    {"name": "Fall Classic", "date": datetime.strptime("2020-10-22 13:30:00", '%Y-%m-%d %H:%M:%S'), "numberOfPlaces": "13"},
]

@pytest.fixture
def mock_clubs():
    return clubs

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

    monkeypatch.setattr('server.clubs', clubs)
    monkeypatch.setattr('server.competitions', competitions)
    with app.test_client() as client:
        yield client


