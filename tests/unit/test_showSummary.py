from flask import url_for

from server import EmailError, app

def test_showSummary_valid_email(client, mock_clubs):
    """
    Objectif : S'assurer que la fonction showSummary 
    répond avec un statut 200 pour un email valide.
    """

    # Arrange : email valide du premier club
    email = mock_clubs[0]['email']

    # Act : appel fonction showSummary avec 'email'
    response = client.post('/showSummary', data={'email': email})

    # Assert
    assert response.status_code == 200


def test_showSummary_invalid_email(client, monkeypatch):
    """
    Objectif : S'assurer que la fonction showSummary 
    redirige vers l'URL de l'index pour un email invalide.
    """
    
    # Arrange : tester un email invalide
    def mock_get_email(email):
        raise EmailError('invalid_email@example.com')
    
    monkeypatch.setattr('server.get_email', mock_get_email)
    
    # Configuration du nom du serveur pour un test de redirection.
    app.config['SERVER_NAME'] = 'localhost:5000'
    email = 'invalid_email@example.com'

    # Act : On simule une requête POST vers la route /showSummary de l'appli, 
    # en utilisant l'email comme donnée envoyée dans la requête.
    with app.app_context():  
        response = client.post('/showSummary', data={'email': email})

        # Assert : Vérification réponse 302 avec redirection vers la page d'index
        assert response.status_code == 302  # Redirection
        
        # Vérifie l'envoi d'un email invalide à la fonction showSummary,
        # si ok, l'application redirige vers la page d'index
        assert response.location.endswith(url_for('index', _external=False))