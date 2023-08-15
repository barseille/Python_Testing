from server import loadCompetitions

def test_loadCompetitions():
    
    # Arrange : 
    first_competition_name = "Spring Festival"
    competitions_length = 2 
    
    # Act : 
    loaded_competitions = loadCompetitions()

    # Assert : 
    assert loaded_competitions[0]['name'] == first_competition_name
    assert len(loaded_competitions) == competitions_length
