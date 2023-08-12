def test_points_clubs(client, mock_clubs):
    """
    Teste la route 'points_clubs' pour s'assurer qu'elle renvoie le bon statut HTTP
    et contient les noms de tous les clubs dans la réponse.
    """
    # Arrange 
    expected_club_names = [club['name'].encode() for club in mock_clubs]

    # Act
    response = client.get('/points_clubs')

    # Assert 
    assert response.status_code == 200
    for club_name in expected_club_names:
        assert club_name in response.data

