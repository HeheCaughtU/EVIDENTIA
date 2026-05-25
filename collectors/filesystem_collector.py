import os
import json
from datetime import datetime


def filesystem_metadata_collector(incident_path, tag="snapshot"):
    print("[DEBUG] filesystem_metadata_collector() started")

    fs_dir = os.path.join(incident_path, "filesystem_metadata")
    os.makedirs(fs_dir, exist_ok=True)

    data = {
        "scan_time": datetime.now().isoformat(),
        "base_path": os.getcwd(),
        "files": []
    }

    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        for name in files:
            full_path = os.path.join(root, name)

            try:
                stat = os.stat(full_path)

                data["files"].append({
                    "path": full_path,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

            except (FileNotFoundError, PermissionError, OSError):
                # File was deleted, locked, or changed during scan
                continue

    filename = f"filesystem_{tag}.json"
    output_file = os.path.join(fs_dir, filename)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Filesystem metadata saved: {output_file}")
