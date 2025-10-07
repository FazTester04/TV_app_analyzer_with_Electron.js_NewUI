import sys
import os
import re
import pandas as pd

LOG_PATTERN = re.compile(r"^(?P<ts>[^|]+) \| (?P<level>[^|]+) \| (?P<msg>.*)$")

def parse_log(path):
    entries = []
    if not os.path.exists(path):
        print(f"[ERROR] Log file not found: {path}")
        return pd.DataFrame()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = LOG_PATTERN.match(line)
            if not m:
                continue
            ts = m.group('ts').strip()
            level = m.group('level').strip()
            msg = m.group('msg').strip()
            status = None
            action = None
            error = None
            if msg.startswith('[PASS]'):
                status = 'PASS'
                action = msg[len('[PASS]'):].strip()
            elif msg.startswith('[FAIL]'):
                status = 'FAIL'
                action = msg[len('[FAIL]'):].strip()
            elif msg.startswith('[INFO]'):
                status = 'INFO'
                action = msg[len('[INFO]'):].strip()
            else:
                action = msg
            err_match = re.search(r'\{.*\}|code\": \"(?P<code>[A-Za-z0-9_]+)\"', msg)
            if err_match:
                try:
                    error = err_match.groupdict().get('code')
                except Exception:
                    error = None
            entries.append({
                'timestamp': ts,
                'level': level,
                'status': status,
                'action': action,
                'error': error
            })
    return pd.DataFrame(entries)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyzer/log_analyzer.py path/to/test_log.txt")
        sys.exit(1)
    path = sys.argv[1]
    df = parse_log(path)
    if df.empty:
        print("[WARNING] No log entries parsed or file empty.")
        sys.exit(0)
    total = len(df[df['status'].isin(['PASS','FAIL'])])
    passes = len(df[df['status'] == 'PASS'])
    fails = len(df[df['status'] == 'FAIL'])
    print(f"Total assertions: {total}  PASS: {passes}  FAIL: {fails}")
    common = df[df['status'] == 'FAIL']['action'].value_counts().head(10)
    if not common.empty:
        print("\nTop failures:")
        print(common)
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'runner')
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, 'log_summary.csv')
    try:
        df.to_csv(out_csv, index=False)
        print(f"[OK] Saved summary to {out_csv}")
    except Exception as e:
        print(f"[ERROR] Failed to write CSV: {e}")
if __name__ == '__main__':
    main()
