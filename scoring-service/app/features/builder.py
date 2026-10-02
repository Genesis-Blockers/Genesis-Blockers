from typing import Any, Dict, List


class FeatureBuilder:
    """
    Converts Graph Service candidate evidence into
    candidate-level features used by the scoring system.
    """

    def build_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        vasp = candidate.get("vasp", {})

        graph_distance = candidate.get("graph_distance", 0)
        path_strength = candidate.get("path_strength", 0.0)
        transaction_count = candidate.get("transaction_count", 0)
        address_confidence = candidate.get("address_confidence", 0.0)
        known_address_match = bool(vasp.get("known", False))

        # Derived features
        distance_score = (
            1.0 / graph_distance
            if graph_distance and graph_distance > 0
            else 0.0
        )

        transaction_score = min(
            transaction_count / 10.0,
            1.0,
        )

        address_match_score = 1.0 if known_address_match else 0.0

        return {
            # Identification
            "vasp_id": vasp.get("vasp_id"),
            "vasp_name": vasp.get("vasp_name"),

            # Raw graph / intelligence evidence
            "graph_distance": graph_distance,
            "path_strength": path_strength,
            "transaction_count": transaction_count,
            "address_confidence": address_confidence,
            "known_address_match": known_address_match,

            # Derived numerical features
            "distance_score": distance_score,
            "transaction_score": transaction_score,
            "address_match_score": address_match_score,
        }

    def build_response(
        self,
        graph_response: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Convert an entire Graph Service response into
        candidate-level feature records.
        """

        data = graph_response.get("data", {})
        candidates = data.get("vasp_matches", [])

        return [
            self.build_candidate(candidate)
            for candidate in candidates
        ]