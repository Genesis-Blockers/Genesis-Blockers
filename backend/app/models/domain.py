from pydantic import BaseModel, Field, ConfigDict
from typing import List

class Transaction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tx_hash: str
    block_number: int
    timestamp: str
    from_address: str = Field(alias="from")
    to_address: str = Field(alias="to")
    asset: str = "ETH"
    amount: float
    status: str

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
