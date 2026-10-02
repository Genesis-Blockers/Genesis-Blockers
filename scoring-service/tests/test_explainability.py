from app.explainability.reasons import ReasonGenerator


def test_high_confidence_reasons():
    generator = ReasonGenerator()

    features = {
        "address_confidence": 0.98,
        "graph_distance": 1,
        "transaction_count": 1,
    }

    reasons = generator.generate(features)

    descriptions = [
        reason["description"]
        for reason in reasons
    ]

    assert len(reasons) == 3

    assert "High-confidence VASP address match" in descriptions

    assert (
        "VASP address is directly connected to the wallet"
        in descriptions
    )

    assert (
        "Transaction activity supports the connection"
        in descriptions
    )


def test_low_confidence_reasons():
    generator = ReasonGenerator()

    features = {
        "address_confidence": 0.35,
        "graph_distance": 5,
        "transaction_count": 5,
    }

    reasons = generator.generate(features)

    descriptions = [
        reason["description"]
        for reason in reasons
    ]

    assert "Low-confidence VASP address match" in descriptions

    assert (
        "Multiple transactions support the connection"
        in descriptions
    )