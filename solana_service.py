import requests
from datetime import datetime

RPC_URL = "https://api.mainnet-beta.solana.com"

def get_sol_balance(wallet_address: str) -> float:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [wallet_address]
    }
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10).json()
        if "result" in response and "value" in response["result"]:
            return response["result"]["value"] / 1e9  # Convert lamports to SOL
    except Exception as e:
        print(f"Error fetching SOL balance: {e}")
    return 0.0

def get_spl_tokens(wallet_address: str) -> list:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            wallet_address,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"}
        ]
    }
    tokens = []
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10).json()
        if "result" in response and "value" in response["result"]:
            for item in response["result"]["value"]:
                parsed = item["account"]["data"]["parsed"]["info"]
                mint = parsed["mint"]
                amount = parsed["tokenAmount"]["uiAmount"]
                if amount and amount > 0:
                    tokens.append({"mint": mint, "amount": amount})
    except Exception as e:
        print(f"Error fetching SPL tokens: {e}")
    return tokens

def get_recent_transactions(wallet_address: str, limit: int = 500) -> list:
    """Fetches up to `limit` recent transaction signatures with parsed ISO timestamps."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [wallet_address, {"limit": limit}]
    }
    tx_list = []
    try:
        response = requests.post(RPC_URL, json=payload, timeout=10).json()
        if "result" in response and isinstance(response["result"], list):
            for item in response["result"]:
                if isinstance(item, dict) and "signature" in item:
                    block_time = item.get("blockTime")
                    formatted_time = (
                        datetime.fromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S')
                        if block_time else "N/A"
                    )
                    tx_list.append({
                        "signature": item["signature"],
                        "blockTime": block_time,
                        "timestamp": formatted_time
                    })
    except Exception as e:
        print(f"Error fetching transactions: {e}")
    return tx_list