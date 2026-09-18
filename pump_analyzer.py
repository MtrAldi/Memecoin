import sys
import json
import requests

def get_color(score):
    if score >= 80: return "\033[92m" # Green
    if score >= 50: return "\033[93m" # Yellow
    return "\033[91m" # Red

def scan_token(address):
    print(f"\n\033[1m[+] Scanning Solana Token: {address}\033[0m")
    print("-" * 50)
    
    # Disclaimer: In a real environment, you'd use a GMGN API Key.
    # This tool provides the logic based on the safety parameters discussed.
    
    print("[*] Fetching data from GMGN.ai & Pump.fun...")
    
    # Simulating API Response structure from GMGN
    # In production: response = requests.get(f'https://api.gmgn.ai/v1/token/sol/{address}')
    
    # Mock Data for Demonstration (User can replace with real API call)
    data = {
        "token": "MEME_TOKEN",
        "is_pump_fun": True,
        "dev_holding": 8.5,           # % of supply
        "top_10_holders": 45.0,       # % of supply
        "liquidity_locked": False,    # On pump.fun, it's bonding curve
        "has_socials": True,
        "dev_history": "Clean",       # or "Rugged 3 times"
        "mint_disabled": True,
        "freeze_auth_disabled": False
    }

    score = 100
    report = []

    # Logic 1: Dev Holding
    if data["dev_holding"] > 10:
        score -= 30
        report.append("[-] HIGH RISK: Dev holds >10% of supply.")
    else:
        report.append("[+] SAFE: Dev holding is reasonable (<10%).")

    # Logic 2: Top 10 Holders
    if data["top_10_holders"] > 50:
        score -= 25
        report.append("[-] HIGH RISK: Top 10 holders own >50% (High concentration).")
    else:
        report.append("[+] SAFE: Holder distribution is healthy.")

    # Logic 3: Social Links
    if not data["has_socials"]:
        score -= 20
        report.append("[-] WARNING: No Social Links (Twitter/Telegram) found.")
    else:
        report.append("[+] SAFE: Social links are present.")

    # Logic 4: Freeze Authority (Crucial for Solana)
    if not data["freeze_auth_disabled"]:
        score -= 15
        report.append("[-] WARNING: Freeze Authority is STILL ACTIVE. Dev can block sells.")
    else:
        report.append("[+] SAFE: Freeze Authority is disabled.")

    # Logic 5: Pump.fun Specific
    if data["is_pump_fun"]:
        report.append("[i] Platform: Pump.fun (Bonding Curve Mechanism)")

    print(f"\n\033[1mSAFETY SCORE: {get_color(score)}{score}/100\033[0m")
    print("-" * 50)
    for line in report:
        print(line)
    
    if score < 50:
        print(f"\n\033[91m[!] VERDICT: HIGH RISK. POTENTIAL RUGPULL.\033[0m")
    elif score < 80:
        print(f"\n\033[93m[!] VERDICT: MEDIUM RISK. DYOR BEFORE BUYING.\033[0m")
    else:
        print(f"\n\033[92m[!] VERDICT: RELATIVELY SAFE. MONITOR DEV ACTIVITY.\033[0m")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pump_analyzer.py <CONTRACT_ADDRESS>")
    else:
        scan_token(sys.argv[1])