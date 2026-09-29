from typing import List, Dict, Set
from app.models.domain import Transaction, GraphPath
from app.services.blockchain import BlockchainDataService
from app.services.vasp_intelligence import VaspIntelligenceService

class GraphService:
    def __init__(self, blockchain_service: BlockchainDataService, vasp_service: VaspIntelligenceService):
        self.blockchain_service = blockchain_service
        self.vasp_service = vasp_service

    def build_and_traverse_graph(self, start_wallet: str, chain: str, max_hops: int) -> List[GraphPath]:
        """
        Traverse the transaction graph from start_wallet up to max_hops.
        Returns paths that end in a known VASP address.
        """
        start_wallet = start_wallet.lower()
        paths_found: List[GraphPath] = []
        
        # Queue for BFS: stores tuples of (current_address, current_path_of_addresses, current_path_of_txs, total_value)
        queue = [(start_wallet, [start_wallet], [], 0.0)]
        visited_edges: Set[str] = set()

        while queue:
            current_address, address_path, tx_path, total_value = queue.pop(0)
            
            # Stop if we reached max hops
            if len(address_path) - 1 >= max_hops:
                continue

            # Fetch outgoing transactions for current address
            transactions = self.blockchain_service.get_transactions(current_address, chain)
            
            for tx in transactions:
                # Prevent cyclic loops
                edge_id = f"{tx.from_address}-{tx.to_address}-{tx.tx_hash}"
                if edge_id in visited_edges:
                    continue
                visited_edges.add(edge_id)

                new_address_path = address_path + [tx.to_address]
                new_tx_path = tx_path + [tx]
                new_total_value = total_value + tx.value

                # Check if the destination is a known VASP
                vasp = self.vasp_service.get_vasp_by_address(tx.to_address)
                if vasp:
                    paths_found.append(
                        GraphPath(
                            path=new_address_path,
                            transactions=new_tx_path,
                            total_value=new_total_value,
                            hops=len(new_address_path) - 1
                        )
                    )
                else:
                    # Enqueue for further traversal
                    queue.append((tx.to_address, new_address_path, new_tx_path, new_total_value))

        return paths_found
