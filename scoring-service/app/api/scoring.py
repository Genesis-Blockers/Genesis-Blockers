import pandas as pd
from fastapi import APIRouter

from app.explainability.reasons import ReasonGenerator
from app.ml.model_loader import ModelLoader
from app.schemas.scoring import (
    RankingRequest,
    RankingResponse,
    RankedCandidate,
    ScoringRequest,
    ScoringResponse,
)
from app.scoring.baseline import BaselineScorer
from app.scoring.hybrid import HybridScorer
from app.scoring.risk import RiskScorer
from app.scoring.ranking import CandidateRanker

router = APIRouter()

baseline_scorer = BaselineScorer()
hybrid_scorer = HybridScorer()
reason_generator = ReasonGenerator()
risk_scorer = RiskScorer()

model_loader = ModelLoader().load()


@router.post(
    "/scoring/calculate",
    response_model=ScoringResponse,
)
def calculate_score(request: ScoringRequest):

    # features = request.features.model_dump()
    features = request.features.model_dump()

    features["distance_score"] = 1 / max(features["graph_distance"], 1)
    features["transaction_score"] = min(
        features["transaction_count"] / 10,
        1.0,
    )
    features["address_match_score"] = (
        1.0 if features["known_address_match"] else 0.0
    )

    # Rule-based baseline
    baseline_confidence = baseline_scorer.score(
        features
    )

    # ML prediction
    ml_probability = model_loader.predict_proba(
        pd.DataFrame([features])
    )[0]

    # Hybrid attribution confidence
    confidence = hybrid_scorer.score(
        ml_probability=ml_probability,
        baseline_confidence=baseline_confidence,
    )
    if confidence >= 0.70:
        attribution_status = "HIGH_CONFIDENCE"
    elif confidence >= 0.50:
        attribution_status = "MEDIUM_CONFIDENCE"
    else:
        attribution_status = "INCONCLUSIVE"

    # Risk
    risk_score = risk_scorer.score(features)
    risk_level = risk_scorer.risk_level(
        risk_score
    )

    # Explanation
    reasons = reason_generator.generate(features)

    return ScoringResponse(
        vasp_id=request.candidate_vasp.vasp_id,
        vasp_name=request.candidate_vasp.vasp_name,

        confidence=round(confidence, 4),

        ml_probability=round(
            ml_probability,
            4,
        ),

        baseline_confidence=round(
            baseline_confidence,
            4,
        ),

        model_version="rf-v1",

        attribution_status=attribution_status,

        risk_score=risk_score,
        risk_level=risk_level,

        attribution={
            "status": attribution_status,
            "ml_probability": round(
                ml_probability,
                4,
            ),
            "baseline_confidence": round(
                baseline_confidence,
                4,
            ),
            "model_version": "rf-v1",
        },

        risk={
            "score": risk_score,
            "level": risk_level,
        },

        evidence={
            "graph_distance": request.features.graph_distance,
            "known_address_match": (
                request.features.known_address_match
            ),
            "address_confidence": (
                request.features.address_confidence
            ),
            "path_strength": (
                request.features.path_strength
            ),
            "transaction_count": (
                request.features.transaction_count
            ),
            "risk_indicators": (
                request.features.risk_indicators.model_dump()
            ),
        },

        reasons=reasons,
    )

@router.post(
    "/scoring/rank",
    response_model=RankingResponse,
)
def rank_candidates(request: RankingRequest):

    rows = []

    for candidate in request.candidates:
        features = candidate.features.model_dump()

        features["distance_score"] = (
            1 / max(features["graph_distance"], 1)
        )

        features["transaction_score"] = min(
            features["transaction_count"] / 10,
            1.0,
        )

        features["address_match_score"] = (
            1.0
            if features["known_address_match"]
            else 0.0
        )

        rows.append(
            {
                "case_id": request.input_wallet,
                "vasp_id": candidate.vasp_id,
                "vasp_name": candidate.vasp_name,
                **features,
            }
        )

    dataset = pd.DataFrame(rows)

    ranked = CandidateRanker().rank(dataset)

    candidates = [
        RankedCandidate(
            vasp_id=row["vasp_id"],
            vasp_name=row["vasp_name"],
            confidence=round(
                float(row["confidence"]),
                4,
            ),
            rank=int(row["rank"]),
        )
        for _, row in ranked.iterrows()
    ]

    return RankingResponse(
        input_wallet=request.input_wallet,
        candidates=candidates,
    )