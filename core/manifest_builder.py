import os
import json
from datetime import datetime


def build_manifest(incident_path):
    """
    Builds an evidence manifest for the incident.
    Lists all collected evidence files with metadata.
    """

    manifest = {
        "incident_path": incident_path,
        "generated_at": datetime.now().isoformat(),
        "evidence": []
    }

    for root, dirs, files in os.walk(incident_path):
        for file in files:
            full_path = os.path.join(root, file)

            # skip manifest itself if rerun
            if file == "manifest.json":
                continue

            try:
                stat = os.stat(full_path)

                manifest["evidence"].append({
                    "file_name": file,
                    "relative_path": os.path.relpath(full_path, incident_path),
                    "size_bytes": stat.st_size,
                    "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

            except Exception:
                continue

    manifest_path = os.path.join(incident_path, "manifest.json")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    print(f"[+] Evidence manifest created: {manifest_path}")
