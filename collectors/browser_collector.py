import os
import shutil
import sqlite3
import json
from datetime import datetime


def browser_history_collector(incident_path):
    print("[DEBUG] browser_history_collector() started")

    output_dir = os.path.join(incident_path, "browser")
    os.makedirs(output_dir, exist_ok=True)

    browsers = {
        "chrome": os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History"
        ),
        "edge": os.path.expandvars(
            r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History"
        )
    }

    results = []

    for browser, path in browsers.items():
        if not os.path.exists(path):
            continue

        try:
            temp_copy = os.path.join(output_dir, f"{browser}_History_copy")

            # ✅ Copy DB (avoid lock)
            shutil.copy2(path, temp_copy)

            conn = sqlite3.connect(temp_copy)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT url, title, visit_count, last_visit_time
                FROM urls
                ORDER BY last_visit_time DESC
                LIMIT 50
            """)

            rows = cursor.fetchall()

            for row in rows:
                results.append({
                    "browser": browser,
                    "url": row[0],
                    "title": row[1],
                    "visit_count": row[2],
                    "last_visit_time": str(row[3])
                })

            conn.close()

        except Exception as e:
            print(f"[ERROR] {browser} history failed: {e}")

    # ✅ Save output
    output_file = os.path.join(output_dir, "browser_history.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"[+] Browser history saved: {output_file}")