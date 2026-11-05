import urllib.request
import urllib.error
import json
import time
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API_KEY = os.environ.get("APINEX_API_KEY", "")
BASE_URL = "https://api.apinex.bond/v1"

# The 21 free models on APInex + top standard models
CANDIDATES = [
    # Top 7 SARA Configured Models
    "free/mimo-v2.6-pro",
    "free/deepseek-v4.1-flash",
    "free/deepseek-v4-pro-0813",
    "free/muse-spark-1.3",
    "free/kimi-k3",
    "free/gemini-3.8-flash",
    "free/glm-5.3-flashx",
    
    # Remaining Free Models
    "free/claude-opus-4.6",
    "free/claude-sonnet-4.6",
    "free/deepseek-v4-flash-0731",
    "free/glm-5.3",
    "free/glm-5.3-flash",
    "free/gemini-3.1-pro",
    "free/gpt-6-luna",
    "free/hy4",
    "free/jev-1.13",
    "free/kimi-k2.8",
    "free/mimo-v2.6-flash",
    "free/minimax-m3",
    "free/minimax-m3.1-flash",
    "free/qwen-3.8-max",
    
    # Standard Tier Models
    "deepseek-v4.1-flash",
    "deepseek-v4-flash",
    "gemini-3.8-flash",
    "claude-sonnet-5.5",
    "gpt-6-luna"
]

def test_model(model_id):
    payload = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": "Respond with the single word: OK"}
        ],
        "max_tokens": 15,
        "temperature": 0.1
    }
    
    t0 = time.perf_counter()
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "SARA-Audit/2.5"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            elapsed_ms = (time.perf_counter() - t0) * 1000
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"].strip()
            return {
                "model": model_id,
                "status": "WORKING",
                "code": 200,
                "latency_ms": round(elapsed_ms, 2),
                "reply": content,
                "error": None
            }
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        try:
            body = json.loads(e.read().decode("utf-8"))
            err_msg = body.get("error", {}).get("message", str(e))
        except Exception:
            err_msg = str(e)
        return {
            "model": model_id,
            "status": "ERROR",
            "code": e.code,
            "latency_ms": round(elapsed_ms, 2),
            "reply": None,
            "error": err_msg
        }
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "model": model_id,
            "status": "FAILED",
            "code": 0,
            "latency_ms": round(elapsed_ms, 2),
            "reply": None,
            "error": str(e)
        }

def main():
    print("Waiting 15 seconds to let APInex rate limit bucket fully reset...")
    time.sleep(15)
    
    print(f"Testing {len(CANDIDATES)} Candidate Models with 4.2s delay between requests (under 15 RPM)...")
    results = []
    
    for idx, model_id in enumerate(CANDIDATES, 1):
        res = test_model(model_id)
        results.append(res)
        tag = "[WORKING]" if res["status"] == "WORKING" else f"[{res['code']}]"
        detail = res["reply"] if res["status"] == "WORKING" else res["error"][:65]
        print(f"{idx:2d}/{len(CANDIDATES)} {tag:<9} {model_id:<28} | {res['latency_ms']}ms | {detail}")
        
        # Save progress live to file
        with open("data/apinex_live_audit_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
            
        time.sleep(4.2)
        
    print("\n" + "="*80)
    print("LIVE AUDIT COMPLETE")
    print("="*80)
    working = [r for r in results if r["status"] == "WORKING"]
    working.sort(key=lambda x: x["latency_ms"])
    print(f"TOTAL WORKING MODELS: {len(working)} / {len(results)}")
    for rank, w in enumerate(working, 1):
        print(f"Rank {rank}: {w['model']} ({w['latency_ms']}ms) -> Reply: '{w['reply']}'")

if __name__ == "__main__":
    main()

