from server import loadClubs

def test_loadClubs():
    """ 
    Objectif : Tester la fonction loadClubs pour s'assurer qu'elle charge correctement les clubs.

    Ce test vérifie que la fonction loadClubs renvoie :
    - le premier club dans la liste a le nom "Simply Lift"
    - la longueur de la liste des clubs est de 3
    """
    
    # Arrange : 
    first_club_name = "Simply Lift"
    clubs_length = 3

    # Act : 
    loaded_clubs = loadClubs()

    # Assert : 
    assert loaded_clubs[0]['name'] == first_club_name
    assert len(loaded_clubs) == clubs_length
