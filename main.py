from fastapi import FastAPI
import requests

app = FastAPI()

# Solana API endpoint (example using Solscan API)
SOLSCAN_API = "https://api.solscan.io/account/transactions"

@app.get("/analyze")
def analyze(wallet: str):
    if not wallet:
        return {"error": "Wallet address is required"}

    # Fetch transaction history
    response = requests.get(f"{SOLSCAN_API}?address={wallet}")

    if response.status_code != 200:
        return {"error": "Failed to fetch transactions"}

    transactions = response.json()

    paper_handed_tokens = []
    total_missed_profit = 0

    for tx in transactions:
        if "sold" in tx:  # Example logic to find sales
            token = tx["token"]
            sold_for = tx["sold_price"]
            current_value = tx["current_price"]

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
