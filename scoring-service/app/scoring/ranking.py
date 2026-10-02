import pandas as pd

from app.ml.model_loader import ModelLoader
from app.scoring.baseline import BaselineScorer
from app.scoring.hybrid import HybridScorer


class CandidateRanker:
    """
    Scores and ranks VASP candidates for each investigation case
    using the ML + baseline hybrid confidence.
    """

    def __init__(self):
        self.baseline_scorer = BaselineScorer()
        self.hybrid_scorer = HybridScorer()
        self.model = ModelLoader().load()

    def rank(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate hybrid attribution confidence for every candidate
        and rank candidates within each investigation case.
        """

        dataset = dataset.copy()

        # Derived features required by the ML model.
        dataset["distance_score"] = (
            1 / dataset["graph_distance"].clip(lower=1)
        )

        dataset["transaction_score"] = (
            dataset["transaction_count"] / 10
        ).clip(upper=1.0)

        dataset["address_match_score"] = (
            dataset["known_address_match"].astype(float)
        )

        # ML probability for every candidate.
        ml_probabilities = self.model.predict_proba(dataset)

        # Calculate hybrid confidence candidate-by-candidate.
        hybrid_scores = []

        for (_, row), ml_probability in zip(
            dataset.iterrows(),
            ml_probabilities,
        ):
            baseline_confidence = self.baseline_scorer.score(
                {
                    "graph_distance": row["graph_distance"],
                    "transaction_count": row["transaction_count"],
                    "address_confidence": row["address_confidence"],
                }
            )

            hybrid_confidence = self.hybrid_scorer.score(
                ml_probability=ml_probability,
                baseline_confidence=baseline_confidence,
            )

            hybrid_scores.append(hybrid_confidence)

        dataset["confidence"] = hybrid_scores

        # Rank candidates within each investigation case.
        dataset["rank"] = (
            dataset.groupby("case_id")["confidence"]
            .rank(
                method="dense",
                ascending=False,
            )
            .astype(int)
        )

        return dataset.sort_values(
            ["case_id", "rank"]
        ).reset_index(drop=True)