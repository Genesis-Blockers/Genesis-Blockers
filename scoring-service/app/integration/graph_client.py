import httpx


class GraphClient:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8001",
    ):
        self.base_url = base_url.rstrip("/")

    def analyze(
        self,
        wallet: str,
        chain: str,
        max_hops: int,
        transactions: list[dict],
    ) -> dict:
        response = httpx.post(
            f"{self.base_url}/api/v1/graph/analyze",
            json={
                "wallet": wallet,
                "chain": chain,
                "max_hops": max_hops,
                "transactions": transactions,
            },
            timeout=30.0,
        )

        response.raise_for_status()

        return response.json()