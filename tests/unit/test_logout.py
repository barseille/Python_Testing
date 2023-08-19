from flask import url_for

def test_logout(client):
    """
    Teste la route de déconnexion pour s'assurer qu'elle renvoie 
    une redirection (code de statut 302) vers la page d'index.
    """

    # Act : 
    response = client.get('/logout')

    # Assert : 
    assert response.status_code == 302  # Redirection
    assert response.location.endswith(url_for('index'))
