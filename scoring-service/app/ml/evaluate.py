from typing import Dict
from sklearn.model_selection import GroupKFold

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    average_precision_score,
)

from app.ml.model import AttributionModel
from app.scoring.baseline import BaselineScorer
from app.scoring.hybrid import HybridScorer

class ModelEvaluator:
    """
    Evaluates the ML model and compares it with
    the rule-based baseline.
    """

    def evaluate(
        self,
        train_dataset: pd.DataFrame,
        test_dataset: pd.DataFrame,
    ) -> Dict[str, Dict[str, float]]:

        logistic_model = AttributionModel("logistic")
        logistic_model.train(train_dataset)

        logistic_probabilities = logistic_model.predict_proba(
            test_dataset
        )

        logistic_predictions = [
            1 if probability >= 0.5 else 0
            for probability in logistic_probabilities
        ]

        random_forest_model = AttributionModel("random_forest")
        random_forest_model.train(train_dataset)

        rf_probabilities = random_forest_model.predict_proba(
            test_dataset
        )

        rf_predictions = [
            1 if probability >= 0.5 else 0
            for probability in rf_probabilities
        ]

        y_true = test_dataset["label"].astype(int).tolist()

        baseline_scorer = BaselineScorer()

        baseline_scores = [
            baseline_scorer.score(
                {
                    "graph_distance": row["graph_distance"],
                    "transaction_count": row["transaction_count"],
                    "address_confidence": row["address_confidence"],
                }
            )
            for _, row in test_dataset.iterrows()
        ]

        baseline_predictions = [
            1 if score >= 0.5 else 0
            for score in baseline_scores
        ]

        return {
            "logistic_regression": self._calculate_metrics(
                y_true,
                logistic_predictions,
                logistic_probabilities,
            ),
            "random_forest": self._calculate_metrics(
                y_true,
                rf_predictions,
                rf_probabilities,
            ),
            "baseline": self._calculate_metrics(
                y_true,
                baseline_predictions,
                [score / 100 for score in baseline_scores],
            ),
        }

    def _calculate_metrics(
        self,
        y_true,
        predictions,
        probabilities,
    ) -> Dict[str, float]:

        metrics = {
            "accuracy": accuracy_score(
                y_true,
                predictions,
            ),
            "precision": precision_score(
                y_true,
                predictions,
                zero_division=0,
            ),
            "recall": recall_score(
                y_true,
                predictions,
                zero_division=0,
            ),
            "f1": f1_score(
                y_true,
                predictions,
                zero_division=0,
            ),
        }

        # ROC-AUC requires both classes to exist.
        if len(set(y_true)) == 2:
            metrics["roc_auc"] = roc_auc_score(
                y_true,
                probabilities,
            )

            metrics["pr_auc"] = average_precision_score(
                y_true,
                probabilities,
            )
        else:
            metrics["roc_auc"] = 0.0
            metrics["pr_auc"] = 0.0

        return {
            key: round(value, 4)
            for key, value in metrics.items()
        }

    def prediction_details(
        self,
        train_dataset: pd.DataFrame,
        test_dataset: pd.DataFrame,
    ) -> pd.DataFrame:

        model = AttributionModel("random_forest")
        model.train(train_dataset)

        result = test_dataset[
            [
                "case_id",
                "vasp_id",
                "graph_distance",
                "path_strength",
                "transaction_count",
                "address_confidence",
                "known_address_match",
                "distance_score",
                "transaction_score",
                "address_match_score",
                "label",
            ]
        ].copy()

        result["ml_probability"] = model.predict_proba(
            test_dataset
        )

        result["ml_prediction"] = (
            result["ml_probability"] >= 0.5
        ).astype(int)

        result["correct"] = (
            result["ml_prediction"]
            == result["label"]
        )

        return result

    def evaluate_hybrid(
        self,
        train_dataset: pd.DataFrame,
        test_dataset: pd.DataFrame,
    ) -> Dict[str, float]:

        model = AttributionModel("random_forest")
        model.train(train_dataset)

        ml_probabilities = model.predict_proba(test_dataset)

        baseline_scorer = BaselineScorer()
        hybrid_scorer = HybridScorer()

        hybrid_scores = []

        for (_, row), ml_probability in zip(
            test_dataset.iterrows(),
            ml_probabilities,
        ):
            baseline_confidence = baseline_scorer.score(
                {
                    "graph_distance": row["graph_distance"],
                    "transaction_count": row["transaction_count"],
                    "address_confidence": row["address_confidence"],
                }
            )

            hybrid_score = hybrid_scorer.score(
                ml_probability=ml_probability,
                baseline_confidence=baseline_confidence,
            )

            hybrid_scores.append(hybrid_score)

        predictions = [
            1 if score >= 0.5 else 0
            for score in hybrid_scores
        ]

        y_true = test_dataset["label"].astype(int).tolist()

        return self._calculate_metrics(
            y_true,
            predictions,
            hybrid_scores,
        )

    def cross_validate_random_forest(
        self,
        dataset: pd.DataFrame,
        n_splits: int = 5,
    ) -> Dict[str, float]:
        """
        Evaluate Random Forest using stratified k-fold cross-validation.
        Each fold trains a fresh model and evaluates it on unseen data.
        """

        X = dataset.drop(columns=["label"])
        y = dataset["label"].astype(int)
        groups = dataset["case_id"]

        splitter = GroupKFold(
            n_splits=n_splits,
        )

        accuracy_scores = []
        precision_scores = []
        recall_scores = []
        f1_scores = []
        roc_auc_scores = []
        pr_auc_scores = []

        for train_indices, test_indices in splitter.split(X, y, groups=groups):

            train_dataset = dataset.iloc[train_indices].copy()
            test_dataset = dataset.iloc[test_indices].copy()

            model = AttributionModel("random_forest")
            model.train(train_dataset)

            probabilities = model.predict_proba(test_dataset)

            predictions = [
                1 if probability >= 0.5 else 0
                for probability in probabilities
            ]

            y_true = test_dataset["label"].astype(int)

            accuracy_scores.append(
                accuracy_score(y_true, predictions)
            )

            precision_scores.append(
                precision_score(
                    y_true,
                    predictions,
                    zero_division=0,
                )
            )

            recall_scores.append(
                recall_score(
                    y_true,
                    predictions,
                    zero_division=0,
                )
            )

            f1_scores.append(
                f1_score(
                    y_true,
                    predictions,
                    zero_division=0,
                )
            )

            if len(set(y_true)) == 2:
                roc_auc_scores.append(
                    roc_auc_score(
                        y_true,
                        probabilities,
                    )
                )

                pr_auc_scores.append(
                    average_precision_score(
                        y_true,
                        probabilities,
                    )
                )

        return {
            "accuracy_mean": round(
                sum(accuracy_scores) / len(accuracy_scores),
                4,
            ),
            "accuracy_std": round(
                pd.Series(accuracy_scores).std(),
                4,
            ),
            "precision_mean": round(
                sum(precision_scores) / len(precision_scores),
                4,
            ),
            "recall_mean": round(
                sum(recall_scores) / len(recall_scores),
                4,
            ),
            "f1_mean": round(
                sum(f1_scores) / len(f1_scores),
                4,
            ),
            "roc_auc_mean": round(
                sum(roc_auc_scores) / len(roc_auc_scores),
                4,
            ),
            "pr_auc_mean": round(
                sum(pr_auc_scores) / len(pr_auc_scores),
                4,
            ),
        }

if __name__ == "__main__":
    from app.features.dataset import DatasetLoader

    dataset = DatasetLoader().load()

    evaluator = ModelEvaluator()

    print("=== MODEL EVALUATION ===")

    # Existing evaluation
    from app.ml.split import DatasetSplitter

    splitter = DatasetSplitter()
    train_dataset, test_dataset = splitter.split(dataset)

    results = evaluator.evaluate(
        train_dataset,
        test_dataset,
    )

    for model_name, metrics in results.items():
        print(f"\n{model_name}")

        for metric_name, value in metrics.items():
            print(f"  {metric_name}: {value}")

    # Cross-validation
    print("\n=== RANDOM FOREST 5-FOLD CROSS-VALIDATION ===")

    cv_results = evaluator.cross_validate_random_forest(
        dataset,
        n_splits=5,
    )

    for metric_name, value in cv_results.items():
        print(f"  {metric_name}: {value}")