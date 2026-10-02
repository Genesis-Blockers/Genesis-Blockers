import json
import random
from pathlib import Path

random.seed(42)

DATA_DIR = Path("data/dummy")
DATA_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_SCENARIOS = [
    # Strong direct match
    {
        "graph_distance": 1,
        "path_strength": 0.50,
        "transaction_count": 1,
        "address_confidence": 0.98,
        "known_address_match": True,
        "label": 1,
    },

    # Strong direct match with multiple transactions
    {
        "graph_distance": 1,
        "path_strength": 0.50,
        "transaction_count": 5,
        "address_confidence": 0.95,
        "known_address_match": True,
        "label": 1,
    },

    # Strong but indirect match
    {
        "graph_distance": 4,
        "path_strength": 0.20,
        "transaction_count": 8,
        "address_confidence": 0.92,
        "known_address_match": True,
        "label": 1,
    },

    # Medium-distance strong match
    {
        "graph_distance": 2,
        "path_strength": 0.3333,
        "transaction_count": 4,
        "address_confidence": 0.88,
        "known_address_match": True,
        "label": 1,
    },

    # Direct but weak evidence
    {
        "graph_distance": 1,
        "path_strength": 0.50,
        "transaction_count": 1,
        "address_confidence": 0.40,
        "known_address_match": False,
        "label": 0,
    },

    # Many transactions but weak VASP evidence
    {
        "graph_distance": 3,
        "path_strength": 0.25,
        "transaction_count": 10,
        "address_confidence": 0.45,
        "known_address_match": False,
        "label": 0,
    },

    # Far away with weak confidence
    {
        "graph_distance": 5,
        "path_strength": 0.1667,
        "transaction_count": 6,
        "address_confidence": 0.35,
        "known_address_match": False,
        "label": 0,
    },

    # Close competition
    {
        "graph_distance": 2,
        "path_strength": 0.3333,
        "transaction_count": 3,
        "address_confidence": 0.82,
        "known_address_match": True,
        "label": 1,
    },

    # Close competition, weaker
    {
        "graph_distance": 2,
        "path_strength": 0.3333,
        "transaction_count": 3,
        "address_confidence": 0.75,
        "known_address_match": True,
        "label": 0,
    },

    # High confidence but distant
    {
        "graph_distance": 5,
        "path_strength": 0.1667,
        "transaction_count": 12,
        "address_confidence": 0.90,
        "known_address_match": False,
        "label": 1,
    },

    # Low confidence but many transactions
    {
        "graph_distance": 1,
        "path_strength": 0.50,
        "transaction_count": 12,
        "address_confidence": 0.50,
        "known_address_match": True,
        "label": 0,
    },

    # Ambiguous
    {
        "graph_distance": 4,
        "path_strength": 0.20,
        "transaction_count": 2,
        "address_confidence": 0.40,
        "known_address_match": False,
        "label": 0,
    },

    # High confidence but unknown address
    {
        "graph_distance": 2,
        "path_strength": 0.3333,
        "transaction_count": 4,
        "address_confidence": 0.90,
        "known_address_match": False,
        "label": 1,
    },

    # Known address but weaker attribution
    {
        "graph_distance": 3,
        "path_strength": 0.25,
        "transaction_count": 2,
        "address_confidence": 0.70,
        "known_address_match": True,
        "label": 0,
    },
]

