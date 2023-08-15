from server import loadClubs

def test_loadClubs():
    
    # Arrange : 
    first_club_name = "Simply Lift"
    clubs_length = 3

    # Act : 
    loaded_clubs = loadClubs()

    # Assert : 
    assert loaded_clubs[0]['name'] == first_club_name
    assert len(loaded_clubs) == clubs_length
