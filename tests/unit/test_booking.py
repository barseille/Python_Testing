def test_book_existing_competition_and_club(client, mock_clubs, mock_competitions):
    """ 
    Objectif : Tester la réservation pour une compétition et un club existants.

    Ce test simule une demande de réservation pour le club "Simply Lift" et 
    la compétition "Spring Festival",et vérifie que la réponse a un statut 200
    """
    
    # Arrange
    competition_name = mock_competitions[0]['name']
    club_name = mock_clubs[0]['name']
    
    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 200
    assert competition_name in result.data.decode()


def test_book_non_existent_competition(client, mock_clubs):
    """ 
    Objectif : Tester la réservation pour une compétition inexistante.

    Ce test simule une demande de réservation pour le club "Simply Lift" et 
    une compétition inexistante "NonExistentCompetition",
    et vérifie que la réponse a un statut 404, avec un message d'erreur 
    """
    
    # Arrange
    competition_name = "NonExistentCompetition"
    club_name = mock_clubs[0]['name']
    
    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 404
    assert "Erreur - Club ou compétition non trouvés, veuillez réessayer" in result.data.decode()


def test_book_non_existent_club(client, mock_competitions):
    """ 
    Objectif : Tester la réservation pour un club inexistant.

    Ce test simule une demande de réservation pour un club inexistant "NonExistentClub" 
    et la compétition "Spring Festival",et vérifie que la réponse a un statut 404,
    avec un message d'erreur.
    """
    
    # Arrange
    competition_name = mock_competitions[0]['name']
    club_name = "NonExistentClub"

    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 404
    assert "Erreur - Club ou compétition non trouvés, veuillez réessayer" in result.data.decode()
