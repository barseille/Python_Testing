from flask import url_for

from server import EmailError, app

def test_showSummary_valid_email(client, mock_clubs):
    """
    Teste la fonction showSummary avec un email valide.
    Il vérifie ensuite que l'application répond avec un statut 200.
    """

    # Arrange : email valide du premier club
    email = mock_clubs[0]['email']

    # Act : appel fonction showSummary avec 'email'
    response = client.post('/showSummary', data={'email': email})

    # Assert
    assert response.status_code == 200


def test_showSummary_invalid_email(client, monkeypatch):
    """
    Teste la fonction showSummary avec un email invalide.
    La fonction doit retourner une réponse avec le code de statut 302 et l'en-tête de localisation défini sur l'URL de l'index.
    """
    
    # Arrange : tester un email invalide
    def mock_get_email(email):
        raise EmailError('invalid_email@example.com')
    
    monkeypatch.setattr('server.get_email', mock_get_email)
    app.config['SERVER_NAME'] = 'localhost:5000'
    email = 'invalid_email@example.com'

    # Act : appel fonction showSummary avec 'email' invalide
    with app.app_context():  
        response = client.post('/showSummary', data={'email': email})

        # Assert : Vérification réponse 302 avec redirection vers la page d'index
        assert response.status_code == 302  # Redirection
        assert response.location.endswith(url_for('index', _external=False))