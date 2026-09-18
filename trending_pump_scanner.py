import requests
import json
import time

def fetch_trending_pump_tokens():
    print("=" * 60)
    print(" 🚀 SOLANA PUMP.FUN & GMGN TRENDING & SAFETY SCANNER 🚀 ")
    print("=" * 60)
    print("[*] Fetching trending/hot tokens from GMGN API endpoints...")
    
    url = "https://gmgn.ai/defi/quotation/v1/rank/sol/swaps/1h?orderby=volume&direction=desc"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://gmgn.ai/',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        if data.get('code') != 0:
            print(f"[-] Error fetching data from GMGN: {data.get('msg', 'Unknown error')}")
            print("[*] Falling back to simulated live trending scanner...")
            show_mock_trending()
            return

        tokens = data.get('data', {}).get('rank', [])[:10]
        
        if not tokens:
            print("[-] No tokens found.")
            return

        print(f"\n[+] Successfully fetched {len(tokens)} trending tokens. Analyzing safety...\n")
        
        for i, t in enumerate(tokens, 1):
            symbol = t.get('symbol', 'UNKNOWN')
            name = t.get('name', 'N/A')
            address = t.get('address', 'N/A')
            price = t.get('price', 0)
            mcap = t.get('market_cap', 0)
            volume = t.get('volume', 0)
            holder_count = t.get('holder_count', 0)
            smart_buy = t.get('smart_buy_24h', 0)
            
            # Simple heuristic safety check based on available metrics
            risk_score = 100
            warnings = []
            
            if holder_count < 50:
                risk_score -= 30
                warnings.append("Low holders (<50)")
            
            if mcap and mcap < 10000:
                risk_score -= 20
                warnings.append("Very low market cap (High volatility)")

            print(f"{i}. [{symbol}] - {name}")
            print(f"   Address: {address}")
            print(f"   Market Cap: ${mcap:,.2f} | Volume: ${volume:,.2f} | Holders: {holder_count}")
            print(f"   Smart Buys (24h): {smart_buy}")
            
            if warnings:
                print(f"   \033[93m[!] Risks: {', '.join(warnings)}\033[0m")
                print(f"   \033[93m[!] Safety Score: {risk_score}/100 (CAUTION)\033[0m")
            else:
                print(f"   \033[92m[✓] Safety Score: {risk_score}/100 (Relatively Stable)\033[0m")
            print("-" * 60)

    except Exception as e:
        print(f"[-] Connection or parsing error: {e}")
        print("[*] Showing demonstration mode...")
        show_mock_trending()

def show_mock_trending():
    # Fallback demonstration to show how the scanner filters for potential pump coins safely
    mock_tokens = [
        {"symbol": "PEPEsol", "mcap": 45000, "holders": 320, "dev_sold": False, "smart_money": 12},
        {"symbol": "SOLmoon", "mcap": 12000, "holders": 85, "dev_sold": True, "smart_money": 1},
        {"symbol": "CHAD", "mcap": 890000, "holders": 2400, "dev_sold": False, "smart_money": 45}
    ]
    
    print("\n[DEMO MODE] Analyzing potential pump coins:")
    for i, t in enumerate(mock_tokens, 1):
        print(f"\n{i}. Token: {t['symbol']}")
        print(f"   Market Cap: ${t['mcap']:,} | Holders: {t['holders']} | Smart Money Inflow: {t['smart_money']} wallets")
        if t['dev_sold']:
            print("   \033[91m[-] ALERT: Dev has already sold their bags (Potential Rug/Dump)!\033[0m")
        else:
            print("   \033[92m[+] Dev holding intact. Good momentum.\033[0m")

if __name__ == "__main__":
    fetch_trending_pump_tokens()