def vary_scenario(scenario):
    """
    Add controlled variation to a base synthetic scenario.

    The label remains attached to the underlying scenario,
    while numerical features receive realistic perturbations.
    """

    varied = scenario.copy()

    # Graph distance remains an integer hop count.
    distance_variation = random.choice([-1, 0, 0, 0, 1])

    varied["graph_distance"] = max(
        1,
        min(
            5,
            scenario["graph_distance"] + distance_variation,
        ),
    )

    # Transaction count gets realistic variation.
    transaction_variation = random.choice(
        [-2, -1, 0, 0, 0, 1, 2]
    )

    varied["transaction_count"] = max(
        1,
        min(
            15,
            scenario["transaction_count"]
            + transaction_variation,
        ),
    )

    # Address confidence varies slightly.
    confidence_variation = random.uniform(
        -0.06,
        0.06,
    )

    varied["address_confidence"] = round(
        max(
            0.20,
            min(
                0.99,
                scenario["address_confidence"]
                + confidence_variation,
            ),
        ),
        2,
    )

    # Path strength is related to distance.
    distance = varied["graph_distance"]

    varied["path_strength"] = round(
        1.0 / (distance + 1),
        4,
    )

    # Occasionally flip the known-address signal.
    # This creates harder classification cases.
    if random.random() < 0.08:
        varied["known_address_match"] = (
            not scenario["known_address_match"]
        )

    return varied

def make_candidate(case_id, candidate_number, scenario):
    vasp_id = f"vasp_{candidate_number:03d}"

    address = (
        f"0x"
        f"{case_id}"
        f"{candidate_number:02d}"
        f"{'a' * 36}"
    )

    return {
        "address": address,
        "graph_distance": scenario["graph_distance"],
        "transaction_count": scenario["transaction_count"],
        "address_confidence": scenario["address_confidence"],
        "path_strength": scenario["path_strength"],
        "path": [],
        "transactions": [],
        "vasp": {
            "known": scenario["known_address_match"],
            "vasp_id": vasp_id,
            "vasp_name": f"Synthetic VASP {candidate_number:03d}",
        },
        "_label": scenario["label"],
    }


def generate_case(case_id, scenario_pair):
    candidates = []

    for candidate_number, scenario in enumerate(
        scenario_pair,
        start=1,
    ):
        candidates.append(
            make_candidate(
                case_id,
                candidate_number,
                scenario,
            )
        )

    graph_response = {
        "success": True,
        "data": {
            "input_wallet": (
                f"0x{'f' * 40}"
            ),
            "chain": "ethereum",
            "max_hops": 5,
            "node_count": 10,
            "edge_count": 12,
            "reachable_wallet_count": 5,
            "reachable_wallets": [],
            "vasp_matches": candidates,
        },
    }

    return graph_response


def main():
    # Remove old synthetic graph files.
    for file_path in DATA_DIR.glob("graph_response_*.json"):
        file_path.unlink()

    labels = []

    scenario_pairs = []

    # Create 60 investigation cases.
    for _ in range(60):
        scenario_1 = random.choice(FEATURE_SCENARIOS)
        scenario_2 = random.choice(FEATURE_SCENARIOS)

        while scenario_1 == scenario_2:
            scenario_2 = random.choice(FEATURE_SCENARIOS)

        scenario_pairs.append(
            [
                vary_scenario(scenario_1),
                vary_scenario(scenario_2),
            ]
        )

    for case_number, scenario_pair in enumerate(
        scenario_pairs,
        start=1,
    ):
        case_id = f"{case_number:03d}"

        graph_response = generate_case(
            case_id,
            scenario_pair,
        )

        graph_file = (
            DATA_DIR
            / f"graph_response_{case_id}.json"
        )

        with open(
            graph_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                graph_response,
                file,
                indent=2,
            )

        for candidate in graph_response["data"]["vasp_matches"]:
            labels.append(
                {
                    "case_id": case_id,
                    "candidate_vasp_id": candidate["vasp"]["vasp_id"],
                    "label": candidate["_label"],
                }
            )

            # Do not store the development label
            # inside the graph response.
            del candidate["_label"]

        # Rewrite file after removing labels.
        with open(
            graph_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                graph_response,
                file,
                indent=2,
            )

    labels_file = DATA_DIR / "labels.csv"

    with open(
        labels_file,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(
            "case_id,candidate_vasp_id,label\n"
        )

        for row in labels:
            file.write(
                f"{row['case_id']},"
                f"{row['candidate_vasp_id']},"
                f"{row['label']}\n"
            )

    print(
        f"Generated {len(scenario_pairs)} cases."
    )
    print(
        f"Generated {len(labels)} candidate labels."
    )


if __name__ == "__main__":
    main()