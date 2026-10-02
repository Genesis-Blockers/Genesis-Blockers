from pydantic import BaseModel, Field


class CandidateVASP(BaseModel):
    vasp_id: str
    vasp_name: str


class RiskIndicators(BaseModel):
    high_risk_exposure: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    suspicious_transaction_ratio: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    rapid_transaction_activity: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


class ScoringFeatures(BaseModel):
    graph_distance: int = Field(ge=0)
    known_address_match: bool
    address_confidence: float = Field(ge=0.0, le=1.0)
    path_strength: float = Field(ge=0.0, le=1.0)
    transaction_count: int = Field(ge=0)

    risk_indicators: RiskIndicators = RiskIndicators()


class ScoringRequest(BaseModel):
    input_wallet: str
    candidate_vasp: CandidateVASP
    features: ScoringFeatures


class Reason(BaseModel):
    factor: str
    description: str
    contribution: float = Field(
        ge=0.0,
        le=1.0,
    )


class AttributionDetails(BaseModel):
    status: str
    ml_probability: float = Field(
        ge=0.0,
        le=1.0,
    )
    baseline_confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    model_version: str


class RiskDetails(BaseModel):
    score: int = Field(
        ge=0,
        le=100,
    )
    level: str


class ScoringData(BaseModel):
    vasp_id: str
    vasp_name: str

    # Final combined attribution confidence
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    # ML + baseline information
    attribution: AttributionDetails

    # Risk information
    risk: RiskDetails

    # Original evidence used for scoring
    evidence: ScoringFeatures

    # Human-readable explanations
    reasons: list[Reason]


class ScoringResponse(BaseModel):
    # Existing API fields
    vasp_id: str
    vasp_name: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    # Existing ML fields
    ml_probability: float = Field(
        ge=0.0,
        le=1.0,
    )

    baseline_confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    model_version: str
    attribution_status: str

    risk_score: int = Field(
        ge=0,
        le=100,
    )

    risk_level: str

    # New structured information
    attribution: AttributionDetails
    risk: RiskDetails
    evidence: ScoringFeatures
    reasons: list[Reason]

class RankingCandidate(BaseModel):
    vasp_id: str
    vasp_name: str
    features: ScoringFeatures


class RankingRequest(BaseModel):
    input_wallet: str
    candidates: list[RankingCandidate]


class RankedCandidate(BaseModel):
    vasp_id: str
    vasp_name: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    rank: int = Field(ge=1)

class RankingResponse(BaseModel):
    input_wallet: str
    candidates: list[RankedCandidate]