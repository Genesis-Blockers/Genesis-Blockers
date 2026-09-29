import uuid
from typing import List

from app.models.investigation import InvestigationRequest, InvestigationResponse
from app.models.domain import AttributionResult
from app.services.blockchain import BlockchainDataService
from app.services.vasp_intelligence import VaspIntelligenceService
from app.services.graph import GraphService
from app.services.scoring import ScoringEngineService

class InvestigationOrchestrator:
    def __init__(self):
        self.blockchain_service = BlockchainDataService()
        self.vasp_service = VaspIntelligenceService()
        self.graph_service = GraphService(self.blockchain_service, self.vasp_service)
        self.scoring_service = ScoringEngineService()

    def run_investigation(self, request: InvestigationRequest) -> InvestigationResponse:
        investigation_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
        
        # Step 1: Trace graph to find paths to VASPs
        graph_paths = self.graph_service.build_and_traverse_graph(
            start_wallet=request.wallet,
            chain=request.chain,
            max_hops=request.max_hops
        )

        # Step 2: Calculate scores and build attributions
        attributions: List[AttributionResult] = []
        for path in graph_paths:
            # The last address in the path is the VASP address
            matched_address = path.path[-1]
            vasp = self.vasp_service.get_vasp_by_address(matched_address)
            
            if vasp:
                attribution = self.scoring_service.calculate_scores(
                    vasp=vasp,
                    matched_address=matched_address,
                    path=path
                )
                attributions.append(attribution)

        # Sort attributions by confidence score (descending)
        attributions.sort(key=lambda x: x.confidence_score, reverse=True)

        status = "completed" if attributions else "no_attribution_found"
        message = f"Found {len(attributions)} potential VASP attributions." if attributions else "No known VASPs found within max hops."

        return InvestigationResponse(
            investigation_id=investigation_id,
            wallet=request.wallet,
            chain=request.chain,
            status=status,
            message=message,
            attributions=attributions
        )

# Singleton orchestrator for dependency injection or direct use
orchestrator = InvestigationOrchestrator()
