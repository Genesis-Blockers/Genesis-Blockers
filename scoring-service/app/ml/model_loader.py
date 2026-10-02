from pathlib import Path

import joblib
import pandas as pd

from app.ml.model import FEATURE_COLUMNS


class ModelLoader:
    def __init__(
        self,
        model_path: str = "models/attribution_random_forest.joblib",
    ):
        self.model_path = Path(model_path)
        self.model = None

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        self.model = joblib.load(self.model_path)

        return self

    def predict_proba(
        self,
        dataset: pd.DataFrame,
    ) -> list[float]:

        if self.model is None:
            raise RuntimeError(
                "Model has not been loaded"
            )

        X = dataset[FEATURE_COLUMNS]

        probabilities = self.model.predict_proba(X)

        return probabilities[:, 1].tolist()

    def feature_importance(self) -> dict[str, float]:
        if self.model is None:
            raise RuntimeError(
                "Model has not been loaded"
            )

        if not hasattr(self.model, "feature_importances_"):
            raise RuntimeError(
                "Loaded model does not expose feature importances"
            )

        return dict(
            zip(
                FEATURE_COLUMNS,
                self.model.feature_importances_,
            )
        )