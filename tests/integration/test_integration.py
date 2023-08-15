from flask import url_for


def test_complete_booking_flow(client, mock_clubs, mock_competitions):
    
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
    original_club_points = int(test_club['points'])
    
    # Sauvegarde du nombre de places disponibles pour la compétition avant la réservation
    original_competition_places = int(test_competition['numberOfPlaces'])

    # Nombre de places que l'on souhaite réserver pour le test
    places_required = 3

    # Simule la connexion en utilisant l'email du club
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
    assert int(test_club['points']) == original_club_points - places_required
    
    # Vérifie si le nombre de places disponibles pour la compétition a été correctement déduit après la réservation
    assert int(test_competition['numberOfPlaces']) == original_competition_places - places_required

    # Simule la déconnexion
    response = client.get('/logout')
    assert response.status_code == 302 # Redirection vers la page d'index

    # Vérifie que l'utilisateur est redirigé vers la page d'index
    assert response.location.endswith(url_for('index'))
