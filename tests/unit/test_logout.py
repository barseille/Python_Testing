from flask import url_for


def test_logout(client):
    # Appelle la route de déconnexion
    response = client.get('/logout')

    # Vérifie que le code de statut est 302, ce qui indique une redirection
    assert response.status_code == 302

    # Vérifie que l'URL de redirection est l'URL de la page d'index
    assert response.location.endswith(url_for('index'))
