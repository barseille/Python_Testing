def test_points_clubs(client, mock_clubs):
    """
    Objectif : Tester la route 'points_clubs' pour s'assurer qu'elle renvoie le bon statut HTTP
               et contient les noms de tous les clubs dans la réponse.

    Ce test utilise les données fictives des clubs et simule une requête GET à l'URL "/points_clubs".
    Il vérifie ensuite que la réponse a un statut 200 (succès) et que les noms de tous les clubs
    sont présents dans la réponse.

    Clubs utilisés dans ce test :
    - "Simply Lift"
    - "Iron Temple"
    - "She Lifts"
    """
    
    # Arrange 
    club_names = []
    for club in mock_clubs:
        club_names.append(club["name"].encode())

    # Act
    response = client.get('/points_clubs')

    # Assert 
    assert response.status_code == 200
    for c in club_names:
        assert c in response.data

