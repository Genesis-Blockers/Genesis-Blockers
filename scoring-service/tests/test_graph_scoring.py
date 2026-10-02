from app.integration.graph_scoring import GraphScoringAdapter


def test_graph_response_converts_to_scoring_inputs():
    adapter = GraphScoringAdapter()

    adapter.graph_client.analyze = lambda **kwargs: {
        "success": True,
        "data": {
            "input_wallet": "0x1111111111111111111111111111111111111111",
            "chain": "ethereum",
            "max_hops": 5,
            "vasp_matches": [
                {
                    "address": "0x2222222222222222222222222222222222222222",
                    "graph_distance": 1,
                    "transaction_count": 1,
                    "address_confidence": 0.95,
                    "path_strength": 0.5,
                    "vasp": {
                        "known": True,
                        "vasp_id": "VASP-DEMO-001",
                        "name": "Demo Exchange",
                        "confidence": 0.95,
                    },
                }
            ],
        },
    }

    result = adapter.get_scoring_inputs(
        wallet="0x1111111111111111111111111111111111111111",
        chain="ethereum",
        max_hops=5,
        transactions=[],
    )

    assert len(result) == 1

    scoring_input = result[0]

    assert scoring_input["input_wallet"] == (
        "0x1111111111111111111111111111111111111111"
    )

    assert scoring_input["candidate_vasp"]["vasp_id"] == (
        "VASP-DEMO-001"
    )

    assert scoring_input["candidate_vasp"]["vasp_name"] == (
        "Demo Exchange"
    )

    assert scoring_input["features"]["graph_distance"] == 1
    assert scoring_input["features"]["known_address_match"] is True
    assert scoring_input["features"]["address_confidence"] == 0.95
    assert scoring_input["features"]["path_strength"] == 0.5
    assert scoring_input["features"]["transaction_count"] == 1
