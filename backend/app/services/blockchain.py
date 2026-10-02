import random
import time
import json
import urllib.request
import urllib.error
import re
from datetime import datetime, timezone
from typing import List, Set
from app.models.domain import Transaction

class BlockchainDataService:
    def __init__(self):
        # In a real app, API keys would be in environment variables
        self.etherscan_api_key = "YourApiKeyToken" 
        self.etherscan_base_url = "https://api.etherscan.io/api"
        
    def _is_valid_eth_address(self, address: str) -> bool:
        return bool(re.match(r"^0x[a-fA-F0-9]{40}$", address))

    def _fetch_from_etherscan(self, wallet_address: str) -> List[Transaction]:
        """Fetch real transactions from Etherscan API with pagination and deduplication."""
        transactions = []
        seen_tx_hashes: Set[str] = set()
        page = 1
        offset = 50 # Fetch up to 50 at a time
        max_pages = 5 # Limit to prevent infinite loops / rate limits during demo

        while page <= max_pages:
            url = f"{self.etherscan_base_url}?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&page={page}&offset={offset}&sort=desc&apikey={self.etherscan_api_key}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    
                    # Handle rate limiting or errors
                    if data.get("status") == "0" and data.get("message") == "NOTOK":
                        print(f"Etherscan API error: {data.get('result')}")
                        break
                        
                    if data.get("status") == "1" and isinstance(data.get("result"), list):
                        results = data["result"]
                        if not results:
                            break # No more transactions
                            
                        for tx in results:
                            tx_hash = tx.get("hash", "")
                            if not tx_hash or tx_hash in seen_tx_hashes:
                                continue
                                
                            seen_tx_hashes.add(tx_hash)
                            
                            # Convert Wei to ETH
                            value_eth = float(tx.get("value", 0)) / 10**18
                            if value_eth > 0: # Only care about value transfers
                                
                                # Format timestamp to ISO-8601
                                ts_int = int(tx.get("timeStamp", 0))
                                ts_iso = datetime.fromtimestamp(ts_int, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                                
                                # Determine status based on txreceipt_status
                                status = "success" if tx.get("txreceipt_status") == "1" else "failed"
                                
                                transactions.append(
                                    Transaction(
                                        tx_hash=tx_hash,
                                        block_number=int(tx.get("blockNumber", 0)),
                                        timestamp=ts_iso,
                                        from_address=tx.get("from", "").lower(),
                                        to_address=tx.get("to", "").lower(),
                                        amount=round(value_eth, 4),
                                        status=status,
                                        asset="ETH"
                                    )
                                )
                        
                        if len(results) < offset:
                            break # Last page reached
                    else:
                        break # Unexpected response
                        
            except Exception as e:
                print(f"Error fetching from Etherscan on page {page}: {e}")
                break
                
            page += 1
            time.sleep(0.2) # Sleep to respect rate limits (5 req/sec free tier)
            
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
                if not self._is_valid_eth_address(wallet_address):
                    print(f"Invalid Ethereum address format: {wallet_address}")
                    return []
                real_txs = self._fetch_from_etherscan(wallet_address)
                if real_txs:
                    return real_txs

        # 2. Mock Data for Hackathon Demo Paths
        transactions = []
        current_time = int(time.time())
        
        def create_mock_tx(tx_hash, from_addr, to_addr, amount, ts_offset):
            ts_iso = datetime.fromtimestamp(current_time - ts_offset, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            return Transaction(
                tx_hash=tx_hash,
                block_number=12345678,
                timestamp=ts_iso,
                from_address=from_addr,
                to_address=to_addr,
                amount=amount,
                status="success",
                asset="ETH"
            )
        
        if wallet_address == "0xsuspect":
            transactions.extend([
                create_mock_tx("0xtx1", "0xsuspect", "0xhop1", 10.5, 10000),
                create_mock_tx("0xtx2", "0xsuspect", "0xhop3", 50.0, 5000),
            ])
        elif wallet_address == "0xhop1":
            transactions.extend([
                create_mock_tx("0xtx3", "0xhop1", "0xhop2", 10.4, 8000),
            ])
        elif wallet_address == "0xhop2":
            transactions.extend([
                create_mock_tx("0xtx4", "0xhop2", "0xbinance1", 10.3, 7000),
            ])
        elif wallet_address == "0xhop3":
            transactions.extend([
                create_mock_tx("0xtx5", "0xhop3", "0xtornado1", 49.5, 4000),
            ])
        else:
            # Random mock transactions for other addresses to simulate noise
            num_txs = random.randint(0, 3)
            for i in range(num_txs):
                to_addr = f"0xrandom{random.randint(100, 999)}"
                amt = round(random.uniform(0.1, 5.0), 2)
                transactions.append(
                    create_mock_tx(f"0xtx_rand_{random.randint(1000, 9999)}", wallet_address, to_addr, amt, random.randint(100, 20000))
                )
                
        return transactions
