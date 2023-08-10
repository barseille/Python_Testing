def test_complete_booking_flow(client, mock_clubs, mock_competitions):
    # Choisissez un club pour le test
    test_club = None
    for c in mock_clubs:
        if c['name'] == 'Simply Lift':
            test_club = c
            break

    # Choisissez une compétition pour le test
    test_competition = None
    for c in mock_competitions:
        if c['name'] == 'Spring Festival':
            test_competition = c
            break

    # Définissez les valeurs originales des points du club et des places de compétition
    original_club_points = int(test_club['points'])
    original_competition_places = int(test_competition['numberOfPlaces'])

    # Nombre de places à réserver pour le test
    places_required = 3

    # Simulez la connexion en utilisant l'email du club
    response = client.post('/showSummary', data={'email': test_club['email']})
    assert response.status_code == 200

    # Simulez la réservation des places
    response = client.post('/purchasePlaces', data={
        'competition': test_competition['name'],
        'club': test_club['name'],
        'places': places_required
    })
    assert response.status_code == 200

    # Vérifiez si les valeurs ont été mises à jour correctement
    assert int(test_club['points']) == original_club_points - places_required
    assert int(test_competition['numberOfPlaces']) == original_competition_places - places_required
