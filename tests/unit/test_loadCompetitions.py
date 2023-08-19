from server import loadCompetitions

def test_loadCompetitions():
    """ 
    Objectif : Tester la fonction loadCompetitions pour s'assurer qu'elle charge correctement les compétitions.

    Ce test vérifie que la fonction loadCompetitions :
    - la première compétition dans la liste a le nom "Spring Festival"
    - la longueur de la liste des compétitions est de 2
    """
    
    # Arrange : 
    first_competition_name = "Spring Festival"
    competitions_length = 2 
    
    # Act : 
    loaded_competitions = loadCompetitions()

    # Assert : 
    assert loaded_competitions[0]['name'] == first_competition_name
    assert len(loaded_competitions) == competitions_length
