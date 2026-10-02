from typing import Any

from app.integration.graph_client import GraphClient


class GraphScoringAdapter:
    """
    Converts graph-service VASP matches into
    scoring-service input structures.
    """

    def __init__(self):
        self.graph_client = GraphClient()

    def get_scoring_inputs(
        self,
        wallet: str,
        chain: str,
        max_hops: int,
        transactions: list[dict],
    ) -> list[dict[str, Any]]:

        graph_response = self.graph_client.analyze(
            wallet=wallet,
            chain=chain,
            max_hops=max_hops,
            transactions=transactions,
        )

        data = graph_response["data"]

        scoring_inputs = []

        for match in data["vasp_matches"]:
            vasp = match["vasp"]

            scoring_inputs.append(
                {
                    "input_wallet": data["input_wallet"],
                    "candidate_vasp": {
                        "vasp_id": vasp["vasp_id"],
                        "vasp_name": vasp["name"],
                    },
                    "features": {
                        "graph_distance": match["graph_distance"],
                        "known_address_match": vasp["known"],
                        "address_confidence": (
                            match["address_confidence"]
                        ),
                        "path_strength": match["path_strength"],
                        "transaction_count": (
                            match["transaction_count"]
                        ),
                    },
                }
            )

        return scoring_inputs