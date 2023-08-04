from flask import url_for

from server import EmailError, clubs, app



def test_showSummary_valid_email(monkeypatch):
    """
    Teste la fonction showSummary avec un email valide.
    La fonction doit retourner une réponse avec le code de statut 200 et l'email du club dans les données de la réponse.
    """
    
    # Arrange
    def mock_get_email(email):
        return clubs[0]
    monkeypatch.setattr('server.get_email', mock_get_email)
    tester = app.test_client()
    email = clubs[0]['email']

    # Act
    response = tester.post('/showSummary', data={'email': email})

    # Assert
    assert response.status_code == 200
    assert clubs[0]['email'] in response.get_data(as_text=True)


def test_showSummary_invalid_email(monkeypatch):
    """
    Teste la fonction showSummary avec un email invalide.
    La fonction doit retourner une réponse avec le code de statut 302 et l'en-tête de localisation défini sur l'URL de l'index.
    """
    
    # Arrange
    def mock_get_email(email):
        raise EmailError('invalid_email@example.com')
    monkeypatch.setattr('server.get_email', mock_get_email)
    tester = app.test_client()
    app.config['SERVER_NAME'] = 'localhost:5000'
    email = 'invalid_email@example.com'

    # Act
    with app.app_context():  
        response = tester.post('/showSummary', data={'email': email})

        # Assert
        assert response.status_code == 302  # Redirection
        assert 'Location' in response.headers
        # assert response.headers['Location'] == url_for('index', _external=False)
        assert response.headers['Location'].endswith(url_for('index', _external=False))


