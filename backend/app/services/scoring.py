from app.models.domain import AttributionResult, GraphPath, VaspEntity

class ScoringEngineService:
    def __init__(self):
        pass

    def calculate_scores(self, vasp: VaspEntity, matched_address: str, path: GraphPath) -> AttributionResult:
        """
        Calculates confidence and risk scores based on graph path and VASP intelligence.
        """
        # 1. Confidence Score Logic
        # Confidence drops as hops increase
        base_confidence = 100.0
        hop_penalty = (path.hops - 1) * 15.0 # 15% penalty per hop after the first
        confidence_score = max(0.0, base_confidence - hop_penalty)
        
        # Adjust confidence based on VASP category
        if vasp.category == "mixer":
            confidence_score *= 0.9 # Mixers obfuscate, so confidence is slightly lower
            
        # 2. Risk Score Logic
        risk_score = 0.0
        
        # Base risk from VASP type
        if vasp.risk_level == "high":
            risk_score += 80.0
        elif vasp.risk_level == "medium":
            risk_score += 40.0
        else:
            risk_score += 10.0
            
        # Increase risk if value transferred is high (e.g. > 10 ETH)
        if path.total_value > 10.0:
            risk_score += 20.0
            
        risk_score = min(100.0, risk_score)

        return AttributionResult(
            vasp_name=vasp.name,
            vasp_category=vasp.category,
            confidence_score=round(confidence_score, 2),
            risk_score=round(risk_score, 2),
            matched_address=matched_address,
            path=path
        )
