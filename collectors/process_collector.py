import os
import json
import psutil
from datetime import datetime

def process_collector(incident_path, tag="snapshot"):
    print("[DEBUG] process_collector() started")

    proc_dir = os.path.join(incident_path, "process_snapshot")
    os.makedirs(proc_dir, exist_ok=True)

    filename = f"process_{tag}.json"
    output_file = os.path.join(proc_dir, filename)

    process_list = []

    for proc in psutil.process_iter(
        ['pid', 'name', 'username', 'create_time', 'exe']
    ):
        try:
            process_list.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "user": proc.info['username'],
                "exe": proc.info['exe'],
                "start_time": datetime.fromtimestamp(
                    proc.info['create_time']
                ).isoformat() if proc.info['create_time'] else None
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(process_list, f, indent=4)

    print(f"[+] Process snapshot saved: {output_file}")
