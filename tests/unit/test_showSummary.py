from flask import url_for

from server import EmailError, app



def test_showSummary_valid_email(client, monkeypatch, mock_clubs):
    """
    Teste la fonction showSummary avec un email valide.
    
    Ce test utilise un faux utilisateur pour envoyer une requête POST à l'application, 
    en prétendant soumettre le formulaire sur la page '/showSummary' avec l'email du premier club.
    
    Il vérifie ensuite que l'application répond correctement avec un statut 200 et que l'email du premier club 
    apparaît bien dans la réponse. Pour ce faire, il remplace temporairement la fonction get_email par une version factice 
    qui renvoie simplement le premier club, peu importe l'email donné.
    """
    
    # Arrange
    def mock_get_email(email):
        return mock_clubs[0]
    
    monkeypatch.setattr('server.get_email', mock_get_email)
    email = mock_clubs[0]['email']

    # Act
    response = client.post('/showSummary', data={'email': email})

    # Assert
    assert response.status_code == 200
    assert mock_clubs[0]['email'] in response.get_data(as_text=True)


def test_showSummary_invalid_email(client, monkeypatch, mock_clubs):
    """
    Teste la fonction showSummary avec un email invalide.
    La fonction doit retourner une réponse avec le code de statut 302 et l'en-tête de localisation défini sur l'URL de l'index.
    """
    
    # Arrange
    def mock_get_email(email):
        raise EmailError('invalid_email@example.com')
    
    monkeypatch.setattr('server.get_email', mock_get_email)
    app.config['SERVER_NAME'] = 'localhost:5000'
    email = 'invalid_email@example.com'

    # Act
    with app.app_context():  
        response = client.post('/showSummary', data={'email': email})

        # Assert
        assert response.status_code == 302  # Redirection
        assert 'Location' in response.headers
        assert response.headers['Location'].endswith(url_for('index', _external=False))
