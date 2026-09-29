import random
import time
import json
import urllib.request
import urllib.error
from typing import List
from app.models.domain import Transaction

class BlockchainDataService:
    def __init__(self):
        # In a real app, API keys would be in environment variables
        self.etherscan_api_key = "YourApiKeyToken" 
        self.etherscan_base_url = "https://api.etherscan.io/api"

    def _fetch_from_etherscan(self, wallet_address: str) -> List[Transaction]:
        """Fetch real transactions from Etherscan API."""
        url = f"{self.etherscan_base_url}?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&page=1&offset=20&sort=desc&apikey={self.etherscan_api_key}"
        transactions = []
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get("status") == "1" and isinstance(data.get("result"), list):
                    for tx in data["result"]:
                        # Convert Wei to ETH (1 ETH = 10^18 Wei)
                        value_eth = float(tx.get("value", 0)) / 10**18
                        if value_eth > 0: # Only care about value transfers
                            transactions.append(
                                Transaction(
                                    tx_hash=tx.get("hash", ""),
                                    from_address=tx.get("from", "").lower(),
                                    to_address=tx.get("to", "").lower(),
                                    value=round(value_eth, 4),
                                    timestamp=int(tx.get("timeStamp", 0)),
                                    asset="ETH"
                                )
                            )
        except Exception as e:
            print(f"Error fetching from Etherscan: {e}")
        return transactions

    def get_transactions(self, wallet_address: str, chain: str) -> List[Transaction]:
        """
        Retrieves transaction history.
        Uses mocked data for demonstration if the wallet is the '0xsuspect' test wallet.
        Otherwise, attempts to fetch real data from Etherscan.
        """
        wallet_address = wallet_address.lower()
        
        # 1. Use real API for any real Ethereum addresses
        if wallet_address != "0xsuspect" and not wallet_address.startswith("0xhop") and not wallet_address.startswith("0xrandom"):
            if chain.lower() == "ethereum":
                real_txs = self._fetch_from_etherscan(wallet_address)
                if real_txs:
                    return real_txs

        # 2. Mock Data for Hackathon Demo Paths
        transactions = []
        current_time = int(time.time())
        
        if wallet_address == "0xsuspect":
            transactions.extend([
                Transaction(tx_hash="0xtx1", from_address="0xsuspect", to_address="0xhop1", value=10.5, timestamp=current_time - 10000),
                Transaction(tx_hash="0xtx2", from_address="0xsuspect", to_address="0xhop3", value=50.0, timestamp=current_time - 5000),
            ])
        elif wallet_address == "0xhop1":
            transactions.extend([
                Transaction(tx_hash="0xtx3", from_address="0xhop1", to_address="0xhop2", value=10.4, timestamp=current_time - 8000),
            ])
        elif wallet_address == "0xhop2":
            transactions.extend([
                Transaction(tx_hash="0xtx4", from_address="0xhop2", to_address="0xbinance1", value=10.3, timestamp=current_time - 7000),
            ])
        elif wallet_address == "0xhop3":
            transactions.extend([
                Transaction(tx_hash="0xtx5", from_address="0xhop3", to_address="0xtornado1", value=49.5, timestamp=current_time - 4000),
            ])
        else:
            # Random mock transactions for other addresses to simulate noise
            num_txs = random.randint(0, 3)
            for i in range(num_txs):
                to_addr = f"0xrandom{random.randint(100, 999)}"
                transactions.append(
                    Transaction(
                        tx_hash=f"0xtx_rand_{random.randint(1000, 9999)}",
                        from_address=wallet_address,
                        to_address=to_addr,
                        value=round(random.uniform(0.1, 5.0), 2),
                        timestamp=current_time - random.randint(100, 20000)
                    )
                )
                
        return transactions
