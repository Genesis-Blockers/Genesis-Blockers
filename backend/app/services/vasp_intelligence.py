from typing import List, Optional
from app.models.domain import VaspEntity

# Mock VASP Database
KNOWN_VASPS = [
    VaspEntity(
        name="Binance",
        category="exchange",
        risk_level="low",
        addresses=["0xbinance1", "0xbinance2", "0xbinance3"]
    ),
    VaspEntity(
        name="Tornado Cash",
        category="mixer",
        risk_level="high",
        addresses=["0xtornado1", "0xtornado2"]
    ),
    VaspEntity(
        name="Huobi",
        category="exchange",
        risk_level="medium",
        addresses=["0xhuobi1"]
    ),
    VaspEntity(
        name="Kraken",
        category="exchange",
        risk_level="low",
        addresses=["0xkraken1"]
    ),
    VaspEntity(
        name="Lazarus Group Wallet",
        category="malicious",
        risk_level="high",
        addresses=["0xlazarus1"]
    ),
    VaspEntity(
        name="AnySwap Bridge",
        category="defi_bridge",
        risk_level="medium",
        addresses=["0xanyswap1"]
    ),
    VaspEntity(
        name="ThorChain Swap",
        category="cross_chain_swap",
        risk_level="medium",
        addresses=["0xthorchain1"]
    ),
    VaspEntity(
        name="Binance Hot Wallet",
        category="hot_wallet",
        risk_level="low",
        addresses=["0xbinancehot1"]
    )
]

class VaspIntelligenceService:
    def __init__(self):
        self.vasp_db = KNOWN_VASPS

    def get_vasp_by_address(self, address: str) -> Optional[VaspEntity]:
        """Check if an address belongs to a known VASP."""
        for vasp in self.vasp_db:
            if address.lower() in [addr.lower() for addr in vasp.addresses]:
                return vasp
        return None

    def get_all_known_addresses(self) -> List[str]:
        """Return a list of all known VASP addresses."""
        addresses = []
        for vasp in self.vasp_db:
            addresses.extend(vasp.addresses)
        return addresses
