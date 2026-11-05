import urllib.request
import urllib.error
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

API_KEY = os.environ.get("APINEX_API_KEY", "")
BASE_URL = "https://api.apinex.bond/v1"

def get_all_models():
    req = urllib.request.Request(f"{BASE_URL}/models", headers={
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "SARA-Audit/2.5"
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return [m["id"] for m in data.get("data", [])]

def test_single_model(model_id):
    payload = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": "Hello, respond with ONE word: 'ONLINE'."}
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
        with urllib.request.urlopen(req, timeout=12) as resp:
            elapsed_ms = (time.perf_counter() - t0) * 1000
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"].strip()
            return {
                "model": model_id,
                "status": "WORKING",
                "code": 200,
                "latency_ms": round(elapsed_ms, 2),
                "response": content[:100],
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
            "response": None,
            "error": err_msg
        }
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "model": model_id,
            "status": "FAILED",
            "code": 0,
            "latency_ms": round(elapsed_ms, 2),
            "response": None,
            "error": str(e)
        }

def main():
    print("Fetching models list from APInex...")
    models = get_all_models()
    print(f"Total models found: {len(models)}")
    
    results = []
    print("Testing models concurrently (workers=4)...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_model = {executor.submit(test_single_model, m): m for m in models}
        for future in as_completed(future_to_model):
            res = future.result()
            results.append(res)
            icon = "[OK]  " if res["status"] == "WORKING" else "[FAIL]"
            print(f"{icon} [{res['code']}] {res['model']:<30} | {res['status']:<7} | {res['latency_ms']}ms | {res['response'] or res['error'][:60]}")

    # Save detailed JSON audit
    with open("data/apinex_models_audit.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    working = [r for r in results if r["status"] == "WORKING"]
    working.sort(key=lambda x: x["latency_ms"])
    
    print("\n" + "="*80)
    print(f"AUDIT SUMMARY: {len(working)} WORKING / {len(results)} TOTAL TESTED")
    print("="*80)
    print("RANKED WORKING MODELS (By Speed & Latency):")
    for rank, w in enumerate(working, 1):
        print(f"Rank {rank}: {w['model']} ({w['latency_ms']}ms) -> Reply: '{w['response']}'")

    print("\nNON-WORKING / BLOCKED MODELS:")
    blocked = [r for r in results if r["status"] != "WORKING"]
    for b in blocked:
        print(f"[{b['code']}] {b['model']}: {b['error']}")

if __name__ == "__main__":
    main()
