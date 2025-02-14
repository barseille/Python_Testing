from server import validate_purchase

# Limite de réservation
BOOKING_LIMIT = 12

def test_validate_purchase(mock_clubs):
    
    # Teste un nombre de places valide
    assert validate_purchase(mock_clubs[0], 5) is None

    # Teste un nombre de places négatif
    assert validate_purchase(mock_clubs[0], -5) == "Le nombre de places demandées doit être un nombre positif."

    # Teste une réservation dépassant la limite de réservation
    assert validate_purchase(mock_clubs[0], 13) == f"Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places."

    # Teste un nombre de points insuffisant
    assert validate_purchase(mock_clubs[1], 6) == "Pas assez de points pour réserver ce nombre de places."