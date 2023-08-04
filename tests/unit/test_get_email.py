import pytest

from server import get_email, EmailError, clubs

def test_get_email_valid():
    """
    Teste la fonction get_club_by_email avec un email valide.
    La fonction doit retourner le club correspondant à l'email donné.
    """
    
    # Arrange
    email = clubs[0]['email']

    # Act
    club = get_email(email)

    # Assert
    assert club['email'] == email


def test_get_email_invalid():
    """
    Teste la fonction get_club_by_email avec un email invalide.
    La fonction doit lever une exception EmailError.
    """
    
    # Arrange
    email = 'email_invalide@gmail.com'

    # Act & Assert
    with pytest.raises(EmailError):
        get_email(email)


def test_get_email_empty():
    """
    Teste la fonction get_club_by_email avec une chaîne vide.
    La fonction doit lever une exception ValueError.
    """
    
    # Arrange
    email = ''

    # Act & Assert
    with pytest.raises(ValueError):
        get_email(email)


def test_get_email_invalid_format():
    """
    Teste la fonction get_club_by_email avec un format invalide.
    La fonction doit lever une exception EmailError.
    """
    
    # Arrange
    email = 'invalid_format'

    # Act & Assert
    with pytest.raises(EmailError):
        get_email(email)
