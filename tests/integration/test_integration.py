from server import clubs, competitions, loadClubs, loadCompetitions


def test_complete_booking_flow(client, setup_data):
    
    # Choisissez un club pour le test
    test_club = None
    for c in clubs:
        if c['name'] == 'Simply Lift':
            test_club = c
            break

    # Choisissez une compétition pour le test
    test_competition = None
    for c in competitions:
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

    # Rechargez les clubs et les compétitions depuis les fichiers pour refléter les changements
    updated_clubs = loadClubs()
    updated_competitions = loadCompetitions()

    
    updated_test_club = None
    for c in updated_clubs:
        if c['name'] == 'Simply Lift':
            updated_test_club = c
            break

    updated_test_competition = None
    for c in updated_competitions:
        if c['name'] == 'Spring Festival':
            updated_test_competition = c
            break


    # Vérifiez si les valeurs ont été mises à jour correctement
    assert int(updated_test_club['points']) == original_club_points - places_required
    assert int(updated_test_competition['numberOfPlaces']) == original_competition_places - places_required
