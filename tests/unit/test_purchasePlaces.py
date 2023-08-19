from server import BOOKING_LIMIT


def test_purchasePlaces_valid_request(client, mock_clubs, mock_competitions):
    """ 
    Objectif : Tester une demande de réservation valide :
    
    Ce test simule une requête de réservation :
    - club "Simply Lift" qui a 13 points
    - compétition "Spring Festival" qui a 25 places
    - demande de réservation : 1 place
    
    Il effectue une requête POST à l'URL "/purchasePlaces" avec ces données et 
    vérifie que la réponse a un statut 200 et 
    contient le message 'Super ! Réservation réussie!'.
    """
    
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
    
    # vérifie que la chaîne de caractères est présente dans le contenu de la réponse renvoyée par le serveur.
    assert 'Super ! Réservation réussie!' in response.data.decode()


def test_purchasePlaces_not_enough_points(client, mock_clubs, mock_competitions):
    """ 
    Objectif : Tester une réservation avec un nombre de points insuffisant :
    
    Ce test simule une demande de réservation : 
    - club "Iron Temple" qui n'a que 4 points
    - compétition "Spring Festival" qui a 25 places.
    - une demande de réservation : 6 places. 
    
    Il effectue une requête POST à l'URL "/purchasePlaces" avec ces données et 
    vérifie que la réponse a un statut 400, indiquant une erreur client, et 
    contient le message "Pas assez de points pour réserver ce nombre de places."
    """
    
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


def test_purchasePlaces_invalid_club(client, mock_competitions):
    """ 
    Objectif : Tester une réservation avec un club non existant.

    
    Ce test simule une demande de réservation : 
    - club "Nonexistent Club" (club inexistant)
    - compétition "Spring Festival" qui a 25 places.
    - une demande de réservation : 1 places. 
    
    Il effectue une requête POST à l'URL "/purchasePlaces" avec ces données et 
    vérifie que la réponse a un statut 404, indiquant que le club n'a pas été trouvé, et 
    contient le message "Erreur. Veuillez saisir un nombre de places valides"
    """
 
 
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
    assert 'Erreur. Veuillez saisir un nombre de places valides' in response.data.decode()


def test_purchasePlaces_invalid_competition(client, mock_clubs):
    """ 
    Objectif : Tester une réservation avec une compétition non existante.

    Ce test simule une demande de réservation :
    - club : "Simply Lift"
    - compétition : "Nonexistent Competition"(compétition inexistant)
    - une demande de réservation : 1 place.

    Il effectue une requête POST à l'URL "/purchasePlaces" avec ces données et 
    vérifie que la réponse a un statut 404, indiquant que la ressource demandée 
    (dans ce cas, la compétition) n'a pas été trouvée sur le serveur. 
    Le message d'erreur "Erreur. Veuillez saisir un nombre de places valides" 
    est également vérifié dans la réponse.
    """
    
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
    assert 'Erreur. Veuillez saisir un nombre de places valides' in response.data.decode()


def test_purchasePlaces_exceeding_booking_limit(client, mock_clubs, mock_competitions):
    """ 
    Objectif : Tester une réservation dépassant la limite de réservation.

    Ce test simule une demande de réservation :
    - club : "Simply Lift", qui a 13 points
    - compétition : "Spring Festival", qui a 25 places disponibles
    - une demande de réservation : 13 places, ce qui dépasse la limite de réservation globale (BOOKING_LIMIT).

    Il effectue une requête POST à l'URL "/purchasePlaces" avec ces données et 
    vérifie que la réponse a un statut 400, indiquant un message d'erreur 
    "Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places (12)." 
    car la demande de réservation dépasse la limite autorisée.
    """
    
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
    """ 
    Objectif : Tester une réservation avec un nombre de places négatif ou nul.

    Ce test simule une demande de réservation :
    - club : "Simply Lift", qui a 13 points
    - compétition : "Spring Festival", qui a 25 places 
    - une demande de réservation : 0 places, ce qui est invalide car le nombre de places doit être positif.

    Il effectue une requête POST à l'URL "/purchasePlaces" avec ces données et 
    vérifie que la réponse a un statut 400, indiquant une erreur, 
    car la demande de réservation est invalide avec un nombre de places négatif ou nul. 
    avec un message d'erreur "Le nombre de places demandées doit être un nombre positif." 
    """
    
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
