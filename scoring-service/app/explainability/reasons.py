class ReasonGenerator:

    def generate(self, features):
        reasons = []

        known_address_match = features.get(
            "known_address_match",
            False,
        )

        address_confidence = features.get(
            "address_confidence",
            0.0,
        )

        graph_distance = features.get(
            "graph_distance",
            999,
        )

        transaction_count = features.get(
            "transaction_count",
            0,
        )

        path_strength = features.get(
            "path_strength",
            0.0,
        )

        # Address confidence
        if address_confidence >= 0.90:
            reasons.append(
                {
                    "factor": "address_confidence",
                    "description": (
                        "High-confidence VASP address match"
                    ),
                    "contribution": 0.10,
                }
            )
        elif address_confidence < 0.50:
            reasons.append(
                {
                    "factor": "address_confidence",
                    "description": (
                        "Low-confidence VASP address match"
                    ),
                    "contribution": 0.10,
                }
            )

        # Known address
        if known_address_match:
            reasons.append(
                {
                    "factor": "known_address_match",
                    "description": (
                        "Known VASP address matches the wallet"
                    ),
                    "contribution": 0.40,
                }
            )

        # Graph distance
        if graph_distance == 1:
            reasons.append(
                {
                    "factor": "graph_distance",
                    "description": (
                        "VASP address is directly connected "
                        "to the wallet"
                    ),
                    "contribution": 0.30,
                }
            )
        elif graph_distance <= 2:
            reasons.append(
                {
                    "factor": "graph_distance",
                    "description": (
                        "VASP is closely connected to the "
                        "wallet in the transaction graph"
                    ),
                    "contribution": 0.20,
                }
            )

        # Transaction activity
        if transaction_count >= 5:
            reasons.append(
                {
                    "factor": "transaction_frequency",
                    "description": (
                        "Multiple transactions support "
                        "the connection"
                    ),
                    "contribution": 0.20,
                }
            )
        elif transaction_count > 0:
            reasons.append(
                {
                    "factor": "transaction_frequency",
                    "description": (
                        "Transaction activity supports "
                        "the connection"
                    ),
                    "contribution": 0.10,
                }
            )

        # Path strength
        if path_strength >= 0.50:
            reasons.append(
                {
                    "factor": "path_strength",
                    "description": (
                        "Strong transaction path supports "
                        "the attribution"
                    ),
                    "contribution": 0.10,
                }
            )

        return reasons