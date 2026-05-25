import os
import json
from datetime import datetime


def prefetch_collector(incident_path):
    print("[DEBUG] prefetch_collector() started")

    prefetch_path = r"C:\Windows\Prefetch"
    files = []

    try:
        files = os.listdir(prefetch_path)
    except Exception:
        files = ["Access denied or Prefetch disabled"]

    output_dir = os.path.join(incident_path, "prefetch")
    os.makedirs(output_dir, exist_ok=True)

    data = {
        "collection_time": datetime.now().isoformat(),
        "prefetch_files": files
    }

    output_file = os.path.join(output_dir, "prefetch.json")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Prefetch data saved: {output_file}")