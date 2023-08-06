def test_book_existing_competition_and_club(client):
    """Teste la réservation pour une compétition et un club existants."""
    # Arrange
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 200
    assert competition_name in result.data.decode()


def test_book_past_competition(client):
    """Teste la réservation pour une compétition passée."""
    # Arrange
    competition_name = "Spring Festival"
    club_name = "Simply Lift"

    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 200
    assert "Cette compétition a déjà eu lieu. Réservation impossible." in result.data.decode()


def test_book_non_existent_competition(client):
    """Teste la réservation pour une compétition inexistante."""
    # Arrange
    competition_name = "NonExistentCompetition"
    club_name = "Simply Lift"

    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 200
    assert "Erreur - veuillez réessayer" in result.data.decode()


def test_book_non_existent_club(client):
    """Teste la réservation pour un club inexistant."""
    # Arrange
    competition_name = "Spring Festival"
    club_name = "NonExistentClub"

    # Act
    result = client.get(f"/book/{competition_name}/{club_name}")

    # Assert
    assert result.status_code == 200
    assert "Erreur - veuillez réessayer" in result.data.decode()