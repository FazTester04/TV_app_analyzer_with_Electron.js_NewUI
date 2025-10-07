import sys, os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print("Usage: python reports/report_generator.py path/to/test_log.txt")
        sys.exit(1)

    csv_path = os.path.join("runner", "log_summary.csv")
    if not os.path.exists(csv_path):
        print(f"[ERROR] Missing file: {csv_path}")
        print("Please run log_analyzer.py first.")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    if df.empty:
        print("[ERROR] log_summary.csv is empty — no data to plot.")
        sys.exit(1)

    summary = df["status"].value_counts()
    print(summary)

    # === BAR CHART ===
    plt.figure(figsize=(5,4))
    summary.plot(kind="bar", color=["grey","green","red"])
    plt.title("Test Results (PASS vs FAIL)")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.tight_layout()
    bar_path = os.path.join("reports","pass_fail.png")
    plt.savefig(bar_path)
    plt.close()

    # === PIE CHART ===
    plt.figure(figsize=(5,5))
    summary.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        colors=["grey","green","red"],
        legend=False
    )
    plt.title("Test Results Distribution")
    plt.ylabel("")
    plt.tight_layout()
    pie_path = os.path.join("reports","pass_fail_pie.png")
    plt.savefig(pie_path)
    plt.close()

    print(f"[OK] Saved charts:\n  {bar_path}\n  {pie_path}")

if __name__ == "__main__":
    main()
