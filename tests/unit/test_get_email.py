import pytest

from server import get_email, EmailError

def test_get_email_valid(mock_clubs):
    """
    Tester si la fonction get_email retourne le club correspondant à un e-mail valide.
    """
    
    # Arrange
    email = mock_clubs[0]['email']  

    # Act
    club = get_email(email)

    # Assert : Le club retourné doit avoir le même e-mail que celui fourni.
    assert club['email'] == email


def test_get_email_invalid():
    """
    Teste la fonction get_club_by_email avec un email invalide.
    La fonction doit lever une exception EmailError.
    """
    
    # Arrange : email fictif
    email = 'email_invalide@gmail.com'

    # Act & Assert : Une exception EmailError doit être levée.
    with pytest.raises(EmailError):
        get_email(email)


def test_get_email_empty():
    """
    Teste la fonction get_club_by_email avec une chaîne vide.
    La fonction doit lever une exception ValueError.
    """
    
    # Arrange : formulaire vide
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
