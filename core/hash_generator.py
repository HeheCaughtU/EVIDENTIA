import os
import json
import hashlib
from datetime import datetime


def sha256_file(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def generate_hashes(incident_path):
    """
    Generates SHA-256 hashes for all evidence files in an incident.
    """

    hashes = {
        "incident_path": incident_path,
        "generated_at": datetime.now().isoformat(),
        "algorithm": "SHA-256",
        "files": []
    }

    for root, dirs, files in os.walk(incident_path):
        for file in files:
            # skip hash & manifest files themselves
            if file in ("hashes.json", "manifest.json"):
                continue

            full_path = os.path.join(root, file)

            try:
                file_hash = sha256_file(full_path)
                stat = os.stat(full_path)

                hashes["files"].append({
                    "file_name": file,
                    "relative_path": os.path.relpath(full_path, incident_path),
                    "size_bytes": stat.st_size,
                    "sha256": file_hash
                })

            except Exception:
                continue

    hashes_path = os.path.join(incident_path, "hashes.json")   

    with open(hashes_path, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=4)

    print(f"[+] Evidence hashes created: {hashes_path}")
