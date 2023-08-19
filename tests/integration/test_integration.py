from flask import url_for


def test_complete_booking_flow(client, mock_clubs, mock_competitions):
    """
    Objectif : Tester le flux complet de réservation pour un club et une compétition.

    Ce test simule le processus complet de réservation de places pour une compétition par un club :
    - Sélection du club "Simply Lift" avec 13 points
    - Sélection de la compétition "Spring Festival" avec 25 places
    - Sauvegarde des valeurs initiales pour vérification
    - Simule la connexion en utilisant l'email du club
    - Simule la réservation de 3 places
    - Vérifie si le nombre de points du club est correctement déduit (10 == 13 - 3)
    - Vérifie si le nombre de places disponibles pour la compétition est correctement déduit (22 == 25 - 3)
    - Simule la déconnexion et vérifie la redirection vers la page d'index
    """
    
    # Sélection du club "Simply Lift" pour le test
    test_club = None
    for c in mock_clubs:
        if c['name'] == 'Simply Lift':
            test_club = c
            break

    # Sélection de la compétition "Spring Festival" pour le test
    test_competition = None
    for c in mock_competitions:
        if c['name'] == 'Spring Festival':
            test_competition = c
            break

    # Sauvegarde du nombre de points du club avant la réservation
    # 'Simply Lift' : 13 points
    club_points = int(test_club['points'])
    
    # Sauvegarde du nombre de places disponibles pour la compétition avant la réservation
    # 'Spring Festival' : 25 places
    competition_places = int(test_competition['numberOfPlaces'])

    # Nombre de places que l'on souhaite réserver pour le test
    places_required = 3

    # Simule la connexion en utilisant l'email du club "john@simplylift.co"
    response = client.post('/showSummary', data={'email': test_club['email']})
    assert response.status_code == 200

    # Simule la réservation des places
    response = client.post('/purchasePlaces', data={
        'competition': test_competition['name'],
        'club': test_club['name'],
        'places': places_required
    })
    assert response.status_code == 200

    # Vérifie si le nombre de points du club a été correctement déduit après la réservation
    # 10 == 13 - 3
    assert int(test_club['points']) == club_points - places_required
    
    # Vérifie si le nombre de places disponibles pour la compétition a été correctement déduit après la réservation
    # 22 == 25 - 3
    assert int(test_competition['numberOfPlaces']) == competition_places - places_required

    # Simule la déconnexion
    response = client.get('/logout')
    assert response.status_code == 302 # Redirection vers la page d'index

    # Vérifie que l'utilisateur est redirigé vers la page d'index
    assert response.location.endswith(url_for('index'))
