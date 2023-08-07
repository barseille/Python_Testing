import pytest
import json

from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client




@pytest.fixture
def setup_data():
    # Charger les données originales
    with open('clubs.json', 'r') as file:
        original_clubs = json.load(file)
    with open('competitions.json', 'r') as file:
        original_competitions = json.load(file)

    yield  # Ici, les tests seront exécutés

    # Réinitialiser les données après le test
    with open('clubs.json', 'w') as file:
        json.dump(original_clubs, file, indent=4)
    with open('competitions.json', 'w') as file:
        json.dump(original_competitions, file, indent=4)
