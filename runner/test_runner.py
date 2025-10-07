import sys
import os
import json
import time
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(ROOT, 'runner', 'test_log.txt')
TV_BASE = "http://127.0.0.1:5000"

def log(msg, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {level} | {msg}"
    print(line)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def clear_log():
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

def run_test(flow):
    steps = flow.get("commands") or flow.get("steps") or []
    if not steps:
        log("[FAIL] No commands found in the flow.", "ERROR")
        return

    log("=== TEST RUN START ===")
    for step in steps:
        try:
            name = step.get("name") or step.get("action", "Unnamed Step")
            log(f"[INFO] Running step: {name}")
            if "url" in step:
                url = step["url"]
                payload = step.get("payload", {})
                response = requests.post(url, json=payload, timeout=5)
                if response.status_code == 200:
                    log(f"[PASS] {name} -> {response.status_code}", "INFO")
                else:
                    log(f"[FAIL] {name} -> {response.status_code} {response.text}", "ERROR")
                continue
            action = step.get("action")
            if action == "power_on":
                response = requests.post(f"{TV_BASE}/power", json={"on": True}, timeout=5)
            elif action == "power_off":
                response = requests.post(f"{TV_BASE}/power", json={"on": False}, timeout=5)
            elif action in ("launch_app", "open_app"):
                app_name = step.get("app", "UnknownApp")
                response = requests.post(f"{TV_BASE}/app/launch", json={"app": app_name}, timeout=5)
            elif action == "play":
                title = step.get("title", "Unknown Title")
                response = requests.post(f"{TV_BASE}/app/play", json={"title": title}, timeout=5)
            elif action == "check_status":
                response = requests.get(f"{TV_BASE}/status", timeout=5)
            elif action == "wait":
                seconds = step.get("seconds", 1)
                log(f"[INFO] Waiting for {seconds}s...")
                time.sleep(seconds)
                continue
            else:
                log(f"[FAIL] Unknown action: {action}", "WARNING")
                continue

            if response.status_code == 200:
                log(f"[PASS] {action} -> {response.status_code}", "INFO")
            else:
                log(f"[FAIL] {action} -> {response.status_code} {response.text}", "ERROR")
        except Exception as e:
            log(f"[FAIL] Exception during step '{step}': {e}", "ERROR")
    log("=== TEST RUN END ===")
    log("[INFO] Test flow completed.\n")

if __name__ == "__main__":
    clear_log()
    if len(sys.argv) > 1:
        flow_path = sys.argv[1]
    else:
        print("No flow file provided.")
        flow_path = input("Enter flow file path (e.g. examples/sample_flow.json): ").strip()
    if not os.path.exists(flow_path):
        print(f" File not found: {flow_path}")
        sys.exit(1)
    try:
        with open(flow_path, "r", encoding="utf-8") as f:
            flow = json.load(f)
        log(f"[INFO] Starting test run for flow: {os.path.basename(flow_path)}")
        run_test(flow)
    except Exception as e:
        log(f"[FAIL] Fatal error: {e}", "ERROR")
