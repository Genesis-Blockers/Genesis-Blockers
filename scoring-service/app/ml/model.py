import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


FEATURE_COLUMNS = [
    "graph_distance",
    "path_strength",
    "transaction_count",
    "address_confidence",
    "known_address_match",
    "distance_score",
    "transaction_score",
    "address_match_score",
]


class AttributionModel:
    def __init__(self, model_type: str = "logistic"):
        self.model_type = model_type

        if model_type == "logistic":
            self.model = LogisticRegression(
                random_state=42,
                max_iter=1000,
            )

        elif model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                max_depth=6,
                min_samples_leaf=2,
            )

        else:
            raise ValueError(
                f"Unsupported model type: {model_type}"
            )

    def train(self, dataset: pd.DataFrame) -> None:
        X = self._prepare_features(dataset)
        y = dataset["label"].astype(int)

        self.model.fit(X, y)

    def predict_proba(
        self,
        dataset: pd.DataFrame,
    ) -> list[float]:
        X = self._prepare_features(dataset)

        probabilities = self.model.predict_proba(X)

        return probabilities[:, 1].tolist()

    def predict(
        self,
        dataset: pd.DataFrame,
    ) -> list[int]:
        X = self._prepare_features(dataset)

        return self.model.predict(X).tolist()

    def feature_importance(self) -> dict[str, float]:
        """
        Return feature importance for models that expose it.
        """

        if not hasattr(self.model, "feature_importances_"):
            return {}

        return dict(
            zip(
                FEATURE_COLUMNS,
                self.model.feature_importances_,
            )
        )

    def _prepare_features(
        self,
        dataset: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Prepare model-ready numerical features.
        """

        features = dataset[FEATURE_COLUMNS].copy()

        features["known_address_match"] = (
            features["known_address_match"]
            .astype(int)
        )

        return features