from fastapi import FastAPI
import requests
import json

app = FastAPI()

# Using Helius API (or Solana RPC if needed)
HELIUS_API = "https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY"

@app.get("/analyze")
def analyze(wallet: str):
    if not wallet:
        return {"error": "Wallet address is required"}

    # Fetch transaction history from Helius
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [wallet, {"limit": 10}]
    }
    
    response = requests.post(HELIUS_API, json=payload, headers={"Content-Type": "application/json"})

    if response.status_code != 200:
        return {"error": "Failed to fetch transactions"}

    transactions = response.json().get("result", [])

    paper_handed_tokens = []
    total_missed_profit = 0

    for tx in transactions:
        if "signature" in tx:  # Looking for transaction signature
            signature = tx["signature"]

            # Fetch transaction details
            tx_details_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTransaction",
                "params": [signature, "json"]
            }
            
            tx_details_response = requests.post(HELIUS_API, json=tx_details_payload, headers={"Content-Type": "application/json"})

            if tx_details_response.status_code == 200:
                tx_data = tx_details_response.json().get("result", {})

                # Example of extracting token details (Adjust logic based on actual response)
                token = "UNKNOWN_TOKEN"
                sold_for = 100  # Placeholder
                current_value = 500  # Placeholder

                missed_profit = current_value - sold_for
                if missed_profit > 0:
                    paper_handed_tokens.append({
                        "token": token,
                        "sold_for": sold_for,
                        "current_value": current_value,
                        "missed_profit": missed_profit
                    })
                    total_missed_profit += missed_profit

    return {
        "wallet": wallet,
        "paper_handed_tokens": paper_handed_tokens,
        "total_missed_profit": total_missed_profit
    }
