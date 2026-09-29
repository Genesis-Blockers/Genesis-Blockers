from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
    tx_hash: str
    from_address: str
    to_address: str
    value: float
    timestamp: int
    asset: str = "ETH"

class VaspEntity(BaseModel):
    name: str
    category: str  # exchange, mixer, bridge, custodial, etc.
    risk_level: str  # high, medium, low
    addresses: List[str]

class GraphPath(BaseModel):
    path: List[str]
    transactions: List[Transaction]
    total_value: float
    hops: int

class AttributionResult(BaseModel):
    vasp_name: str
    vasp_category: str
    confidence_score: float
    risk_score: float
    matched_address: str
    path: GraphPath
