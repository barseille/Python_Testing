# def test_book_existing_competition_and_club(client, mock_clubs, mock_competitions):
#     """Teste la réservation pour une compétition et un club existants."""
    
#     # Arrange
#     competition_name = mock_competitions[0]['name']  
#     club_name = mock_clubs[0]['name']  
    
#     # Act
#     result = client.get(f"/book/{competition_name}/{club_name}")

#     # Assert
#     assert result.status_code == 200
#     assert competition_name in result.data.decode()


# def test_book_future_competition(client, mock_clubs, mock_competitions):
#     """Teste la réservation pour une compétition future."""
    
#     # Arrange
#     competition_name = mock_competitions[0]['name']  
#     club_name = mock_clubs[0]['name']  
    
#     # Act
#     result = client.get(f"/book/{competition_name}/{club_name}")

#     # Assert
#     assert result.status_code == 200
#     assert competition_name in result.data.decode()


# def test_book_non_existent_competition(client, mock_clubs):
#     """Teste la réservation pour une compétition inexistante."""
    
#     # Arrange
#     competition_name = "NonExistentCompetition"
#     club_name = mock_clubs[0]['name']  
#     # Act
#     result = client.get(f"/book/{competition_name}/{club_name}")

#     # Assert
#     assert result.status_code == 200
#     assert "Erreur - veuillez réessayer" in result.data.decode()


# def test_book_non_existent_club(client, mock_clubs, mock_competitions):
#     """Teste la réservation pour un club inexistant."""
    
#     # Arrange
#     competition_name = mock_competitions[0]['name']  
#     club_name = "NonExistentClub"

#     # Act
#     result = client.get(f"/book/{competition_name}/{club_name}")

#     # Assert
#     assert result.status_code == 200
#     assert "Erreur - veuillez réessayer" in result.data.decode()


def test_book_existing_competition_and_club(client, mock_clubs, mock_competitions):
    """Teste la réservation pour une compétition et un club existants."""
    
    # Arrange
    competition_name = mock_competitions[0]['name']
    club_name = mock_clubs[0]['name']
    
    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 200
    assert competition_name in result.data.decode()


def test_book_future_competition(client, mock_clubs, mock_competitions):
    """Teste la réservation pour une compétition future."""
    
    # Arrange
    competition_name = mock_competitions[0]['name']
    club_name = mock_clubs[0]['name']
    
    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 200
    assert competition_name in result.data.decode()


def test_book_non_existent_competition(client, mock_clubs):
    """Teste la réservation pour une compétition inexistante."""
    
    # Arrange
    competition_name = "NonExistentCompetition"
    club_name = mock_clubs[0]['name']
    
    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 404
    assert "Erreur - Club ou compétition non trouvés, veuillez réessayer" in result.data.decode()


def test_book_non_existent_club(client, mock_clubs, mock_competitions):
    """Teste la réservation pour un club inexistant."""
    
    # Arrange
    competition_name = mock_competitions[0]['name']
    club_name = "NonExistentClub"

    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 404
    assert "Erreur - Club ou compétition non trouvés, veuillez réessayer" in result.data.decode()
