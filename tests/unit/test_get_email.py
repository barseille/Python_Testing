import pytest

from server import get_email, EmailError

def test_get_email_valid(mock_clubs):
    """
    Objectif : S'assurer que la fonction retourne le bon club pour un e-mail valide.
    """
    
    # Arrange
    email = mock_clubs[0]['email']  

    # Act
    club = get_email(email)

    # Assert : Le club retourné doit avoir le même e-mail que celui fourni.
    assert club['email'] == email


def test_get_email_invalid():
    """
    Objectif : S'assurer que la fonction lève une exception si l'e-mail n'est pas trouvé.
    """
    
    # Arrange : email fictif
    email = 'email_invalide@gmail.com'

    # Act & Assert : Une exception EmailError doit être levée.
    with pytest.raises(EmailError):
        get_email(email)


def test_get_email_empty():
    """
    Objectif : S'assurer que la fonction lève une exception si l'e-mail est vide.
    """
    
    # Arrange : formulaire vide
    email = ''

    # Act & Assert
    with pytest.raises(ValueError):
        get_email(email)


def test_get_email_invalid_format():
    """
    Objectif : S'assurer que la fonction lève une exception 
    si le format de l'e-mail est invalide.
    """
    
    # Arrange
    email = 'invalid_format'

    # Act & Assert
    with pytest.raises(EmailError):
        get_email(email)
