import os
import json
import subprocess
from datetime import datetime


def scheduled_tasks_collector(incident_path, tag="snapshot"):
    print("[DEBUG] scheduled_tasks_collector() started")

    output_dir = os.path.join(incident_path, "scheduled_tasks")
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = subprocess.check_output(
            ["schtasks", "/query", "/fo", "LIST"],
            text=True
        )
        tasks = result.splitlines()
    except Exception:
        tasks = ["Failed to collect scheduled tasks"]

    data = {
        "collection_time": datetime.now().isoformat(),
        "tag": tag,
        "tasks": tasks
    }

    output_file = os.path.join(output_dir, f"scheduled_tasks_{tag}.json")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Scheduled tasks saved: {output_file}")