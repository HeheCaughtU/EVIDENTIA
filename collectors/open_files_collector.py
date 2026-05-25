import os
import json
import psutil
from datetime import datetime


def open_files_collector(incident_path, tag="snapshot"):
    print("[DEBUG] open_files_collector() started")

    files = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for f in proc.open_files():
                files.append({
                    "pid": proc.pid,
                    "process": proc.name(),
                    "file": f.path
                })
        except Exception:
            continue

    output_dir = os.path.join(incident_path, "open_files")
    os.makedirs(output_dir, exist_ok=True)

    data = {
        "collection_time": datetime.now().isoformat(),
        "tag": tag,
        "open_files": files
    }

    output_file = os.path.join(output_dir, f"open_files_{tag}.json")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Open files saved: {output_file}")